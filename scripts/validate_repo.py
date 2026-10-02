#!/usr/bin/env python3
"""Check skill packaging and evaluation cases; install requirements-dev.txt."""

import csv
import json
import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_BYTES = 14_420


class FrontmatterLoader(yaml.SafeLoader):
    """Read YAML without silently accepting duplicate or non-text field names."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise yaml.constructor.ConstructorError(
                None, None, "campo YAML duplicado ou não textual", key_node.start_mark
            )
        result[key] = loader.construct_object(value_node)
    return result


FrontmatterLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def load_case_pack(cases_path: Path, oracle_path: Path, errors: list[str], label: str):
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{label}: avaliação inválida: {exc}")
        return [], []

    if not isinstance(cases, dict) or not isinstance(oracle, dict):
        errors.append(f"{label}: cases/oracle devem ser objetos JSON")
        return [], []
    if cases.get("version") != 1 or oracle.get("version") != 1:
        errors.append(f"{label}: versão do formato diferente de 1")

    case_items = cases.get("cases", [])
    oracle_items = oracle.get("oracles", [])
    if not isinstance(case_items, list) or not isinstance(oracle_items, list):
        errors.append(f"{label}: cases/oracles devem ser listas")
        return [], []

    case_ids = [item.get("id") for item in case_items if isinstance(item, dict)]
    oracle_ids = [item.get("id") for item in oracle_items if isinstance(item, dict)]
    if (len(case_ids) != len(case_items) or len(oracle_ids) != len(oracle_items)
            or any(not isinstance(case_id, str) or not case_id.strip() for case_id in case_ids + oracle_ids)):
        errors.append(f"{label}: casos/oracles devem ser objetos com id textual")
        return [], []
    if len(set(case_ids)) != len(case_ids) or len(set(oracle_ids)) != len(oracle_ids):
        errors.append(f"{label}: id duplicado")
    if set(case_ids) != set(oracle_ids):
        errors.append(f"{label}: cada caso precisa de exatamente um oracle correspondente")

    for item in case_items:
        mode = item.get("mode")
        if not isinstance(mode, str) or mode not in {"conversation", "snippet"}:
            errors.append(f"{label}/{item.get('id')}: modo inválido")
        if any(not isinstance(item.get(field), str) or not item[field].strip()
               for field in ("id", "domain", "prompt", "evidence")):
            errors.append(f"{label}/{item.get('id')}: dados de entrada incompletos")

    for item in oracle_items:
        for field in ("expected", "forbidden"):
            values = item.get(field)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                errors.append(f"{label}/{item.get('id')}: {field} inválido")
    return case_items, oracle_items


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = root / ".agents/skills/verificar-mudancas"
    skill_file = skill_dir / "SKILL.md"
    try:
        skill_bytes = skill_file.read_bytes()
        skill = skill_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"SKILL.md indisponível: {exc}"]

    normalized_skill_bytes = skill.encode("utf-8")
    if len(normalized_skill_bytes) > MAX_SKILL_BYTES:
        errors.append(f"SKILL.md: {len(normalized_skill_bytes)} bytes normalizados excede orçamento de {MAX_SKILL_BYTES}")

    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if match is None:
        errors.append("SKILL.md: frontmatter ausente")
    else:
        try:
            header = yaml.load(match.group(1), Loader=FrontmatterLoader)
        except yaml.YAMLError as exc:
            errors.append(f"SKILL.md: frontmatter YAML inválido: {exc}")
        else:
            if not isinstance(header, dict):
                errors.append("SKILL.md: frontmatter deve ser um objeto YAML")
            else:
                if set(header) != {"name", "description"}:
                    errors.append("SKILL.md: esperado somente name e description")
                if header.get("name") != "verificar-mudancas":
                    errors.append("SKILL.md: name inesperado")
                description = header.get("description")
                if not isinstance(description, str) or not description.strip():
                    errors.append("SKILL.md: description deve ser texto não vazio")

    expected_references = {
        "references/java.md", "references/python.md", "references/gamedev.md",
        "references/libgdx.md", "references/unity-csharp.md", "references/data.md",
        "references/terraform-iac.md", "references/security.md", "references/api-contracts.md",
        "references/databases-migrations.md", "references/distributed-systems.md",
        "references/observability-sre.md", "references/ci-cd-release.md", "references/performance.md",
        "references/dependencies-supply-chain.md", "references/architecture-refactoring.md",
        "references/frontend-ui-e2e.md", "references/containers-cloud-runtime.md",
        "references/change-evidence.md", "references/regulated-profile.md",
    }
    references = set(re.findall(r"\]\((references/[^)]+\.md)\)", skill))
    if references != expected_references:
        missing = sorted(expected_references - references)
        unexpected = sorted(references - expected_references)
        if missing:
            errors.append(f"SKILL.md: referências esperadas ausentes: {', '.join(missing)}")
        if unexpected:
            errors.append(f"SKILL.md: referências inesperadas: {', '.join(unexpected)}")
    for relative in expected_references:
        if not (skill_dir / relative).is_file():
            errors.append(f"referência ausente: {relative}")

    expected_playbooks = {
        "playbooks/bug-fix.md", "playbooks/game-bug.md", "playbooks/feature.md", "playbooks/refactor.md",
        "playbooks/migration.md", "playbooks/incident.md", "playbooks/dependency-upgrade.md",
        "playbooks/performance-regression.md",
    }
    playbooks = set(re.findall(r"\]\((playbooks/[^)]+\.md)\)", skill))
    if playbooks != expected_playbooks:
        missing = sorted(expected_playbooks - playbooks)
        unexpected = sorted(playbooks - expected_playbooks)
        if missing:
            errors.append(f"SKILL.md: playbooks esperados ausentes: {', '.join(missing)}")
        if unexpected:
            errors.append(f"SKILL.md: playbooks inesperados: {', '.join(unexpected)}")
    for relative in expected_playbooks:
        if not (skill_dir / relative).is_file():
            errors.append(f"playbook ausente: {relative}")

    for relative in {".gitignore", ".gitattributes", "CHANGELOG.md", "CONTRIBUTING.md", "evals/ab/README.md", "evals/oracle-review.example.json", "docs/maturity.md", "scripts/prepare_ab_eval.py", "scripts/eval_protocol.py"}:
        if not (root / relative).is_file():
            errors.append(f"arquivo de manutenção ausente: {relative}")

    try:
        gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f".gitignore indisponível: {exc}")
    else:
        for pattern in (".venv/", "sample.parquet", "target/", ".terraform/", "*.tfstate"):
            if pattern not in gitignore:
                errors.append(f".gitignore: padrão esperado ausente: {pattern}")

    try:
        attributes = (root / ".gitattributes").read_text(encoding="utf-8")
        if "* text=auto eol=lf" not in attributes:
            errors.append(".gitattributes: política LF ausente")
    except OSError as exc:
        errors.append(f".gitattributes indisponível: {exc}")

    for relative in {
        "evals/fixtures/runtime-port-binding/README.md",
        "evals/fixtures/runtime-port-binding/Dockerfile",
        "evals/fixtures/runtime-port-binding/app.py",
        "evals/fixtures/runtime-port-binding/run.sh",
    }:
        if not (root / relative).is_file():
            errors.append(f"fixture runtime ausente: {relative}")

    documents = [root / "README.md", root / "evals/README.md", root / "CONTRIBUTING.md", root / "CHANGELOG.md", skill_file]
    documents.extend(skill_dir / relative for relative in expected_references | expected_playbooks)
    for document in documents:
        try:
            content = document.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"documento indisponível: {exc}")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = target.split("#", 1)[0]
            if not (document.parent / path).exists():
                errors.append(f"{document.relative_to(root)}: link ausente: {target}")

    case_items, _ = load_case_pack(root / "evals/cases.json", root / "evals/oracle.json", errors, "core")
    domains = {
        item["domain"] for item in case_items
        if isinstance(item, dict) and isinstance(item.get("domain"), str)
    }
    required_domains = {"java", "python", "gamedev", "libgdx", "unity", "data", "terraform", "security", "workflow", "api", "database", "distributed", "performance", "release", "runtime"}
    if not required_domains.issubset(domains):
        errors.append("casos não cobrem as áreas mínimas: " + ", ".join(sorted(required_domains - domains)))

    regulated_cases, _ = load_case_pack(root / "evals/profiles/regulated-cases.json", root / "evals/profiles/regulated-oracle.json", errors, "regulated")
    regulated_ids = {item.get("id") for item in regulated_cases if isinstance(item, dict)}
    required_regulated = {"regulated-pii-log", "regulated-secret-log", "regulated-production-command", "regulated-human-approval"}
    if regulated_ids != required_regulated:
        errors.append("regulated: conjunto de casos inesperado")

    required_scorecard_columns = {"run_id", "blind_id", "case_id", "condition", "repetition", "agent", "model", "skill_commit", "access", "run_date", "elapsed_seconds", "response_chars", "classificacao", "aceite", "risco", "causa", "experimento", "fronteira", "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade", "escopo", "violacoes", "observacoes"}
    try:
        with (root / "evals/scorecard.csv").open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle), [])
    except OSError as exc:
        errors.append(f"scorecard.csv indisponível: {exc}")
    else:
        if set(header) != required_scorecard_columns:
            missing = sorted(required_scorecard_columns - set(header))
            unexpected = sorted(set(header) - required_scorecard_columns)
            if missing:
                errors.append(f"scorecard.csv: colunas ausentes: {', '.join(missing)}")
            if unexpected:
                errors.append(f"scorecard.csv: colunas inesperadas: {', '.join(unexpected)}")

    return errors


if __name__ == "__main__":
    repository_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    problems = validate(repository_root)
    if problems:
        for problem in problems:
            print(f"ERRO: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Estrutura modular, orçamento do núcleo e casos de avaliação válidos.")
