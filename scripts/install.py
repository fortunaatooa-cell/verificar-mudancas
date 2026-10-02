#!/usr/bin/env python3
"""Install verificar-mudancas portable assets into another workspace."""

import argparse
import json
import shutil
from pathlib import Path

try:
    from .claude_native import install_native as install_claude_native
except ImportError:
    from claude_native import install_native as install_claude_native

ADAPTERS = {"generic", "codex", "claude", "devin", "copilot"}
RUNTIME_SCRIPTS = ("run_hook.py", "quality_gate.py", "memory_store.py", "detect_capabilities.py", "record_run.py", "create_regression_eval.py", "claude_hook_bridge.py")
AUXILIARY_SKILLS = ("investigar", "planejamento", "arquitetura", "estrategia-testes", "revisar-mudanca", "diagnosticar-runtime", "desenho-tecnico")


def _copy(source: Path, destination: Path, force: bool, dry_run: bool, operations: list):
    if destination.exists() and not force:
        operations.append({"path": str(destination), "status": "skipped-existing"}); return
    operations.append({"path": str(destination), "status": "planned" if dry_run else "written"})
    if dry_run: return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        if destination.exists(): shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else: shutil.copy2(source, destination)


def install(source_root: Path, target: Path, adapter: str, mode: str, force=False, dry_run=False):
    if adapter not in ADAPTERS: raise ValueError(f"adapter desconhecido: {adapter}")
    operations = []
    _copy(source_root / ".agents/skills/verificar-mudancas", target / ".agents/skills/verificar-mudancas", force, dry_run, operations)
    if adapter == "claude" and mode == "skill":
        install_claude_native(source_root, target, mode=mode, force=force, dry_run=dry_run, operations=operations)
    if mode == "full":
        for auxiliary in AUXILIARY_SKILLS:
            _copy(source_root / ".agents/skills" / auxiliary, target / ".agents/skills" / auxiliary, force, dry_run, operations)
        for folder in ("agents", "commands", "rules", "hooks"):
            _copy(source_root / ".agents" / folder, target / ".agents" / folder, force, dry_run, operations)
        _copy(source_root / "AGENTS.md", target / "AGENTS.md", force, dry_run, operations)
        _copy(source_root / "schemas", target / ".verificar-mudancas/schemas", force, dry_run, operations)
        for script in RUNTIME_SCRIPTS:
            _copy(source_root / "scripts" / script, target / ".verificar-mudancas/scripts" / script, force, dry_run, operations)
        _copy(source_root / "adapters" / adapter, target / ".verificar-mudancas/adapter", force, dry_run, operations)
        if adapter == "claude":
            install_claude_native(source_root, target, mode=mode, force=force, dry_run=dry_run, operations=operations)
        if not dry_run:
            for folder in ("lessons", "patterns", "incidents", "project", "index"):
                (target / "memory" / folder).mkdir(parents=True, exist_ok=True)
            index = target / "memory/index/index.json"
            if force or not index.exists(): index.write_text('{"version":1,"entries":[]}\n', encoding="utf-8")
            info = target / ".verificar-mudancas/installation.json"; info.parent.mkdir(parents=True, exist_ok=True)
            info.write_text(json.dumps({"version":1,"adapter":adapter,"mode":mode}, indent=2) + "\n", encoding="utf-8")
    return operations


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--target", required=True); parser.add_argument("--adapter", choices=sorted(ADAPTERS), default="generic"); parser.add_argument("--mode", choices=("skill", "full"), default="full"); parser.add_argument("--force", action="store_true"); parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(); source_root = Path(__file__).resolve().parents[1]; target = Path(args.target).resolve(); target.mkdir(parents=True, exist_ok=True)
    operations = install(source_root, target, args.adapter, args.mode, args.force, args.dry_run)
    print(json.dumps({"adapter":args.adapter,"mode":args.mode,"target":str(target),"operations":operations}, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
