#!/usr/bin/env python3
"""Resolve adapter capabilities conservatively for the current workspace."""

import argparse
import json
import os
import shutil
from pathlib import Path

BOOLEAN_ENV = {"web":"VM_CAP_WEB","subagents":"VM_CAP_SUBAGENTS","hooks":"VM_CAP_HOOKS","persistent_memory":"VM_CAP_MEMORY"}


def _env_bool(name):
    value = os.getenv(name) if name else None
    if value is None:
        return None
    return value.strip().lower() in {"1","true","yes","on"}


def detect(root: Path, adapter_dir: Path):
    manifest = json.loads((adapter_dir / "adapter.json").read_text(encoding="utf-8"))
    resolved = {}
    for name, declared in manifest["capabilities"].items():
        if declared in {"native","emulated","unsupported"}:
            resolved[name] = declared
        elif name == "repository_read":
            resolved[name] = "available" if root.exists() and os.access(root, os.R_OK) else "unavailable"
        elif name == "repository_write":
            resolved[name] = "available" if root.exists() and os.access(root, os.W_OK) else "unavailable"
        elif name == "shell":
            resolved[name] = "available" if shutil.which("git") or shutil.which("python3") else "unknown"
        else:
            value = _env_bool(BOOLEAN_ENV.get(name))
            resolved[name] = "available" if value is True else ("unavailable" if value is False else "unknown")
    return {"adapter":manifest["adapter"],"declared":manifest["capabilities"],"resolved":resolved,"fallback":"Use staged roles/portable scripts whenever a runtime-detect capability is unknown or unavailable."}


def _find_adapter(root: Path, adapter: str):
    installed = root / ".verificar-mudancas/adapter"
    if (installed / "adapter.json").is_file():
        return installed
    repository = Path(__file__).resolve().parents[1] / "adapters" / adapter
    if (repository / "adapter.json").is_file():
        return repository
    raise FileNotFoundError(f"manifest do adapter não encontrado: {adapter}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", choices=("generic","codex","claude","devin","copilot"), default="generic")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    result = detect(root, _find_adapter(root, args.adapter))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
