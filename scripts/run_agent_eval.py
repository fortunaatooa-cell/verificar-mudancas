#!/usr/bin/env python3
"""Run isolated A/B agent evaluations with Codex CLI."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from prepare_ab_eval import DEFAULT_SEED, prepare

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_RELATIVE = Path(".agents/skills/verificar-mudancas")
REQUIRED_CODEX_FLAGS = {
    "--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox",
    "--skip-git-repo-check", "--output-last-message", "--json",
}
SCORE_FIELDS = [
    "classificacao", "aceite", "risco", "causa", "experimento", "fronteira",
    "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade", "escopo",
]


def run_capture(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL, check=False,
    )


def git_head() -> str:
    result = run_capture(["git", "rev-parse", "HEAD"], REPO_ROOT)
    if result.returncode != 0:
        raise RuntimeError("não foi possível identificar o commit da skill")
    return result.stdout.strip()


def ensure_skill_clean() -> None:
    result = run_capture(["git", "status", "--porcelain", "--", str(SKILL_RELATIVE)], REPO_ROOT)
    if result.returncode != 0:
        raise RuntimeError("não foi possível verificar o estado da skill")
    if result.stdout.strip():
        raise RuntimeError("a skill possui alterações locais; commit/stash antes do benchmark para fixar a versão")


def global_skill_paths() -> list[Path]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", str(home / ".codex")))
    candidates = [
        home / ".agents" / "skills" / "verificar-mudancas",
        codex_home / "skills" / "verificar-mudancas",
    ]
    return [path for path in candidates if path.exists()]


def command_prefix(raw: str) -> list[str]:
    parts = shlex.split(raw, posix=os.name != "nt")
    if not parts:
        raise RuntimeError("--codex-bin vazio")
    if shutil.which(parts[0]) is None and not Path(parts[0]).exists():
        raise RuntimeError(f"executável não encontrado: {parts[0]}")
    return parts


def codex_preflight(prefix: list[str]) -> str:
    version = run_capture(prefix + ["--version"])
    if version.returncode != 0:
        raise RuntimeError("falha ao executar Codex: " + version.stderr.strip())
    help_result = run_capture(prefix + ["exec", "--help"])
    if help_result.returncode != 0:
        raise RuntimeError("falha ao consultar `codex exec --help`")
    help_text = help_result.stdout + "\n" + help_result.stderr
    missing = sorted(flag for flag in REQUIRED_CODEX_FLAGS if flag not in help_text)
    if missing:
        raise RuntimeError("versão do Codex não expõe flags exigidas para isolamento: " + ", ".join(missing))
    return (version.stdout or version.stderr).strip()


def build_prompt(row: dict[str, str]) -> str:
    treatment = ""
    if row["condition"] == "with_skill":
        treatment = (
            "Use a skill `verificar-mudancas` disponível neste workspace como método de investigação. "
            "Consulte os arquivos dela que forem pertinentes.\n\n"
        )
    return (
        "Você está respondendo a um caso isolado de engenharia de software. "
        "Use apenas o enunciado e a evidência abaixo como contexto específico do sistema. "
        "Não procure arquivos de avaliação, oracle ou respostas esperadas. "
        "Documentação externa pode ser consultada somente se a ferramenta permitir e se for tecnicamente necessária. "
        "Não mencione benchmark, braço ou condição experimental na resposta.\n\n"
        f"{treatment}"
        f"## Problema\n{row['prompt']}\n\n"
        f"## Evidência disponível\n{row['evidence']}\n\n"
        "Entregue um diagnóstico ou próximo passo útil, distinguindo o que está provado do que ainda é hipótese."
    )


def copy_treatment_skill(workspace: Path) -> None:
    source = REPO_ROOT / SKILL_RELATIVE
    if not source.is_dir():
        raise RuntimeError(f"skill ausente em {source}")
    target = workspace / SKILL_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)


def response_sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def parse_jsonl_metrics(path: Path) -> tuple[dict[str, int], int]:
    usage: dict[str, int] = {}
    tool_calls = 0
    if not path.is_file():
        return usage, tool_calls
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "item.completed":
            item_type = (event.get("item") or {}).get("type")
            if item_type not in {None, "agent_message", "reasoning"}:
                tool_calls += 1
        candidate = event.get("usage")
        if isinstance(candidate, dict):
            for key in ("input_tokens", "output_tokens", "total_tokens"):
                if isinstance(candidate.get(key), int):
                    usage[key] = candidate[key]
    return usage, tool_calls


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def create_grading_sheet(out: Path, operator_rows: list[dict[str, str]]) -> None:
    grading_path = out / "grading.csv"
    existing: dict[str, dict[str, str]] = {}
    if grading_path.is_file():
        existing = {row["blind_id"]: row for row in read_csv(grading_path)}

    rows = []
    for row in operator_rows:
        blind_id = row["blind_id"]
        response = out / "responses" / f"{blind_id}.md"
        metadata_path = out / "operator_logs" / f"{blind_id}.json"
        status = "missing"
        if metadata_path.is_file():
            try:
                status = json.loads(metadata_path.read_text(encoding="utf-8")).get("status", "missing")
            except json.JSONDecodeError:
                status = "invalid-metadata"
        previous = existing.get(blind_id, {})
        grading = {
            "blind_id": blind_id,
            "case_id": row["case_id"],
            "repetition": row["repetition"],
            "response_file": str(response.relative_to(out)) if response.exists() else "",
            "status": status,
        }
        grading.update({field: previous.get(field, "") for field in SCORE_FIELDS})
        grading["violacoes"] = previous.get("violacoes", "")
        grading["observacoes"] = previous.get("observacoes", "")
        rows.append(grading)
    write_csv(
        grading_path, rows,
        ["blind_id", "case_id", "repetition", "response_file", "status", *SCORE_FIELDS, "violacoes", "observacoes"],
    )


def execute_one(
    prefix: list[str], row: dict[str, str], out: Path, model: str,
    reasoning_effort: str, web_search: str, timeout_seconds: int, keep_workspace: bool,
) -> dict[str, Any]:
    blind_id = row["blind_id"]
    responses = out / "responses"
    logs = out / "operator_logs"
    responses.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    response_path = responses / f"{blind_id}.md"
    events_path = logs / f"{blind_id}.jsonl"
    stderr_path = logs / f"{blind_id}.stderr.log"
    metadata_path = logs / f"{blind_id}.json"

    workspace = Path(tempfile.mkdtemp(prefix=f"verificar-ab-{blind_id}-"))
    if row["condition"] == "with_skill":
        copy_treatment_skill(workspace)

    command = prefix + [
        "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--sandbox", "read-only", "--skip-git-repo-check", "--json",
        "--output-last-message", str(response_path.resolve()), "--model", model,
        "--cd", str(workspace.resolve()),
        "--config", f'model_reasoning_effort="{reasoning_effort}"',
        "--config", f'web_search="{web_search}"',
        build_prompt(row),
    ]

    started = time.monotonic()
    timed_out = False
    exit_code: int | None = None
    try:
        with events_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
            completed = subprocess.run(
                command, cwd=workspace, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                text=True, timeout=timeout_seconds, check=False, env={**os.environ, "NO_COLOR": "1"},
            )
            exit_code = completed.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
    elapsed = round(time.monotonic() - started, 3)

    response_text = response_path.read_text(encoding="utf-8", errors="replace") if response_path.is_file() else ""
    has_response = bool(response_text.strip())
    status = "success" if exit_code == 0 and not timed_out and has_response else "failed"
    usage, tool_calls = parse_jsonl_metrics(events_path)
    metadata: dict[str, Any] = {
        "blind_id": blind_id,
        "case_id": row["case_id"],
        "condition": row["condition"],
        "repetition": int(row["repetition"]),
        "status": status,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "elapsed_seconds": elapsed,
        "response_chars": len(response_text),
        "response_sha256": response_sha256(response_path),
        "tool_calls": tool_calls,
        "token_usage": usage,
        "workspace_had_skill": (workspace / SKILL_RELATIVE).is_dir(),
    }
    if keep_workspace:
        metadata["workspace"] = str(workspace)
    else:
        shutil.rmtree(workspace, ignore_errors=True)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def experiment_signature(
    skill_commit: str, codex_version: str, model: str, reasoning_effort: str,
    web_search: str, seed: int, rows: list[dict[str, str]], allow_contamination: bool,
) -> dict[str, Any]:
    return {
        "skill_commit": skill_commit,
        "codex_version": codex_version,
        "model": model,
        "reasoning_effort": reasoning_effort,
        "web_search": web_search,
        "sandbox": "read-only",
        "ephemeral": True,
        "ignore_user_config": True,
        "ignore_rules": True,
        "seed": seed,
        "run_count": len(rows),
        "blind_ids": sorted(row["blind_id"] for row in rows),
        "global_skill_contamination_allowed": allow_contamination,
    }


def verify_resume(existing: dict[str, Any], current: dict[str, Any]) -> None:
    keys = [
        "skill_commit", "codex_version", "model", "reasoning_effort", "web_search", "sandbox",
        "ephemeral", "ignore_user_config", "ignore_rules", "seed", "run_count", "blind_ids",
        "global_skill_contamination_allowed",
    ]
    differences = [key for key in keys if existing.get(key) != current.get(key)]
    if differences:
        raise RuntimeError(
            "--resume recusado porque a configuração mudou: " + ", ".join(differences)
            + ". Use o mesmo comando/configuração ou inicie outro diretório."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o A/B da verificar-mudancas em sessões Codex isoladas.")
    parser.add_argument("--out", required=True, help="Diretório de resultados; deve ficar fora do versionamento.")
    parser.add_argument("--model", required=True, help="Modelo Codex fixado para os dois braços.")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--web-search", choices=("live", "disabled"), default="live")
    parser.add_argument("--codex-bin", default="codex", help="Executável/comando Codex. Útil para teste com adapter fake.")
    parser.add_argument("--cases", default=str(REPO_ROOT / "evals/cases.json"))
    parser.add_argument("--case-id", action="append", dest="case_ids")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--resume", action="store_true", help="Pula execuções já concluídas com sucesso.")
    parser.add_argument("--keep-workspaces", action="store_true", help="Somente para depuração; pode revelar a condição.")
    parser.add_argument("--allow-global-skill-contamination", action="store_true")
    args = parser.parse_args()

    if args.timeout_seconds < 1:
        raise SystemExit("--timeout-seconds deve ser >= 1")
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()) and not args.resume:
        raise SystemExit(f"diretório de saída não está vazio: {out}; use --resume ou outro diretório")
    out.mkdir(parents=True, exist_ok=True)

    try:
        ensure_skill_clean()
        skill_commit = git_head()
        contamination = global_skill_paths()
        if contamination and not args.allow_global_skill_contamination:
            formatted = "\n".join(f"- {path}" for path in contamination)
            raise RuntimeError(
                "baseline contaminado: existe verificar-mudancas em escopo global. "
                "Remova/mova temporariamente antes do benchmark:\n" + formatted
            )
        prefix = command_prefix(args.codex_bin)
        codex_version = codex_preflight(prefix)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    operator_path = out / "operator.csv"
    if operator_path.exists() and args.resume:
        rows = read_csv(operator_path)
    else:
        try:
            prepare(Path(args.cases), out, case_ids=args.case_ids, repetitions=args.repetitions, seed=args.seed)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        rows = read_csv(operator_path)

    signature = experiment_signature(
        skill_commit, codex_version, args.model, args.reasoning_effort, args.web_search,
        args.seed, rows, args.allow_global_skill_contamination,
    )
    experiment_path = out / "experiment.json"
    if args.resume and experiment_path.is_file():
        try:
            existing = json.loads(experiment_path.read_text(encoding="utf-8"))
            verify_resume(existing, signature)
        except (json.JSONDecodeError, RuntimeError) as exc:
            raise SystemExit(str(exc)) from exc
        experiment = existing
    else:
        experiment = {"created_at": datetime.now(timezone.utc).isoformat(), **signature}
        experiment_path.write_text(json.dumps(experiment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    run_rows: list[dict[str, Any]] = []
    failures = 0
    for index, row in enumerate(rows, start=1):
        metadata_path = out / "operator_logs" / f"{row['blind_id']}.json"
        if args.resume and metadata_path.is_file():
            try:
                previous = json.loads(metadata_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                previous = {}
            if previous.get("status") == "success":
                print(f"[{index}/{len(rows)}] {row['blind_id']} já concluído; pulando")
                run_rows.append(previous)
                continue

        print(f"[{index}/{len(rows)}] executando {row['blind_id']} ({row['case_id']})")
        metadata = execute_one(
            prefix, row, out, args.model, args.reasoning_effort, args.web_search,
            args.timeout_seconds, args.keep_workspaces,
        )
        run_rows.append(metadata)
        if metadata["status"] != "success":
            failures += 1
            print(f"  FALHOU: exit={metadata['exit_code']} timeout={metadata['timed_out']}", file=sys.stderr)

    result_fields = [
        "blind_id", "case_id", "condition", "repetition", "status", "exit_code", "timed_out",
        "elapsed_seconds", "response_chars", "response_sha256", "tool_calls",
    ]
    write_csv(
        out / "results.csv",
        [{key: item.get(key, "") for key in result_fields} for item in run_rows],
        result_fields,
    )
    create_grading_sheet(out, rows)

    statuses = Counter(item.get("status") for item in run_rows)
    summary = {
        "total": len(run_rows),
        "success": statuses.get("success", 0),
        "failed": statuses.get("failed", 0),
        "by_condition": {
            condition: dict(Counter(item.get("status") for item in run_rows if item.get("condition") == condition))
            for condition in ("baseline", "with_skill")
        },
    }
    (out / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Resultados: {out}")
    print(f"Sucesso: {summary['success']}/{summary['total']}")
    print("Entregue `grading.csv` + `responses/` ao avaliador; não entregue `operator.csv`.")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
