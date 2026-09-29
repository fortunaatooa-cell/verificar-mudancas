#!/usr/bin/env python3
"""Validate the complete portable agentic system."""

import json
import sys
from pathlib import Path

AGENTS = {"README.md","investigador.md","planejador.md","arquiteto.md","diagnosticador-runtime.md","estrategista-testes.md","implementador.md","revisor-codigo.md","revisor-seguranca.md","verificador-evidencias.md","agente-aprendizado.md","analista-desenhos-tecnicos.md"}
COMMANDS = {"README.md","verificar.md","investigar.md","planejar.md","arquitetura.md","tdd.md","adr.md","corrigir.md","revisar.md","validar.md","portao-qualidade.md","aprender.md","desenho-tecnico.md"}
RULES = {"README.md","evidence-first.md","testing.md","tdd-cycle.md","architecture-decisions.md","safe-change.md","high-risk.md","regulated.md","visual-evidence.md"}
HOOKS = {"README.md","pre-edit.md","post-edit.md","pre-finish.md"}
AUX_SKILLS = {"investigar","planejamento","arquitetura","estrategia-testes","revisar-mudanca","diagnosticar-runtime","desenho-tecnico"}
SCHEMAS = {"task.schema.json","investigation.schema.json","evidence.schema.json","result.schema.json","plan.schema.json","adr.schema.json","lesson.schema.json","pattern.schema.json","incident.schema.json","project-knowledge.schema.json","capabilities.schema.json","hook-event.schema.json","quality-gate.schema.json","quality-gate-result.schema.json","run.schema.json"}
ADAPTERS = {"generic","codex","claude","devin","copilot"}
REQUIRED_CAPS = {"repository_read","repository_write","shell","web","subagents","hooks","persistent_memory","external_tools","vision_input","visual_generation"}
RUNTIME_SCRIPTS = {"run_hook.py","quality_gate.py","memory_store.py","install.py","detect_capabilities.py","record_run.py","create_regression_eval.py"}
REQUIRED_AGENTIC_CASES = {"agentic-java-bug","agentic-runtime-memory","agentic-security-change","agentic-investigation-only","agentic-high-risk","agentic-memory-not-truth","agentic-learning-sanitization","agentic-quality-gate","agentic-adapter-degradation","agentic-technical-drawing","agentic-visual-generation-fallback"}
REQUIRED_VISUAL_CASES = {"technical-drawing-no-fabricated-dimensions","technical-drawing-generation-capability","response-mode-simple"}
REQUIRED_LIFECYCLE_CASES = {"lifecycle-planning-unknowns","lifecycle-architecture-tradeoffs","lifecycle-tdd-real-red","lifecycle-tdd-false-red","lifecycle-adr-not-proof","lifecycle-architecture-drawing-crosscheck"}
CAP_VALUES = {"native","emulated","runtime-detect","unsupported"}


def read_json(path: Path, errors: list[str]):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc: errors.append(f"{path}: JSON inválido ou indisponível: {exc}"); return None


def require_files(directory: Path, names, label, errors):
    for filename in sorted(names):
        if not (directory / filename).is_file(): errors.append(f"{label} ausente: {filename}")


def validate_case_pack(cases_path, oracle_path, required_ids, label, errors):
    cases = read_json(cases_path, errors); oracle = read_json(oracle_path, errors)
    if cases is None or oracle is None: return
    case_items = cases.get("cases") if isinstance(cases, dict) else None; oracle_items = oracle.get("oracles") if isinstance(oracle, dict) else None
    if not isinstance(case_items, list) or not isinstance(oracle_items, list): errors.append(f"{label}: cases/oracles devem ser listas"); return
    case_ids = {item.get("id") for item in case_items if isinstance(item, dict)}; oracle_ids = {item.get("id") for item in oracle_items if isinstance(item, dict)}
    if case_ids != required_ids: errors.append(f"{label}: conjunto de casos inesperado")
    if oracle_ids != case_ids: errors.append(f"{label}: cada caso precisa de oracle correspondente")
    for item in case_items:
        if not isinstance(item, dict): errors.append(f"{label}: caso deve ser objeto"); continue
        for field in ("id","domain","mode","prompt","evidence"):
            if not isinstance(item.get(field), str) or not item[field].strip(): errors.append(f"{label}/{item.get('id')}: campo inválido: {field}")
    for item in oracle_items:
        if not isinstance(item, dict): errors.append(f"{label}: oracle deve ser objeto"); continue
        for field in ("expected","forbidden"):
            values = item.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values): errors.append(f"{label}/{item.get('id')}: {field} inválido")


