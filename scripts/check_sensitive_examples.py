#!/usr/bin/env python3
"""Fail CI on high-confidence sensitive-looking examples in public skill/eval material."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".csv", ".py", ".toml"}
PATTERNS = {
    "cpf": re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    "conta": re.compile(r"(?i)\b(?:conta|account)\s*(?:number|n[uú]mero)?\s*[:=]\s*\d{5,}(?:-\d{1,2})?\b"),
    "segredo": re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|chave)\s*[:=]\s*['\"]?[A-Za-z0-9_+/=-]{12,}"),
}
SAFE_MARKERS = ("<redacted>", "<omitido>", "<ficticio>", "<fictício>", "example.invalid")


def scan_paths(root: Path, relative_paths: list[str]) -> list[str]:
    findings: list[str] = []
    for relative in relative_paths:
        target = root / relative
        if not target.exists():
            continue
        files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
        for path in files:
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                lowered = line.lower()
                if any(marker in lowered for marker in SAFE_MARKERS):
                    continue
                for name, pattern in PATTERNS.items():
                    if pattern.search(line):
                        findings.append(f"{path.relative_to(root)}:{lineno}:{name}")
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=["evals", ".agents"])
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    findings = scan_paths(Path(args.root).resolve(), args.paths)
    if findings:
        for finding in findings:
            print("SENSÍVEL:", finding)
        raise SystemExit(1)
    print("Nenhum padrão sensível de alta confiança encontrado.")


if __name__ == "__main__":
    main()
