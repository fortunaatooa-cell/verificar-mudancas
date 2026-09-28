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
SCORE_FIELDS = [
    "classificacao", "aceite", "risco", "causa", "experimento", "fronteira",
    "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade", "escopo",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="verificar-ab-test-") as tmp:
        out = Path(tmp) / "run"
        fake = REPO_ROOT / "evals/ab/fake_codex.py"
        command = [
            sys.executable,
            str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out", str(out),
            "--model", "fake-model",
            "--reasoning-effort", "medium",
            "--web-search", "disabled",
            "--case-id", "local-evidence-sufficient",
            "--repetitions", "1",
            "--timeout-seconds", "30",
            "--codex-bin", f"{sys.executable} {fake}",
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

        grading = read_csv(out / "grading.csv")
        assert grading and "condition" not in grading[0]
        for row in grading:
            score = "2" if condition[row["blind_id"]] == "with_skill" else "1"
            for field in SCORE_FIELDS:
                row[field] = score
            row["violacoes"] = "0"
        write_csv(out / "grading.csv", grading)

        analyzed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts/analyze_ab_results.py"), "--run-dir", str(out)],
            cwd=REPO_ROOT, text=True, capture_output=True, check=False,
        )
        if analyzed.returncode != 0:
            raise AssertionError(analyzed.stdout + "\n" + analyzed.stderr)
        comparison = json.loads((out / "comparison.json").read_text(encoding="utf-8"))
        assert comparison["with_skill_wins"] == 1
        assert comparison["baseline_wins"] == 0
        assert comparison["criterion_met"] is True
        assert (out / "report.md").is_file()

        experiment = json.loads((out / "experiment.json").read_text(encoding="utf-8"))
        assert experiment["run_count"] == 2
        assert experiment["model"] == "fake-model"
        print("A/B runner: isolamento, cegamento e reconciliação pós-avaliação verificados.")


if __name__ == "__main__":
    main()
