#!/usr/bin/env python3
"""Validate the portable agentic v1.5 foundation."""

import json
import sys
from pathlib import Path


AGENTS = {
    "README.md",
    "investigador.md",
    "diagnosticador-runtime.md",
    "estrategista-testes.md",
    "implementador.md",
    "revisor-codigo.md",
    "revisor-seguranca.md",
    "verificador-evidencias.md",
}

COMMANDS = {
    "README.md",
    "verificar.md",
    "investigar.md",
    "corrigir.md",
    "revisar.md",
    "validar.md",
    "portao-qualidade.md",
    "aprender.md",
}

SCHEMAS = {
    "task.schema.json",
    "investigation.schema.json",
    "result.schema.json",
}

REQUIRED_AGENTIC_CASES = {
    "agentic-java-bug",
    "agentic-runtime-memory",
    "agentic-security-change",
    "agentic-investigation-only",
    "agentic-high-risk",
}


def read_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: JSON inválido ou indisponível: {exc}")
        return None


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    agents_dir = root / ".agents/agents"
    commands_dir = root / ".agents/commands"
    schemas_dir = root / "schemas"

    for filename in sorted(AGENTS):
        if not (agents_dir / filename).is_file():
            errors.append(f"agente ausente: {filename}")

    for filename in sorted(COMMANDS):
        if not (commands_dir / filename).is_file():
            errors.append(f"comando ausente: /{filename.removesuffix('.md')}")

    for filename in sorted(SCHEMAS):
        path = schemas_dir / filename
        data = read_json(path, errors)
        if data is not None:
            if not isinstance(data, dict) or data.get("type") != "object":
                errors.append(f"schema inválido: {filename}")
            if "$schema" not in data or "$id" not in data:
                errors.append(f"schema sem metadados: {filename}")

    spec = root / "docs/agentic-v1.5.md"
    if not spec.is_file():
        errors.append("spec agentic ausente: docs/agentic-v1.5.md")

    cases = read_json(root / "evals/agentic/cases.json", errors)
    oracle = read_json(root / "evals/agentic/oracle.json", errors)
    if cases is not None and oracle is not None:
        case_items = cases.get("cases") if isinstance(cases, dict) else None
        oracle_items = oracle.get("oracles") if isinstance(oracle, dict) else None
        if not isinstance(case_items, list) or not isinstance(oracle_items, list):
            errors.append("agentic: cases/oracles devem ser listas")
        else:
            case_ids = {item.get("id") for item in case_items if isinstance(item, dict)}
            oracle_ids = {item.get("id") for item in oracle_items if isinstance(item, dict)}
            if case_ids != REQUIRED_AGENTIC_CASES:
                errors.append("agentic: conjunto de casos inesperado")
            if oracle_ids != case_ids:
                errors.append("agentic: cada caso precisa de oracle correspondente")
            for item in case_items:
                if not isinstance(item, dict):
                    errors.append("agentic: caso deve ser objeto")
                    continue
                for field in ("id", "domain", "mode", "prompt", "evidence"):
                    if not isinstance(item.get(field), str) or not item[field].strip():
                        errors.append(f"agentic/{item.get('id')}: campo inválido: {field}")
            for item in oracle_items:
                if not isinstance(item, dict):
                    errors.append("agentic: oracle deve ser objeto")
                    continue
                for field in ("expected", "forbidden"):
                    values = item.get(field)
                    if not isinstance(values, list) or not values or any(
                        not isinstance(value, str) or not value.strip() for value in values
                    ):
                        errors.append(f"agentic/{item.get('id')}: {field} inválido")

    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    problems = validate(root)
    if problems:
        for problem in problems:
            print(f"ERRO: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Fundação agentic v1.5 válida: agentes, comandos, schemas e evals presentes.")
