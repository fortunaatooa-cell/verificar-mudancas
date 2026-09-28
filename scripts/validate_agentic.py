#!/usr/bin/env python3
"""Validate the complete portable agentic system."""

import json
import sys
from pathlib import Path

AGENTS = {"README.md", "investigador.md", "diagnosticador-runtime.md", "estrategista-testes.md", "implementador.md", "revisor-codigo.md", "revisor-seguranca.md", "verificador-evidencias.md", "agente-aprendizado.md"}
COMMANDS = {"README.md", "verificar.md", "investigar.md", "corrigir.md", "revisar.md", "validar.md", "portao-qualidade.md", "aprender.md"}
RULES = {"README.md", "evidence-first.md", "testing.md", "safe-change.md", "high-risk.md", "regulated.md"}
HOOKS = {"README.md", "pre-edit.md", "post-edit.md", "pre-finish.md"}
SCHEMAS = {"task.schema.json", "investigation.schema.json", "result.schema.json", "lesson.schema.json", "pattern.schema.json", "incident.schema.json", "capabilities.schema.json", "hook-event.schema.json", "quality-gate.schema.json", "quality-gate-result.schema.json", "run.schema.json"}
ADAPTERS = {"generic", "codex", "claude", "devin", "copilot"}
RUNTIME_SCRIPTS = {"run_hook.py", "quality_gate.py", "memory_store.py", "install.py", "detect_capabilities.py", "record_run.py"}
REQUIRED_AGENTIC_CASES = {"agentic-java-bug", "agentic-runtime-memory", "agentic-security-change", "agentic-investigation-only", "agentic-high-risk", "agentic-memory-not-truth", "agentic-learning-sanitization", "agentic-quality-gate", "agentic-adapter-degradation"}
CAP_VALUES = {"native", "emulated", "runtime-detect", "unsupported"}


def read_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: JSON inválido ou indisponível: {exc}")
        return None


def require_files(directory: Path, names, label, errors):
    for filename in sorted(names):
        if not (directory / filename).is_file():
            errors.append(f"{label} ausente: {filename}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    require_files(root / ".agents/agents", AGENTS, "agente", errors)
    require_files(root / ".agents/commands", COMMANDS, "comando", errors)
    require_files(root / ".agents/rules", RULES, "regra", errors)
    require_files(root / ".agents/hooks", HOOKS, "hook", errors)
    require_files(root / "scripts", RUNTIME_SCRIPTS, "script runtime", errors)

    for filename in sorted(SCHEMAS):
        data = read_json(root / "schemas" / filename, errors)
        if data is None:
            continue
        if not isinstance(data, dict) or data.get("type") != "object":
            errors.append(f"schema inválido: {filename}")
        if "$schema" not in data or "$id" not in data:
            errors.append(f"schema sem metadados: {filename}")

    for adapter in sorted(ADAPTERS):
        directory = root / "adapters" / adapter
        if not (directory / "README.md").is_file():
            errors.append(f"adapter sem README: {adapter}")
        data = read_json(directory / "adapter.json", errors)
        if data is None:
            continue
        if data.get("adapter") != adapter or data.get("version") != 1:
            errors.append(f"adapter inválido: {adapter}")
        capabilities = data.get("capabilities")
        if not isinstance(capabilities, dict) or not capabilities:
            errors.append(f"adapter sem capabilities: {adapter}")
        elif any(value not in CAP_VALUES for value in capabilities.values()):
            errors.append(f"adapter com capability inválida: {adapter}")
        if data.get("command_strategy") not in {"native", "staged-prompts", "portable-files"}:
            errors.append(f"adapter com command_strategy inválida: {adapter}")

    for relative in ("memory/README.md", "memory/index/index.json", "docs/agentic-system.md", "docs/installation.md", "quality-gate.repo.json", "AGENTS.md"):
        if not (root / relative).is_file():
            errors.append(f"componente agentic ausente: {relative}")
    for folder in ("memory/lessons", "memory/patterns", "memory/incidents"):
        if not (root / folder).is_dir():
            errors.append(f"diretório de memória ausente: {folder}")

    qg = read_json(root / "quality-gate.repo.json", errors)
    if qg is not None and (qg.get("version") != 1 or not isinstance(qg.get("checks"), list)):
        errors.append("quality-gate.repo.json inválido")

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
                    if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values):
                        errors.append(f"agentic/{item.get('id')}: {field} inválido")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    problems = validate(root)
    if problems:
        for problem in problems:
            print(f"ERRO: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Sistema agentic completo válido: agentes, comandos, regras, hooks, memória, adapters, schemas e evals presentes.")
