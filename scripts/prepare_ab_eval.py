#!/usr/bin/env python3
"""Prepare blinded A/B manifests without invoking a model."""

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
DEFAULT_SEED = 20260928


def blind_id(seed: int, case_id: str, condition: str, repetition: int) -> str:
    raw = f"{seed}:{case_id}:{condition}:{repetition}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def build_rows(
    cases_path: Path,
    case_ids: list[str] | None = None,
    repetitions: int = 3,
    seed: int = DEFAULT_SEED,
) -> list[dict[str, object]]:
    if repetitions < 1:
        raise ValueError("repetitions deve ser >= 1")

    payload = json.loads(cases_path.read_text(encoding="utf-8"))
    cases = {item["id"]: item for item in payload["cases"]}
    selected = case_ids or DEFAULT_CASES
    missing = [case_id for case_id in selected if case_id not in cases]
    if missing:
        raise ValueError("casos ausentes: " + ", ".join(missing))

    rows: list[dict[str, object]] = []
    for case_id in selected:
        for repetition in range(1, repetitions + 1):
            for condition in ("baseline", "with_skill"):
                item = cases[case_id]
                rows.append({
                    "blind_id": blind_id(seed, case_id, condition, repetition),
                    "case_id": case_id,
                    "condition": condition,
                    "repetition": repetition,
                    "prompt": item["prompt"],
                    "evidence": item["evidence"],
                })

    random.Random(seed).shuffle(rows)
    return rows


def write_manifests(rows: list[dict[str, object]], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with (out / "operator.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["blind_id", "case_id", "condition", "repetition", "prompt", "evidence"],
        )
        writer.writeheader()
        writer.writerows(rows)

    with (out / "evaluator.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["blind_id", "case_id", "repetition"])
        writer.writeheader()
        writer.writerows(
            {key: row[key] for key in ("blind_id", "case_id", "repetition")}
            for row in rows
        )


def prepare(
    cases_path: Path,
    out: Path,
    case_ids: list[str] | None = None,
    repetitions: int = 3,
    seed: int = DEFAULT_SEED,
) -> list[dict[str, object]]:
    rows = build_rows(cases_path, case_ids=case_ids, repetitions=repetitions, seed=seed)
    write_manifests(rows, out)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="evals/cases.json")
    parser.add_argument("--out", required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--case-id", action="append", dest="case_ids")
    args = parser.parse_args()

    try:
        rows = prepare(
            Path(args.cases),
            Path(args.out),
            case_ids=args.case_ids,
            repetitions=args.repetitions,
            seed=args.seed,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(f"{len(rows)} execuções preparadas em {args.out}")


if __name__ == "__main__":
    main()
