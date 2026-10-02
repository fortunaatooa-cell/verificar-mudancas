#!/usr/bin/env python3
"""Smoke tests for efficacy and discoverability with fake Codex."""

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


def run(command: list[str]) -> None:
    completed = subprocess.run(
        command, cwd=REPO_ROOT, text=True, capture_output=True, check=False
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stdout + "\n" + completed.stderr)


def main() -> None:
    fake = REPO_ROOT / "evals/ab/fake_codex.py"
    with tempfile.TemporaryDirectory(prefix="verificar-ab-test-") as tmp:
        root = Path(tmp)

        out = root / "efficacy"
        run([
            sys.executable, str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out", str(out),
            "--model", "fake-model",
            "--reasoning-effort", "medium",
            "--web-search", "disabled",
            "--case-id", "local-evidence-sufficient",
            "--repetitions", "1",
            "--timeout-seconds", "30",
            "--codex-bin", f"{sys.executable} {fake}",
            "--allow-global-skill-contamination",
            "--smoke-test",
        ])

        operator = read_csv(out / "operator.csv")
        condition = {row["blind_id"]: row["condition"] for row in operator}
        results = read_csv(out / "results.csv")
        treatment = next(row for row in results if row["condition"] == "with_skill")
        assert treatment["treatment_observed"].lower() == "true"
        assert treatment["status"] == "success"

        grading = read_csv(out / "grading.csv")
        for row in grading:
            score = "2" if condition[row["blind_id"]] == "with_skill" else "1"
            for field in SCORE_FIELDS:
                row[field] = score
            row["violacoes"] = "0"
            row["regressao_critica"] = "false"
        write_csv(out / "grading.csv", grading)

        run([
            sys.executable, str(REPO_ROOT / "scripts/analyze_ab_results.py"),
            "--run-dir", str(out),
        ])
        comparison = json.loads((out / "comparison.json").read_text(encoding="utf-8"))
        assert comparison["with_skill_wins"] == 1
        assert comparison["treatment_not_observed_excluded"] == 0
        assert comparison["effect_minimum_sha256"]
        assert comparison["efficacy_claim_allowed"] is False
        assert comparison["publishable_success"] is False


        no_read = root / "no-read"
        run([
            sys.executable, str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out", str(no_read),
            "--model", "fake-no-read",
            "--reasoning-effort", "medium",
            "--web-search", "disabled",
            "--case-id", "local-evidence-sufficient",
            "--repetitions", "1",
            "--timeout-seconds", "30",
            "--codex-bin", f"{sys.executable} {fake}",
            "--allow-global-skill-contamination",
            "--smoke-test",
        ])
        nr_results = read_csv(no_read / "results.csv")
        nr_treatment = next(row for row in nr_results if row["condition"] == "with_skill")
        assert nr_treatment["status"] == "treatment_not_observed"
        nr_grading = read_csv(no_read / "grading.csv")
        for row in nr_grading:
            for field in SCORE_FIELDS:
                row[field] = "1"
            row["violacoes"] = "0"
            row["regressao_critica"] = "false"
        write_csv(no_read / "grading.csv", nr_grading)
        run([
            sys.executable, str(REPO_ROOT / "scripts/analyze_ab_results.py"),
            "--run-dir", str(no_read),
        ])
        nr_comparison = json.loads((no_read / "comparison.json").read_text(encoding="utf-8"))
        assert nr_comparison["treatment_not_observed_excluded"] == 1
        assert nr_comparison["with_skill_wins"] == 0

        failed = root / "failed"
        failed_command = [
            sys.executable, str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out", str(failed),
            "--model", "fake-fail",
            "--reasoning-effort", "medium",
            "--web-search", "disabled",
            "--case-id", "local-evidence-sufficient",
            "--repetitions", "1",
            "--timeout-seconds", "30",
            "--codex-bin", f"{sys.executable} {fake}",
            "--allow-global-skill-contamination",
            "--smoke-test",
        ]
        completed = subprocess.run(
            failed_command, cwd=REPO_ROOT, text=True, capture_output=True, check=False
        )
        assert completed.returncode == 2
        failed_results = read_csv(failed / "results.csv")
        assert len(failed_results) == 2
        assert all(row["status"] == "failed" for row in failed_results)
        failed_grading = read_csv(failed / "grading.csv")
        for row in failed_grading:
            row["violacoes"] = "0"
            row["regressao_critica"] = "false"
        write_csv(failed / "grading.csv", failed_grading)
        run([
            sys.executable, str(REPO_ROOT / "scripts/analyze_ab_results.py"),
            "--run-dir", str(failed),
        ])
        failed_comparison = json.loads((failed / "comparison.json").read_text(encoding="utf-8"))
        assert failed_comparison["failed_runs"] == 2
        assert failed_comparison["with_skill_wins"] == 0

        discovery = root / "discoverability"
        run([
            sys.executable, str(REPO_ROOT / "scripts/run_agent_eval.py"),
            "--out", str(discovery),
            "--model", "fake-model",
            "--reasoning-effort", "medium",
            "--web-search", "disabled",
            "--case-id", "local-evidence-sufficient",
            "--repetitions", "1",
            "--timeout-seconds", "30",
            "--codex-bin", f"{sys.executable} {fake}",
            "--allow-global-skill-contamination",
            "--experiment-mode", "discoverability",
            "--smoke-test",
        ])
        run([
            sys.executable, str(REPO_ROOT / "scripts/analyze_discoverability.py"),
            "--run-dir", str(discovery),
            "--out", str(discovery / "discoverability.csv"),
        ])
        drows = read_csv(discovery / "discoverability.csv")
        overall = next(row for row in drows if row["case_id"] == "__overall__")
        assert overall["discovery_rate"] == "1.000000"
        assert not (discovery / "grading.csv").exists()

        print("A/B: tratamento observado, scoring fixo e descobribilidade verificados.")


if __name__ == "__main__":
    main()
