#!/usr/bin/env python3
"""Claude Code hook bridge for verificar-mudancas.

The bridge keeps native hooks deterministic and small. It blocks only two
high-confidence situations by default:
- Edit/Write while VM_MODE=investigation-only.
- Known destructive Bash commands without VM_HUMAN_APPROVED=true.

Everything else remains advisory and is handled by the portable methodology.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DESTRUCTIVE_PATTERNS = (
    (re.compile(r"(?i)(?:^|\s)rm\s+-[^\n]*r[^\n]*f\b"), "rm recursivo/forçado"),
    (re.compile(r"(?i)\bgit\s+push\b[^\n]*(?:--force|-f)\b"), "git push forçado"),
    (re.compile(r"(?i)\bgit\s+reset\s+--hard\b"), "git reset --hard"),
    (re.compile(r"(?i)\bgit\s+clean\b[^\n]*-[^\n]*f"), "git clean forçado"),
    (re.compile(r"(?i)\bterraform\s+destroy\b"), "terraform destroy"),
    (re.compile(r"(?i)\bkubectl\s+delete\b"), "kubectl delete"),
    (re.compile(r"(?i)\bDROP\s+(?:TABLE|DATABASE|SCHEMA)\b"), "DDL destrutivo"),
)


def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _tool_name(payload: dict[str, Any]) -> str:
    return str(payload.get("tool_name") or payload.get("tool") or "")


def _tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("tool_input")
    return value if isinstance(value, dict) else {}


def pre_tool(payload: dict[str, Any]) -> tuple[bool, str]:
    tool = _tool_name(payload)
    if os.getenv("VM_MODE", "").strip().lower() == "investigation-only" and tool in {"Write", "Edit"}:
        return True, "verificar-mudancas: modo investigation-only bloqueia Write/Edit."

    if tool == "Bash":
        command = str(_tool_input(payload).get("command") or "")
        for pattern, label in DESTRUCTIVE_PATTERNS:
            if pattern.search(command):
                if _truthy("VM_HUMAN_APPROVED"):
                    return False, f"verificar-mudancas: {label} autorizado por VM_HUMAN_APPROVED=true."
                return (
                    True,
                    "verificar-mudancas: ação destrutiva detectada "
                    f"({label}). Exige aprovação humana explícita; defina VM_HUMAN_APPROVED=true "
                    "somente após revisar alvo, blast radius e recuperação.",
                )
    return False, ""


def session_start(root: Path) -> str:
    branch = ""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    suffix = f" Branch atual: {branch}." if branch else ""
    return (
        "verificar-mudancas ativo para Claude Code. "
        "Use as skills em .claude/skills e os especialistas em .claude/agents; "
        "AGENTS.md e .agents/skills/verificar-mudancas/SKILL.md são fontes canônicas."
        + suffix
    )


def post_edit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not files:
        return ""
    shown = ", ".join(files[:12])
    extra = f" (+{len(files)-12})" if len(files) > 12 else ""
    return f"verificar-mudancas: alterações detectadas: {shown}{extra}. Revalide a fronteira afetada antes de concluir."


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=("session-start", "pre-tool", "post-edit"))
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    payload = _read_payload()

    if args.event == "session-start":
        print(session_start(root))
        return

    if args.event == "pre-tool":
        block, reason = pre_tool(payload)
        if block:
            print(reason, file=sys.stderr)
            raise SystemExit(2)
        if reason:
            print(reason)
        return

    message = post_edit(root)
    if message:
        print(message)


if __name__ == "__main__":
    main()
