#!/usr/bin/env python3
"""Tiny fake Codex CLI used only to test runner isolation in CI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HELP = """
--ephemeral
--ignore-user-config
--ignore-rules
--sandbox
--skip-git-repo-check
--output-last-message
--json
--model
--cd
--config
""".strip()


def value_after(args: list[str], flag: str) -> str:
    try:
        return args[args.index(flag) + 1]
    except (ValueError, IndexError) as exc:
        raise SystemExit(f"flag ausente no fake codex: {flag}") from exc


def main() -> None:
    args = sys.argv[1:]
    if args == ["--version"]:
        print("codex-cli fake-1.0")
        return
    if args[:2] == ["exec", "--help"]:
        print(HELP)
        return
    if not args or args[0] != "exec":
        raise SystemExit("fake codex aceita apenas --version ou exec")

    output = Path(value_after(args, "--output-last-message"))
    cwd = Path(value_after(args, "--cd"))
    skill = cwd / ".agents" / "skills" / "verificar-mudancas" / "SKILL.md"
    present = skill.is_file()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"skill_present={'true' if present else 'false'}\n", encoding="utf-8")

    print(json.dumps({"type": "item.completed", "item": {"type": "agent_message"}}))
    print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}}))


if __name__ == "__main__":
    main()
