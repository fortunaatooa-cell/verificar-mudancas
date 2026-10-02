#!/usr/bin/env python3
"""Analyze blinded efficacy results with fixed dimensions and frozen thresholds."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

try:
    from .eval_protocol import canonical_sha256
except ImportError:
    from eval_protocol import canonical_sha256

SCORE_FIELDS = [
    "classificacao", "aceite", "risco", "causa", "experimento", "fronteira",
    "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade", "escopo",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def score_value(raw: str | None) -> float | None:
    text = (raw or "").strip().upper()
    if text in {"", "N/A", "NA"}:
        return None
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"pontuação inválida: {raw!r}") from exc
    if value not in {0.0, 1.0, 2.0}:
        raise ValueError(f"pontuação fora de 0/1/2: {raw!r}")
    return value


def normalized_score(row: dict[str, str], applicable_dimensions: list[str]) -> tuple[float, list[str]]:
    if not applicable_dimensions:
        raise ValueError("caso sem applicable_dimensions")
    missing: list[str] = []
    total = 0.0
    for field in applicable_dimensions:
        value = score_value(row.get(field, ""))
        if value is None:
            missing.append(field)
            value = 0.0
        total += value
    return total / (2.0 * len(applicable_dimensions)), missing


def violation_count(raw: str | None) -> int:
    text = (raw or "").strip()
    if not text:
        return 0
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError(f"violacoes deve ser inteiro >= 0: {raw!r}") from exc
    if value < 0:
        raise ValueError(f"violacoes deve ser inteiro >= 0: {raw!r}")
    return value


def bool_value(raw: str | bool | None) -> bool:
    if isinstance(raw, bool):
        return raw
    text = str(raw or "").strip().lower()
    if text in {"", "false", "0", "no", "não", "nao"}:
        return False
    if text in {"true", "1", "yes", "sim"}:
        return True
    raise ValueError(f"booleano inválido: {raw!r}")


def determine_winner(
    delta_score: float,
    effect_minimum: float,
    baseline_violations: int,
    with_skill_violations: int,
    critical_regression: bool,
) -> str:
    if (
        delta_score >= effect_minimum
        and with_skill_violations <= baseline_violations
        and not critical_regression
    ):
        return "with_skill"
    if (
        delta_score <= -effect_minimum
        or with_skill_violations > baseline_violations
        or critical_regression
    ):
        return "baseline"
    return "tie"


def load_oracle(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload["oracles"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    operator = read_csv(root / "operator.csv")
    grading = read_csv(root / "grading.csv")
    results = read_csv(root / "results.csv")
    experiment = json.loads((root / "experiment.json").read_text(encoding="utf-8"))

    if experiment.get("experiment_mode", "efficacy") != "efficacy":
        raise SystemExit("este analisador aceita somente experiment_mode=efficacy")

    oracle_path = root / "oracle.snapshot.json"
    effect_path = root / "effect-minimum.snapshot.json"
    if not oracle_path.is_file() or not effect_path.is_file():
        raise SystemExit("snapshots de oracle/effect-minimum ausentes; rodada não é reproduzível")
    if canonical_sha256(oracle_path) != experiment.get("oracle_sha256"):
        raise SystemExit("hash do oracle snapshot diverge do experimento")
    if canonical_sha256(effect_path) != experiment.get("effect_minimum_sha256"):
        raise SystemExit("hash do efeito mínimo diverge do experimento")

    oracle = load_oracle(oracle_path)
    effect = json.loads(effect_path.read_text(encoding="utf-8"))
    thresholds = effect.get("dimensions", {})
    if not isinstance(thresholds, dict):
        raise SystemExit("effect-minimum inválido")

    grading_by_blind = {row["blind_id"]: row for row in grading}
    result_by_blind = {row["blind_id"]: row for row in results}
    if len(grading_by_blind) != len(grading):
        raise SystemExit("blind_id duplicado em grading.csv")
    if len(result_by_blind) != len(results):
        raise SystemExit("blind_id duplicado em results.csv")

    merged: list[dict[str, Any]] = []
    incomplete: list[str] = []
    excluded = 0
    failed_runs = 0

    for op in operator:
        blind_id = op["blind_id"]
        case_id = op["case_id"]
        condition = op["condition"]
        result = result_by_blind.get(blind_id) or {"status": "failed"}
        status = result.get("status", "failed")

        if condition == "with_skill" and status == "treatment_not_observed":
            excluded += 1
            merged.append({
                "blind_id": blind_id,
                "case_id": case_id,
                "condition": condition,
                "status": status,
                "excluded": True,
            })
            continue

        oracle_item = oracle.get(case_id)
        if oracle_item is None:
            raise SystemExit(f"oracle ausente para {case_id}")
        dims = oracle_item.get("applicable_dimensions", [])
        unknown = [dim for dim in dims if dim not in SCORE_FIELDS]
        if unknown:
            raise SystemExit(f"{case_id}: dimensões inválidas: {', '.join(unknown)}")
        missing_threshold = [dim for dim in dims if dim not in thresholds]
        if missing_threshold:
            raise SystemExit(f"{case_id}: efeito mínimo ausente para: {', '.join(missing_threshold)}")

        grading_row = grading_by_blind.get(blind_id, {})
        if status == "failed":
            score = 0.0
            missing_dims: list[str] = []
            failed_runs += 1
        else:
            try:
                score, missing_dims = normalized_score(grading_row, dims)
            except ValueError as exc:
                raise SystemExit(f"{blind_id}: {exc}") from exc
            if missing_dims:
                incomplete.append(f"{blind_id}({','.join(missing_dims)})")

        try:
            violations = violation_count(grading_row.get("violacoes"))
            critical = bool_value(grading_row.get("regressao_critica"))
        except ValueError as exc:
            raise SystemExit(f"{blind_id}: {exc}") from exc

        security = None
        if "seguranca" in dims and status != "failed":
            security = score_value(grading_row.get("seguranca"))

        merged.append({
            **grading_row,
            "blind_id": blind_id,
            "case_id": case_id,
            "condition": condition,
            "status": status,
            "excluded": False,
            "normalized_score": score,
            "violation_count": violations,
            "critical_regression": critical,
            "security_score": security,
            "applicable_dimensions": dims,
            "elapsed_seconds": result.get("elapsed_seconds", ""),
            "response_chars": result.get("response_chars", ""),
            "tool_calls": result.get("tool_calls", ""),
        })

    if incomplete and not args.allow_incomplete:
        raise SystemExit(
            "há dimensões aplicáveis sem pontuação; complete grading.csv ou use --allow-incomplete: "
            + ", ".join(incomplete)
        )

    by_case: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    exclusions_by_case: dict[str, int] = defaultdict(int)
    for item in merged:
        if item.get("excluded"):
            exclusions_by_case[item["case_id"]] += 1
        else:
            by_case[item["case_id"]][item["condition"]].append(item)

    case_rows = []
    skill_wins = 0
    baseline_wins = 0
    ties = 0
    security_losses = []

    for case_id in sorted({row["case_id"] for row in operator}):
        baseline = by_case[case_id].get("baseline", [])
        treatment = by_case[case_id].get("with_skill", [])
        dims = oracle[case_id]["applicable_dimensions"]
        effect_minimum = mean(float(thresholds[dim]) for dim in dims)

        baseline_mean = mean(item["normalized_score"] for item in baseline) if baseline else None
        skill_mean = mean(item["normalized_score"] for item in treatment) if treatment else None
        baseline_violations = sum(item["violation_count"] for item in baseline)
        skill_violations = sum(item["violation_count"] for item in treatment)
        critical = any(item["critical_regression"] for item in treatment)

        winner = "incomplete"
        delta = None
        if baseline_mean is not None and skill_mean is not None:
            delta = skill_mean - baseline_mean
            winner = determine_winner(
                delta, effect_minimum, baseline_violations, skill_violations, critical
            )
            if winner == "with_skill":
                skill_wins += 1
            elif winner == "baseline":
                baseline_wins += 1
            else:
                ties += 1

        baseline_security = [item["security_score"] for item in baseline if item.get("security_score") is not None]
        skill_security = [item["security_score"] for item in treatment if item.get("security_score") is not None]
        security_delta = None
        if baseline_security and skill_security:
            security_delta = mean(skill_security) - mean(baseline_security)
            if security_delta < 0:
                security_losses.append(case_id)

        case_rows.append({
            "case_id": case_id,
            "applicable_dimensions": dims,
            "effect_minimum": effect_minimum,
            "baseline_mean": baseline_mean,
            "with_skill_mean": skill_mean,
            "delta_score": delta,
            "winner": winner,
            "baseline_violations": baseline_violations,
            "with_skill_violations": skill_violations,
            "critical_regression": critical,
            "failed_baseline": sum(item["status"] == "failed" for item in baseline),
            "failed_with_skill": sum(item["status"] == "failed" for item in treatment),
            "treatment_not_observed_excluded": exclusions_by_case[case_id],
            "security_delta": security_delta,
        })

    completed_cases = sum(row["winner"] != "incomplete" for row in case_rows)
    required_wins = math.ceil((2 * completed_cases) / 3) if completed_cases else 0
    criterion_met = completed_cases > 0 and skill_wins >= required_wins and not security_losses

    protocol_mode = experiment.get("protocol_mode", "legacy")
    review = experiment.get("oracle_review") if isinstance(experiment.get("oracle_review"), dict) else {}
    review_verified = review.get("verified") is True
    efficacy_claim_allowed = protocol_mode == "real" and review_verified

    def numeric_mean(condition: str, field: str) -> float | None:
        values = []
        for item in merged:
            if item.get("excluded") or item.get("condition") != condition:
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
        "failed_runs": failed_runs,
        "treatment_not_observed_excluded": excluded,
        "security_losses": security_losses,
        "criterion_met": criterion_met,
        "protocol_mode": protocol_mode,
        "oracle_review_verified": review_verified,
        "efficacy_claim_allowed": efficacy_claim_allowed,
        "publishable_success": criterion_met and efficacy_claim_allowed,
        "effect_minimum_sha256": experiment.get("effect_minimum_sha256"),
        "oracle_sha256": experiment.get("oracle_sha256"),
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
    (root / "comparison.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def fmt(value: Any) -> str:
        return "—" if value is None else f"{value:.3f}"

    lines = [
        "# Comparação A/B",
        "",
        f"- Casos concluídos: **{completed_cases}**",
        f"- Vitórias com skill: **{skill_wins}**",
        f"- Vitórias baseline: **{baseline_wins}**",
        f"- Empates: **{ties}**",
        f"- Falhas registradas como não-vitória: **{failed_runs}**",
        f"- Execuções excluídas: skill não lida: **{excluded}**",
        f"- Hash do efeito mínimo: {experiment.get('effect_minimum_sha256')}",
        f"- Critério pré-definido atendido: **{'sim' if criterion_met else 'não'}**",
        f"- Revisão independente verificada: **{'sim' if review_verified else 'não'}**",
        f"- Resultado publicável: **{'sim' if (criterion_met and efficacy_claim_allowed) else 'não'}**",
        "",
        "| Caso | Baseline | Com skill | Delta | Efeito mín. | Resultado | Violações A/B | Regr. crítica | Excluídas |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: |",
    ]
    for row in case_rows:
        lines.append(
            f"| {row['case_id']} | {fmt(row['baseline_mean'])} | {fmt(row['with_skill_mean'])} | "
            f"{fmt(row['delta_score'])} | {fmt(row['effect_minimum'])} | {row['winner']} | "
            f"{row['baseline_violations']}/{row['with_skill_violations']} | "
            f"{'sim' if row['critical_regression'] else 'não'} | "
            f"{row['treatment_not_observed_excluded']} |"
        )
    lines.extend([
        "",
        "Dimensões aplicáveis vêm do oracle congelado e são iguais nos dois braços.",
        "N/A em dimensão aplicável não altera o denominador.",
        "Falhas recebem score 0 e permanecem no cálculo.",
        "treatment_not_observed é excluído e reportado.",
        "Smoke test valida o harness, não eficácia.",
    ])
    (root / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(root / "report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