def validate(root: Path) -> list[str]:
    errors = []
    require_files(root / ".agents/agents", AGENTS, "agente", errors); require_files(root / ".agents/commands", COMMANDS, "comando", errors); require_files(root / ".agents/rules", RULES, "regra", errors); require_files(root / ".agents/hooks", HOOKS, "hook", errors); require_files(root / "scripts", RUNTIME_SCRIPTS, "script runtime", errors)
    for skill in AUX_SKILLS:
        if not (root / ".agents/skills" / skill / "SKILL.md").is_file(): errors.append(f"skill auxiliar ausente: {skill}")
    for filename in sorted(SCHEMAS):
        data = read_json(root / "schemas" / filename, errors)
        if data is None: continue
        if not isinstance(data, dict) or data.get("type") != "object": errors.append(f"schema inválido: {filename}")
        if "$schema" not in data or "$id" not in data: errors.append(f"schema sem metadados: {filename}")
    for adapter in sorted(ADAPTERS):
        directory = root / "adapters" / adapter
        if not (directory / "README.md").is_file(): errors.append(f"adapter sem README: {adapter}")
        data = read_json(directory / "adapter.json", errors)
        if data is None: continue
        if data.get("adapter") != adapter or data.get("version") != 1: errors.append(f"adapter inválido: {adapter}")
        capabilities = data.get("capabilities")
        if not isinstance(capabilities, dict) or not capabilities: errors.append(f"adapter sem capabilities: {adapter}")
        else:
            if set(capabilities) != REQUIRED_CAPS: errors.append(f"adapter com conjunto de capabilities inválido: {adapter}")
            if any(value not in CAP_VALUES for value in capabilities.values()): errors.append(f"adapter com capability inválida: {adapter}")
        if data.get("command_strategy") not in {"native","staged-prompts","portable-files"}: errors.append(f"adapter com command_strategy inválida: {adapter}")
    for relative in ("memory/README.md","memory/index/index.json","docs/agentic-system.md","docs/spec-v3-1-engineering-lifecycle.md","docs/installation.md","quality-gate.repo.json","AGENTS.md","evals/regression/README.md","evals/visual/README.md","evals/lifecycle/README.md"):
        if not (root / relative).is_file(): errors.append(f"componente agentic ausente: {relative}")
    for folder in ("memory/lessons","memory/patterns","memory/incidents","memory/project","evals/regression/generated"):
        if not (root / folder).is_dir(): errors.append(f"diretório agentic ausente: {folder}")
    qg = read_json(root / "quality-gate.repo.json", errors)
    if qg is not None and (qg.get("version") != 1 or not isinstance(qg.get("checks"), list)): errors.append("quality-gate.repo.json inválido")
    validate_case_pack(root / "evals/agentic/cases.json", root / "evals/agentic/oracle.json", REQUIRED_AGENTIC_CASES, "agentic", errors)
    validate_case_pack(root / "evals/visual/cases.json", root / "evals/visual/oracle.json", REQUIRED_VISUAL_CASES, "visual", errors)
    validate_case_pack(root / "evals/lifecycle/cases.json", root / "evals/lifecycle/oracle.json", REQUIRED_LIFECYCLE_CASES, "lifecycle", errors)
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]; problems = validate(root)
    if problems:
        for problem in problems: print(f"ERRO: {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Sistema agentic completo válido: planejamento, arquitetura, TDD, ADR, desenho técnico, agentes, skills, comandos, regras, memória, adapters, schemas e evals presentes.")
