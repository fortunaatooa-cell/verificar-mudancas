#!/usr/bin/env python3
"""Gate a regulated pilot on six recorded restriction answers and security approval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "ferramenta_aprovada",
    "propriedade_material",
    "dados",
    "segregacao_funcoes",
    "busca_externa",
    "confirmacao_ibm",
}


def check(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    questions = payload.get("questions", [])
    by_id = {q.get("id"): q for q in questions if isinstance(q, dict)}
    if set(by_id) != REQUIRED:
        errors.append("as seis perguntas de restrição devem existir exatamente uma vez")
    for qid in sorted(REQUIRED):
        item = by_id.get(qid, {})
        if str(item.get("answer", "")).strip().lower() in {"", "pending", "pendente"}:
            errors.append(f"{qid}: resposta pendente")
        for field in ("evidence", "responded_by", "responded_at"):
            if not str(item.get(field, "")).strip():
                errors.append(f"{qid}: {field} ausente")
    approval = payload.get("security_approval", {})
    if approval.get("status") != "approved":
        errors.append("security_approval.status deve ser approved")
    for field in ("evidence", "approved_by", "approved_at"):
        if not str(approval.get(field, "")).strip():
            errors.append(f"security_approval.{field} ausente")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="docs/bank-pilot-restrictions.json")
    args = parser.parse_args()
    errors = check(Path(args.file))
    if errors:
        for error in errors:
            print("BLOQUEADO:", error)
        raise SystemExit(1)
    print("Pré-requisitos documentais do piloto atendidos.")


if __name__ == "__main__":
    main()
