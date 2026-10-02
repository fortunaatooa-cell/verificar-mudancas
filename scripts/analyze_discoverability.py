#!/usr/bin/env python3
"""Analyze the separate discoverability experiment (D2)."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_bool(raw: str) -> bool:
    return str(raw).strip().lower() in {"true", "1", "yes", "sim"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    results = read_csv(root / "results.csv")
    rows = [row for row in results if row.get("condition") == "skill_installed_unprompted"]
    if not rows:
        raise SystemExit("nenhuma execução skill_installed_unprompted encontrada")

    by_case = defaultdict(list)
    for row in rows:
        by_case[row["case_id"]].append(row)

    output = []
    for case_id in sorted(by_case):
        case_rows = by_case[case_id]
        discovered = sum(as_bool(row.get("discovered", "")) for row in case_rows)
        output.append({
            "case_id": case_id,
            "runs": len(case_rows),
            "successful": sum(row.get("status") == "success" for row in case_rows),
            "discovered": discovered,
            "discovery_rate": f"{discovered / len(case_rows):.6f}",
        })

    total = len(rows)
    total_discovered = sum(as_bool(row.get("discovered", "")) for row in rows)
    output.append({
        "case_id": "__overall__",
        "runs": total,
        "successful": sum(row.get("status") == "success" for row in rows),
        "discovered": total_discovered,
        "discovery_rate": f"{total_discovered / total:.6f}",
    })

    out = Path(args.out).resolve() if args.out else REPO_ROOT / "evals/ab/discoverability.csv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["case_id", "runs", "successful", "discovered", "discovery_rate"]
        )
        writer.writeheader()
        writer.writerows(output)
    print(out)


if __name__ == "__main__":
    main()
