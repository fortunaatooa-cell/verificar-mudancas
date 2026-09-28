#!/usr/bin/env python3
"""Portable hook runner for verificar-mudancas."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

EVENTS = {"pre-edit", "post-edit", "pre-finish"}
HIGH_RISK = {"HIGH", "CRITICAL"}


def _load_payload(args):
    if args.payload:
        return json.loads(args.payload)
    if args.payload_file:
        return json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        return json.loads(raw) if raw else {}
    return {}


def _status(event, block, messages, incomplete=False, details=None):
    if block:
        status = "VERIFICATION_INCOMPLETE" if incomplete else "BLOCKED"
    elif messages:
        status = "WARN"
    else:
        status = "PASS"
    return {"event": event, "status": status, "block": block, "messages": messages, "details": details or {}}


def pre_edit(payload):
    risk = str(payload.get("risk", "LOW")).upper()
    messages = []
    block = False
    if payload.get("mode") == "investigation-only":
        messages.append("Modo somente investigação não permite edição.")
        block = True
    acceptance = payload.get("acceptance") or []
    if not acceptance:
        messages.append("Critérios observáveis de aceite não informados.")
        block = block or risk in HIGH_RISK
    if not (payload.get("hypothesis") or payload.get("evidence")):
        messages.append("Edição sem hipótese ou evidência material registrada.")
        block = block or risk in HIGH_RISK
    if risk in HIGH_RISK:
        if payload.get("environment_identified") is not True:
            messages.append("HIGH/CRITICAL exige alvo/ambiente identificado.")
            block = True
        if payload.get("destructive") and not payload.get("recovery_plan"):
            messages.append("Ação destrutiva HIGH/CRITICAL exige rollback ou roll-forward.")
            block = True
        if payload.get("human_approval_required") and payload.get("human_approved") is not True:
            messages.append("Aprovação humana requerida ainda não registrada.")
            block = True
    return _status("pre-edit", block, messages, details={"risk": risk})


def _git_changed_files(root):
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB"],
            cwd=root, text=True, capture_output=True, timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _boundaries(files):
    found = set()
    for name in files:
        lower = name.lower()
        if any(x in lower for x in ("controller", "api", "openapi", "route")):
            found.add("api/contrato")
        if any(x in lower for x in ("terraform", ".tf", "dockerfile", "k8s", "helm")):
            found.add("infra/runtime")
        if any(x in lower for x in ("migration", "schema", "repository", "sql")):
            found.add("dados/persistência")
        if any(x in lower for x in ("auth", "security", "iam", "secret")):
            found.add("segurança")
        if any(x in lower for x in ("test", "spec")):
            found.add("testes")
    return sorted(found)


def post_edit(payload, root):
    files = payload.get("changed_files") or _git_changed_files(root)
    boundaries = _boundaries(files)
    messages = []
    if not files:
        messages.append("Nenhum arquivo alterado foi informado ou detectado.")
    if boundaries:
        messages.append("Revalidar fronteiras afetadas: " + ", ".join(boundaries) + ".")
    return _status("post-edit", False, messages, details={"changed_files": files, "boundaries": boundaries})


def pre_finish(payload):
    risk = str(payload.get("risk", "LOW")).upper()
    messages = []
    block = False
    claims = payload.get("claims") or []
    for claim in claims:
        if isinstance(claim, str):
            messages.append(f"Claim sem evidência estruturada: {claim}")
            block = True
        elif isinstance(claim, dict) and not (claim.get("evidence") or []):
            messages.append(f"Claim sem evidência: {claim.get('text', '<sem texto>')}")
            block = True
    if payload.get("material_change") and payload.get("verified_after_last_change") is not True:
        messages.append("Mudança material não foi verificada após a última alteração.")
        block = True
    if risk in HIGH_RISK:
        controls = payload.get("high_risk_controls") or {}
        for field in ("blast_radius", "recovery", "stop_conditions", "success_signals"):
            if not controls.get(field):
                messages.append(f"HIGH/CRITICAL sem controle obrigatório: {field}.")
                block = True
    return _status("pre-finish", block, messages, incomplete=block, details={"risk": risk})


def evaluate(event, payload, root):
    if event == "pre-edit":
        return pre_edit(payload)
    if event == "post-edit":
        return post_edit(payload, root)
    if event == "pre-finish":
        return pre_finish(payload)
    raise ValueError(f"evento desconhecido: {event}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=sorted(EVENTS))
    parser.add_argument("--payload")
    parser.add_argument("--payload-file")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    try:
        payload = _load_payload(args)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": f"payload inválido: {exc}"}, ensure_ascii=False))
        raise SystemExit(2)
    result = evaluate(args.event, payload, Path(args.root).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(3 if result["block"] else 0)


if __name__ == "__main__":
    main()
