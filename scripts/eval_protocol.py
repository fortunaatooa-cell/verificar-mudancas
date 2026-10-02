#!/usr/bin/env python3
"""Protocol guard for real A/B evaluations.

A real efficacy run is allowed only when an independent oracle review matches
the exact case/oracle content being evaluated. Hashes normalize line endings so
LF/CRLF checkouts do not invalidate an otherwise identical review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = 1
APPROVED_STATUS = "approved"


def normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_text(path).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"arquivo de revisão indisponível: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON de revisão inválido: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("registro de revisão deve ser um objeto JSON")
    return payload


def review_template(cases_path: Path, oracle_path: Path, case_ids: list[str]) -> dict[str, Any]:
    return {
        "version": PROTOCOL_VERSION,
        "reviewer": "",
        "reviewed_at": "",
        "independent": False,
        "cases_sha256": canonical_sha256(cases_path),
        "oracle_sha256": canonical_sha256(oracle_path),
        "reviews": [
            {
                "case_id": case_id,
                "status": "pending",
                "method": "",
                "notes": "",
            }
            for case_id in case_ids
        ],
    }


def verify_review(
    review_path: Path,
    cases_path: Path,
    oracle_path: Path,
    selected_case_ids: list[str],
) -> dict[str, Any]:
    review = load_json(review_path)
    errors: list[str] = []

    if review.get("version") != PROTOCOL_VERSION:
        errors.append(f"version deve ser {PROTOCOL_VERSION}")

    reviewer = review.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append("reviewer deve identificar a segunda pessoa que revisou o gabarito")

    if review.get("independent") is not True:
        errors.append("independent deve ser true; auto-revisão não libera rodada real")

    reviewed_at = review.get("reviewed_at")
    if not isinstance(reviewed_at, str) or not reviewed_at.strip():
        errors.append("reviewed_at é obrigatório")
    else:
        try:
            parsed = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                errors.append("reviewed_at deve incluir fuso/offset")
        except ValueError:
            errors.append("reviewed_at deve ser ISO-8601 válido")

    expected_cases_hash = canonical_sha256(cases_path)
    expected_oracle_hash = canonical_sha256(oracle_path)
    if review.get("cases_sha256") != expected_cases_hash:
        errors.append("cases_sha256 não corresponde ao cases.json atual")
    if review.get("oracle_sha256") != expected_oracle_hash:
        errors.append("oracle_sha256 não corresponde ao oracle.json atual")

    review_items = review.get("reviews")
    if not isinstance(review_items, list):
        errors.append("reviews deve ser uma lista")
        review_items = []

    by_case: dict[str, dict[str, Any]] = {}
    for item in review_items:
        if not isinstance(item, dict):
            errors.append("cada item de reviews deve ser objeto")
            continue
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append("review sem case_id textual")
            continue
        if case_id in by_case:
            errors.append(f"review duplicada para {case_id}")
            continue
        by_case[case_id] = item

    missing = [case_id for case_id in selected_case_ids if case_id not in by_case]
    if missing:
        errors.append("casos sem revisão registrada: " + ", ".join(missing))

    for case_id in selected_case_ids:
        item = by_case.get(case_id)
        if not item:
            continue
        if item.get("status") != APPROVED_STATUS:
            errors.append(f"{case_id}: status deve ser approved")
        method = item.get("method")
        if not isinstance(method, str) or not method.strip():
            errors.append(f"{case_id}: method deve registrar como o oracle foi conferido")

    if errors:
        raise ValueError("revisão independente do oracle não aprovada:\n- " + "\n- ".join(errors))

    return {
        "verified": True,
        "reviewer": reviewer.strip(),
        "reviewed_at": reviewed_at,
        "cases_sha256": expected_cases_hash,
        "oracle_sha256": expected_oracle_hash,
        "review_file_sha256": canonical_sha256(review_path),
        "reviewed_case_ids": sorted(set(selected_case_ids)),
    }


def case_ids_from_cases(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", []) if isinstance(payload, dict) else []
    ids = [item.get("id") for item in cases if isinstance(item, dict)]
    if any(not isinstance(case_id, str) or not case_id for case_id in ids):
        raise ValueError("cases.json contém id inválido")
    return ids


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera/verifica o gate de revisão independente do oracle.")
    sub = parser.add_subparsers(dest="command", required=True)

    template = sub.add_parser("template", help="gera registro pendente com hashes atuais")
    template.add_argument("--cases", default="evals/cases.json")
    template.add_argument("--oracle", default="evals/oracle.json")
    template.add_argument("--out", default="evals/oracle-review.json")
    template.add_argument("--case-id", action="append", dest="case_ids")

    verify = sub.add_parser("verify", help="verifica registro de revisão contra os arquivos atuais")
    verify.add_argument("--cases", default="evals/cases.json")
    verify.add_argument("--oracle", default="evals/oracle.json")
    verify.add_argument("--review", default="evals/oracle-review.json")
    verify.add_argument("--case-id", action="append", dest="case_ids")

    args = parser.parse_args()
    cases_path = Path(args.cases).resolve()
    oracle_path = Path(args.oracle).resolve()
    selected = args.case_ids or case_ids_from_cases(cases_path)

    if args.command == "template":
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(review_template(cases_path, oracle_path, selected), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(out)
        return

    try:
        result = verify_review(Path(args.review).resolve(), cases_path, oracle_path, selected)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
