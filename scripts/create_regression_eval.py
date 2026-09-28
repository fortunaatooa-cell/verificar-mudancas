#!/usr/bin/env python3
"""Create a reviewable regression-eval bundle from sanitized memory."""

import argparse
import json
import re
from pathlib import Path

try:
    from scripts.memory_store import privacy_errors
except ModuleNotFoundError:
    from memory_store import privacy_errors


def build_bundle(source_doc, case_id, prompt, expected, forbidden):
    errors = privacy_errors(source_doc)
    if errors:
        raise ValueError("fonte de memória não sanitizada: " + "; ".join(errors))
    if not expected or not forbidden:
        raise ValueError("expected e forbidden precisam de ao menos um item")
    evidence_items = source_doc.get("useful_evidence") or source_doc.get("evidence") or source_doc.get("verification") or []
    evidence = " | ".join(str(item) for item in evidence_items) if evidence_items else "Memória sanitizada disponível; revalidar no caso atual."
    return {
        "version": 1,
        "status": "REVIEW_REQUIRED",
        "source_memory_id": source_doc.get("id"),
        "case": {"id": case_id, "domain": "regression", "mode": "conversation", "prompt": prompt, "evidence": evidence},
        "oracle": {"id": case_id, "expected": expected, "forbidden": forbidden},
    }


def create(source: Path, out_dir: Path, case_id: str, prompt: str, expected, forbidden):
    doc = json.loads(source.read_text(encoding="utf-8"))
    bundle = build_bundle(doc, case_id, prompt, expected, forbidden)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", case_id).strip("-.")
    if not safe:
        raise ValueError("id de caso inválido")
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"{safe}.json"
    if output.exists():
        raise FileExistsError(f"regressão já existe: {output}")
    output.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--expected", action="append", required=True)
    parser.add_argument("--forbidden", action="append", required=True)
    parser.add_argument("--out-dir", default="evals/regression/generated")
    args = parser.parse_args()
    try:
        print(create(Path(args.source), Path(args.out_dir), args.id, args.prompt, args.expected, args.forbidden))
    except (OSError, ValueError) as exc:
        print(f"ERRO: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
