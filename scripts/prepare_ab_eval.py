#!/usr/bin/env python3
"""Prepare blinded A/B manifests; does not invoke any model."""

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path

DEFAULT_CASES = [
    "runtime-port-binding",
    "external-contract-required",
    "local-evidence-sufficient",
    "java-404",
]


def blind_id(seed: int, case_id: str, condition: str, repetition: int) -> str:
    raw = f"{seed}:{case_id}:{condition}:{repetition}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="evals/cases.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260928)
    parser.add_argument("--case-id", action="append", dest="case_ids")
    args = parser.parse_args()

    if args.repetitions < 1:
        raise SystemExit("--repetitions deve ser >= 1")

    payload = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    cases = {item["id"]: item for item in payload["cases"]}
    selected = args.case_ids or DEFAULT_CASES
    missing = [case_id for case_id in selected if case_id not in cases]
    if missing:
        raise SystemExit("casos ausentes: " + ", ".join(missing))

    rows = []
    for case_id in selected:
        for repetition in range(1, args.repetitions + 1):
            for condition in ("baseline", "with_skill"):
                item = cases[case_id]
                bid = blind_id(args.seed, case_id, condition, repetition)
                rows.append({
                    "blind_id": bid,
                    "case_id": case_id,
                    "condition": condition,
                    "repetition": repetition,
                    "prompt": item["prompt"],
                    "evidence": item["evidence"],
                })

    random.Random(args.seed).shuffle(rows)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with (out / "operator.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["blind_id", "case_id", "condition", "repetition", "prompt", "evidence"])
        writer.writeheader(); writer.writerows(rows)

    with (out / "evaluator.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["blind_id", "case_id", "repetition"])
        writer.writeheader()
        writer.writerows({k: row[k] for k in ("blind_id", "case_id", "repetition")} for row in rows)

    print(f"{len(rows)} execuções preparadas em {out}")


if __name__ == "__main__":
    main()
