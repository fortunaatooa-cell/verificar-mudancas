#!/usr/bin/env python3
"""Check skill packaging and evaluation fixtures without external dependencies."""

import csv
import json
import re
import sys
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = root / ".agents/skills/verificar-mudancas"
    skill_file = skill_dir / "SKILL.md"
    try:
        skill = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"SKILL.md indisponível: {exc}"]

    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if match is None:
        errors.append("SKILL.md: frontmatter ausente")
    else:
        header = match.group(1)
        if not re.search(r"^name: verificar-mudancas$", header, re.MULTILINE):
            errors.append("SKILL.md: name inesperado")
        if not re.search(r"^description: \S.+$", header, re.MULTILINE):
            errors.append("SKILL.md: description ausente")

    expected_references = {
        "references/java.md",
        "references/python.md",
        "references/unity-csharp.md",
        "references/data.md",
        "references/terraform-iac.md",
        "references/security.md",
        "references/api-contracts.md",
        "references/databases-migrations.md",
        "references/distributed-systems.md",
        "references/observability-sre.md",
        "references/ci-cd-release.md",
        "references/performance.md",
        "references/dependencies-supply-chain.md",
        "references/architecture-refactoring.md",
        "references/frontend-ui-e2e.md",
        "references/containers-cloud-runtime.md",
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
        "playbooks/bug-fix.md",
        "playbooks/feature.md",
        "playbooks/refactor.md",
        "playbooks/migration.md",
        "playbooks/incident.md",
        "playbooks/dependency-upgrade.md",
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

    documents = [root / "README.md", root / "evals/README.md", skill_file]
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

    try:
        cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        oracle = json.loads((root / "evals/oracle.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return errors + [f"avaliação inválida: {exc}"]

    if not isinstance(cases, dict) or not isinstance(oracle, dict):
        return errors + ["cases/oracle devem ser objetos JSON"]
    if cases.get("version") != 1 or oracle.get("version") != 1:
        errors.append("versão do formato de avaliação diferente de 1")
    case_items = cases.get("cases", [])
    oracle_items = oracle.get("oracles", [])
    if not isinstance(case_items, list) or not isinstance(oracle_items, list):
        return errors + ["cases/oracles devem ser listas"]

    case_ids = [item.get("id") for item in case_items if isinstance(item, dict)]
    oracle_ids = [item.get("id") for item in oracle_items if isinstance(item, dict)]
    if (len(case_ids) != len(case_items) or len(oracle_ids) != len(oracle_items)
            or any(not isinstance(case_id, str) or not case_id for case_id in case_ids + oracle_ids)):
        return errors + ["casos/oracles devem ser objetos com id textual"]
    if len(set(case_ids)) != len(case_ids) or len(set(oracle_ids)) != len(oracle_ids):
        errors.append("id duplicado")
    if set(case_ids) != set(oracle_ids):
        errors.append("cada caso precisa de exatamente um oracle correspondente")

    domains = set()
    for item in case_items:
        if not isinstance(item, dict):
            continue
        domains.add(item.get("domain"))
        if item.get("mode") not in {"conversation", "snippet"}:
            errors.append(f"{item.get('id')}: modo inválido")
        if any(not isinstance(item.get(field), str) or not item[field].strip()
               for field in ("id", "domain", "prompt", "evidence")):
            errors.append(f"{item.get('id')}: dados de entrada incompletos")

    required_domains = {
        "java", "python", "unity", "data", "terraform", "security", "workflow",
        "api", "database", "distributed", "performance", "release",
    }
    if not required_domains.issubset(domains):
        missing_domains = sorted(required_domains - domains)
        errors.append(f"casos não cobrem as áreas mínimas: {', '.join(missing_domains)}")

    for item in oracle_items:
        if not isinstance(item, dict):
            continue
        for field in ("expected", "forbidden"):
            values = item.get(field)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                errors.append(f"{item.get('id')}: {field} inválido")

    scorecard = root / "evals/scorecard.csv"
    required_scorecard_columns = {
        "case_id", "condition", "agent", "model", "skill_commit", "access", "run_date",
        "classificacao", "aceite", "risco", "causa", "experimento", "fronteira",
        "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade",
        "escopo", "violacoes", "observacoes",
    }
    try:
        with scorecard.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
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
    print("Estrutura modular da skill e casos de avaliação válidos.")
