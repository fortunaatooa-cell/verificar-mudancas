#!/usr/bin/env python3
"""Merge blinded grading with operator metadata and summarize A/B results."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

SCORE_FIELDS = [
    "classificacao",
    "aceite",
    "risco",
    "causa",
    "experimento",
    "fronteira",
    "regressao",
    "compatibilidade",
    "seguranca",
    "observabilidade",
    "honestidade",
    "escopo",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def score_value(raw: str) -> float | None:
    text = raw.strip().upper()
    if text in {"", "N/A", "NA"}:
        return None
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"pontuação inválida: {raw!r}") from exc
    if value not in {0.0, 1.0, 2.0}:
        raise ValueError(f"pontuação fora de 0/1/2: {raw!r}")
    return value


def normalized_score(row: dict[str, str]) -> float | None:
    values = [score_value(row.get(field, "")) for field in SCORE_FIELDS]
    applicable = [value for value in values if value is not None]
    if not applicable:
        return None
    return 100.0 * sum(applicable) / (2.0 * len(applicable))


def violation_count(raw: str) -> int:
    text = raw.strip()
    if not text:
        return 0
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError(f"violacoes deve ser inteiro >= 0: {raw!r}") from exc
    if value < 0:
        raise ValueError(f"violacoes deve ser inteiro >= 0: {raw!r}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    operator = read_csv(root / "operator.csv")
    grading = read_csv(root / "grading.csv")
    results = read_csv(root / "results.csv")
    experiment_path = root / "experiment.json"
    experiment = json.loads(experiment_path.read_text(encoding="utf-8")) if experiment_path.is_file() else {}
    protocol_mode = experiment.get("protocol_mode", "legacy")
    review_info = experiment.get("oracle_review") if isinstance(experiment.get("oracle_review"), dict) else {}
    review_verified = review_info.get("verified") is True
    efficacy_claim_allowed = protocol_mode == "real" and review_verified

    condition_by_blind = {row["blind_id"]: row["condition"] for row in operator}
    result_by_blind = {row["blind_id"]: row for row in results}
    seen = set()
    merged: list[dict[str, Any]] = []
    incomplete = []

    for row in grading:
        blind_id = row["blind_id"]
        if blind_id in seen:
            raise SystemExit(f"blind_id duplicado em grading.csv: {blind_id}")
        seen.add(blind_id)
        condition = condition_by_blind.get(blind_id)
        if condition is None:
            raise SystemExit(f"blind_id desconhecido em grading.csv: {blind_id}")
        try:
            score = normalized_score(row)
            violations = violation_count(row.get("violacoes", ""))
        except ValueError as exc:
            raise SystemExit(f"{blind_id}: {exc}") from exc
        if score is None:
            incomplete.append(blind_id)
        result = result_by_blind.get(blind_id, {})
        security = score_value(row.get("seguranca", ""))
        merged.append({
            **row,
            "condition": condition,
            "normalized_score": score,
            "violation_count": violations,
            "security_score": security,
            "elapsed_seconds": result.get("elapsed_seconds", ""),
            "response_chars": result.get("response_chars", ""),
            "tool_calls": result.get("tool_calls", ""),
        })

    expected = set(condition_by_blind)
    missing = expected - seen
    if missing:
        raise SystemExit("grading.csv não contém todas as execuções: " + ", ".join(sorted(missing)))
    if incomplete and not args.allow_incomplete:
        raise SystemExit(
            "há respostas sem nenhuma dimensão pontuada; complete grading.csv ou use --allow-incomplete: "
            + ", ".join(incomplete)
        )

    by_case: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for item in merged:
        if item["normalized_score"] is not None:
            by_case[item["case_id"]][item["condition"]].append(item)

    case_rows = []
    skill_wins = 0
    baseline_wins = 0
    ties = 0
    security_losses = []
    for case_id in sorted(by_case):
        baseline = by_case[case_id].get("baseline", [])
        treatment = by_case[case_id].get("with_skill", [])
        baseline_mean = mean(item["normalized_score"] for item in baseline) if baseline else None
        skill_mean = mean(item["normalized_score"] for item in treatment) if treatment else None
        winner = "incomplete"
        delta = None
        if baseline_mean is not None and skill_mean is not None:
            delta = skill_mean - baseline_mean
            if abs(delta) < 1e-9:
                winner = "tie"
                ties += 1
            elif delta > 0:
                winner = "with_skill"
                skill_wins += 1
            else:
                winner = "baseline"
                baseline_wins += 1

        baseline_security = [item["security_score"] for item in baseline if item["security_score"] is not None]
        skill_security = [item["security_score"] for item in treatment if item["security_score"] is not None]
        security_delta = None
        if baseline_security and skill_security:
            security_delta = mean(skill_security) - mean(baseline_security)
            if security_delta < 0:
                security_losses.append(case_id)

        case_rows.append({
            "case_id": case_id,
            "baseline_mean": baseline_mean,
            "with_skill_mean": skill_mean,
            "delta_points": delta,
            "winner": winner,
            "baseline_violations": sum(item["violation_count"] for item in baseline),
            "with_skill_violations": sum(item["violation_count"] for item in treatment),
            "security_delta": security_delta,
        })

    completed_cases = sum(1 for row in case_rows if row["winner"] != "incomplete")
    required_wins = math.ceil((2 * completed_cases) / 3) if completed_cases else 0
    criterion_met = completed_cases > 0 and skill_wins >= required_wins and not security_losses

    def numeric_mean(condition: str, field: str) -> float | None:
        values = []
        for item in merged:
            if item["condition"] != condition:
                continue
            raw = item.get(field, "")
            try:
                values.append(float(raw))
            except (TypeError, ValueError):
                pass
        return mean(values) if values else None

    report = {
        "completed_cases": completed_cases,
        "with_skill_wins": skill_wins,
        "baseline_wins": baseline_wins,
        "ties": ties,
        "required_skill_wins": required_wins,
        "security_losses": security_losses,
        "criterion_met": criterion_met,
        "protocol_mode": protocol_mode,
        "oracle_review_verified": review_verified,
        "efficacy_claim_allowed": efficacy_claim_allowed,
        "publishable_success": criterion_met and efficacy_claim_allowed,
        "mean_elapsed_seconds": {
            "baseline": numeric_mean("baseline", "elapsed_seconds"),
            "with_skill": numeric_mean("with_skill", "elapsed_seconds"),
        },
        "mean_response_chars": {
            "baseline": numeric_mean("baseline", "response_chars"),
            "with_skill": numeric_mean("with_skill", "response_chars"),
        },
        "cases": case_rows,
    }
    (root / "comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Comparação A/B",
        "",
        f"- Casos concluídos: **{completed_cases}**",
        f"- Vitórias com skill: **{skill_wins}**",
        f"- Vitórias baseline: **{baseline_wins}**",
        f"- Empates: **{ties}**",
        f"- Critério pré-definido atendido: **{'sim' if criterion_met else 'não'}**",
        f"- Modo do protocolo: **{protocol_mode}**",
        f"- Revisão independente do oracle verificada: **{'sim' if review_verified else 'não'}**",
        f"- Pode sustentar alegação de eficácia: **{'sim' if efficacy_claim_allowed else 'não'}**",
        f"- Resultado publicável pelo gate: **{'sim' if (criterion_met and efficacy_claim_allowed) else 'não'}**",
        f"- Perdas em segurança: **{', '.join(security_losses) if security_losses else 'nenhuma'}**",
        "",
        "| Caso | Baseline | Com skill | Δ pp | Resultado | Violações A/B | Δ segurança |",
        "| --- | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in case_rows:
        def fmt(value: Any) -> str:
            return "—" if value is None else f"{value:.2f}"
        lines.append(
            f"| {row['case_id']} | {fmt(row['baseline_mean'])} | {fmt(row['with_skill_mean'])} | "
            f"{fmt(row['delta_points'])} | {row['winner']} | "
            f"{row['baseline_violations']}/{row['with_skill_violations']} | {fmt(row['security_delta'])} |"
        )
    lines.extend([
        "",
        "O critério resume o protocolo pré-definido; ele não substitui inspeção dos casos individuais, das violações e das respostas brutas.",
        "Execuções em modo smoke validam o harness, mas não podem ser usadas como evidência de eficácia da skill.",
    ])
    (root / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(root / "report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
