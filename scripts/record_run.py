#!/usr/bin/env python3
"""Write an explicitly sanitized local run record."""

import argparse
import json
import re
from pathlib import Path

try:
    from scripts.memory_store import privacy_errors
except ModuleNotFoundError:
    from memory_store import privacy_errors


def validate_run(doc):
    errors = []
    required = {"run_id","task_type","risk","selected_agents","selected_references","selected_playbooks","tools_used","verification","final_status","privacy"}
    missing = required - set(doc) if isinstance(doc, dict) else required
    if missing:
        errors.append("campos ausentes: " + ", ".join(sorted(missing)))
    if isinstance(doc, dict):
        fake_memory = {"id": doc.get("run_id", "run"), "kind": "incident", "privacy": doc.get("privacy", {})}
        for key, value in doc.items():
            if key not in fake_memory:
                fake_memory[key] = value
        errors.extend(privacy_errors(fake_memory))
    return errors


def record(root: Path, source: Path):
    doc = json.loads(source.read_text(encoding="utf-8"))
    errors = validate_run(doc)
    if errors:
        raise ValueError("; ".join(errors))
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", doc["run_id"]).strip("-.")
    out = root / ".verificar-mudancas/runs" / f"{safe}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(f"run já registrado: {out}")
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    try:
        print(record(Path(args.root).resolve(), Path(args.file).resolve()))
    except (OSError, ValueError) as exc:
        print(f"ERRO: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
