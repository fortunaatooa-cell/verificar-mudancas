#!/usr/bin/env python3
"""Smoke test for the executable A/B runner using fake Codex."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="verificar-ab-test-") as tmp:
        out = Path(tmp) / "run"
        fake = REPO_ROOT / "evals/ab/fake_codex.py"
        command = [
            sys.executable,
            str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out",
            str(out),
            "--model",
            "fake-model",
            "--reasoning-effort",
            "medium",
            "--web-search",
            "disabled",
            "--case-id",
            "local-evidence-sufficient",
            "--repetitions",
            "1",
            "--timeout-seconds",
            "30",
            "--codex-bin",
            f"{sys.executable} {fake}",
            "--allow-global-skill-contamination",
        ]
        completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + "\n" + completed.stderr)

        operator = read_csv(out / "operator.csv")
        assert len(operator) == 2
        condition = {row["blind_id"]: row["condition"] for row in operator}
        observed = {}
        for blind_id, arm in condition.items():
            response = (out / "responses" / f"{blind_id}.md").read_text(encoding="utf-8").strip()
            observed[arm] = response
        assert observed == {
            "baseline": "skill_present=false",
            "with_skill": "skill_present=true",
        }, observed

        results = read_csv(out / "results.csv")
        assert len(results) == 2
        assert all(row["status"] == "success" for row in results)
        assert {row["condition"] for row in results} == {"baseline", "with_skill"}

        grading_header = set(read_csv(out / "grading.csv")[0])
        assert "condition" not in grading_header
        experiment = json.loads((out / "experiment.json").read_text(encoding="utf-8"))
        assert experiment["run_count"] == 2
        assert experiment["model"] == "fake-model"
        print("A/B runner: baseline sem skill e treatment com skill isolados corretamente.")


if __name__ == "__main__":
    main()
