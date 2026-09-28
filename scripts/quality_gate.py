#!/usr/bin/env python3
"""Conservative, configurable quality gate."""

import argparse
import json
import shlex
import subprocess
from pathlib import Path


def detect_candidates(root: Path):
    candidates = []
    if (root / "pom.xml").is_file():
        exe = "./mvnw" if (root / "mvnw").is_file() else "mvn"
        candidates.append({"name": "testes-maven", "command": [exe, "test"], "required": True, "source": "detected"})
    if (root / "build.gradle").is_file() or (root / "build.gradle.kts").is_file():
        exe = "./gradlew" if (root / "gradlew").is_file() else "gradle"
        candidates.append({"name": "testes-gradle", "command": [exe, "test"], "required": True, "source": "detected"})
    if (root / "package.json").is_file():
        candidates.append({"name": "testes-node", "command": ["npm", "test", "--", "--runInBand"], "required": True, "source": "detected"})
    if (root / "tests").is_dir() and not any(item["name"].startswith("testes-") for item in candidates):
        candidates.append({"name": "testes-python", "command": ["python3", "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], "required": True, "source": "detected"})
    return candidates


def load_config(root: Path, config_path=None):
    if config_path:
        path = Path(config_path)
        if not path.is_absolute():
            path = root / path
        data = json.loads(path.read_text(encoding="utf-8"))
        checks = data.get("checks", [])
        if not isinstance(checks, list):
            raise ValueError("checks deve ser lista")
        return checks, str(path)
    default = root / ".verificar-mudancas/quality-gate.json"
    if default.is_file():
        data = json.loads(default.read_text(encoding="utf-8"))
        checks = data.get("checks", [])
        if not isinstance(checks, list):
            raise ValueError("checks deve ser lista")
        return checks, str(default)
    return detect_candidates(root), "auto-detectado"


def _run_check(root, check):
    command = check.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x for x in command):
        return {"name": check.get("name", "sem-nome"), "status": "FAIL", "reason": "comando inválido"}
    timeout = int(check.get("timeout_seconds", 300))
    try:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "name": check.get("name", " ".join(command)),
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "required": bool(check.get("required", True)),
            "command": command,
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-4000:],
            "stderr_tail": result.stderr[-4000:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"name": check.get("name", " ".join(command)), "status": "FAIL", "required": bool(check.get("required", True)), "command": command, "reason": str(exc)}


def run_gate(root: Path, checks, execute=False):
    if not checks:
        return {"overall": "N/A", "executed": False, "checks": [], "message": "Nenhum check configurado ou detectado."}
    if not execute:
        return {
            "overall": "PARTIAL",
            "executed": False,
            "checks": [{"name": c.get("name", "sem-nome"), "status": "PLANNED", "command": c.get("command"), "required": bool(c.get("required", True))} for c in checks],
            "message": "Plano gerado. Use --execute somente após autorizar os comandos listados.",
        }
    results = [_run_check(root, check) for check in checks]
    required_fail = any(r.get("required", True) and r["status"] != "PASS" for r in results)
    overall = "FAIL" if required_fail else ("PASS" if all(r["status"] == "PASS" for r in results) else "PARTIAL")
    return {"overall": overall, "executed": True, "checks": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--config")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        checks, source = load_config(root, args.config)
        result = run_gate(root, checks, args.execute)
        result["source"] = source
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"overall": "BLOCKED", "executed": False, "checks": [], "error": str(exc)}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    raise SystemExit(1 if result["overall"] in {"FAIL", "BLOCKED"} else 0)


if __name__ == "__main__":
    main()
