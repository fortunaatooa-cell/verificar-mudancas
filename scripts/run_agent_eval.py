#!/usr/bin/env python3
"""Run isolated efficacy or discoverability evaluations with Codex CLI."""

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

try:
    from .eval_protocol import canonical_sha256, verify_review
    from .prepare_ab_eval import DEFAULT_CASES, DEFAULT_SEED, prepare
except ImportError:
    from eval_protocol import canonical_sha256, verify_review
    from prepare_ab_eval import DEFAULT_CASES, DEFAULT_SEED, prepare

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_RELATIVE = Path(".agents/skills/verificar-mudancas")
DEFAULT_EFFECT = REPO_ROOT / "evals/ab/effect-minimum.json"
REQUIRED_CODEX_FLAGS = {
    "--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox",
    "--skip-git-repo-check", "--output-last-message", "--json",
}
SCORE_FIELDS = [
    "classificacao", "aceite", "risco", "causa", "experimento", "fronteira",
    "regressao", "compatibilidade", "seguranca", "observabilidade", "honestidade", "escopo",
]
SKILL_MARKERS = (
    ".agents/skills/verificar-mudancas/skill.md",
    ".agents/skills/verificar-mudancas/references/",
)


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
        raise RuntimeError("falha ao consultar ajuda do codex exec")
    help_text = help_result.stdout + "\n" + help_result.stderr
    missing = sorted(flag for flag in REQUIRED_CODEX_FLAGS if flag not in help_text)
    if missing:
        raise RuntimeError("versão do Codex não expõe flags exigidas para isolamento: " + ", ".join(missing))
    return (version.stdout or version.stderr).strip()


def build_prompt(row: dict[str, str]) -> str:
    treatment = ""
    if row["condition"] == "with_skill":
        treatment = (
            "Use a skill verificar-mudancas disponível neste workspace como método de investigação. "
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


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child)


def detect_skill_read(jsonl_path: Path) -> bool:
    """Return True only when observable JSONL contains the skill/reference path."""
    if not jsonl_path.is_file():
        return False
    for raw in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for value in _strings(event):
            normalized = value.replace("\\", "/").lower()
            if any(marker in normalized for marker in SKILL_MARKERS):
                return True
    return False


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
        grading["regressao_critica"] = previous.get("regressao_critica", "")
        grading["observacoes"] = previous.get("observacoes", "")
        rows.append(grading)
    write_csv(
        grading_path,
        rows,
        ["blind_id", "case_id", "repetition", "response_file", "status", *SCORE_FIELDS,
         "violacoes", "regressao_critica", "observacoes"],
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
    condition = row["condition"]
    if condition in {"with_skill", "skill_installed_unprompted"}:
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
    skill_read = detect_skill_read(events_path)
    treatment_observed: bool | None = None
    discovered: bool | None = None
    if condition == "with_skill":
        treatment_observed = skill_read
        if status == "success" and not treatment_observed:
            status = "treatment_not_observed"
    elif condition == "skill_installed_unprompted":
        discovered = skill_read

    metadata: dict[str, Any] = {
        "blind_id": blind_id,
        "case_id": row["case_id"],
        "condition": condition,
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
        "treatment_observed": treatment_observed,
        "discovered": discovered,
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
    experiment_mode: str, protocol_mode: str, protocol_review: dict[str, Any],
    cases_sha256: str, oracle_sha256: str | None, effect_minimum_sha256: str | None,
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
        "experiment_mode": experiment_mode,
        "protocol_mode": protocol_mode,
        "oracle_review": protocol_review,
        "cases_sha256": cases_sha256,
        "oracle_sha256": oracle_sha256,
        "effect_minimum_sha256": effect_minimum_sha256,
    }


def verify_resume(existing: dict[str, Any], current: dict[str, Any]) -> None:
    keys = sorted(current)
    differences = [key for key in keys if existing.get(key) != current.get(key)]
    if differences:
        raise RuntimeError(
            "--resume recusado porque a configuração mudou: " + ", ".join(differences)
            + ". Use o mesmo comando/configuração ou inicie outro diretório."
        )


def snapshot(source: Path, target: Path) -> str:
    shutil.copyfile(source, target)
    return canonical_sha256(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa avaliações isoladas da verificar-mudancas.")
    parser.add_argument("--out", required=True, help="Diretório de resultados; deve ficar fora do versionamento.")
    parser.add_argument("--model", required=True, help="Modelo Codex fixado para a rodada.")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--web-search", choices=("live", "disabled"), default="live")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--cases", default=str(REPO_ROOT / "evals/cases.json"))
    parser.add_argument("--oracle", default=str(REPO_ROOT / "evals/oracle.json"))
    parser.add_argument("--effect-minimum", default=str(DEFAULT_EFFECT))
    parser.add_argument("--oracle-review", default=str(REPO_ROOT / "evals/oracle-review.json"))
    parser.add_argument("--case-id", action="append", dest="case_ids")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-workspaces", action="store_true")
    parser.add_argument("--allow-global-skill-contamination", action="store_true")
    parser.add_argument("--experiment-mode", choices=("efficacy", "discoverability"), default="efficacy")
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()

    if args.timeout_seconds < 1:
        raise SystemExit("--timeout-seconds deve ser >= 1")
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()) and not args.resume:
        raise SystemExit(f"diretório de saída não está vazio: {out}; use --resume ou outro diretório")
    out.mkdir(parents=True, exist_ok=True)

    cases_path = Path(args.cases).resolve()
    oracle_path = Path(args.oracle).resolve()
    effect_path = Path(args.effect_minimum).resolve()
    selected_case_ids = args.case_ids or DEFAULT_CASES
    cases_hash = canonical_sha256(cases_path)
    oracle_hash: str | None = None
    effect_hash: str | None = None
    protocol_review: dict[str, Any] = {"verified": False}

    if args.experiment_mode == "efficacy":
        oracle_hash = canonical_sha256(oracle_path)
        effect_hash = canonical_sha256(effect_path)
        protocol_mode = "smoke" if args.smoke_test else "real"
        if args.smoke_test:
            protocol_review = {
                "verified": False,
                "reason": "smoke-test: revisão independente não exigida; não usar como evidência de eficácia",
                "reviewed_case_ids": sorted(set(selected_case_ids)),
            }
        else:
            try:
                protocol_review = verify_review(
                    Path(args.oracle_review).resolve(), cases_path, oracle_path, selected_case_ids,
                )
            except ValueError as exc:
                raise SystemExit(
                    str(exc)
                    + "\nGere um registro com scripts/eval_protocol.py template e peça revisão a uma segunda pessoa. "
                      "Para testar somente o harness, use --smoke-test."
                ) from exc
    else:
        protocol_mode = "discoverability-smoke" if args.smoke_test else "discoverability"

    try:
        ensure_skill_clean()
        skill_commit = git_head()
        contamination = global_skill_paths()
        if contamination and not args.allow_global_skill_contamination:
            formatted = "\n".join(f"- {path}" for path in contamination)
            raise RuntimeError(
                "baseline/descobribilidade contaminados por skill global. Remova/mova temporariamente:\n" + formatted
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
            prepare(
                cases_path, out, case_ids=args.case_ids, repetitions=args.repetitions,
                seed=args.seed, mode=args.experiment_mode,
            )
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        rows = read_csv(operator_path)

    if not args.resume:
        snapshot(cases_path, out / "cases.snapshot.json")
        if args.experiment_mode == "efficacy":
            snapshot(oracle_path, out / "oracle.snapshot.json")
            snapshot(effect_path, out / "effect-minimum.snapshot.json")

    signature = experiment_signature(
        skill_commit, codex_version, args.model, args.reasoning_effort, args.web_search,
        args.seed, rows, args.allow_global_skill_contamination, args.experiment_mode,
        protocol_mode, protocol_review, cases_hash, oracle_hash, effect_hash,
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
            if previous.get("status") in {"success", "failed", "treatment_not_observed"}:
                print(f"[{index}/{len(rows)}] {row['blind_id']} já possui resultado terminal; pulando")
                run_rows.append(previous)
                continue

        print(f"[{index}/{len(rows)}] executando {row['blind_id']} ({row['case_id']})")
        metadata = execute_one(
            prefix, row, out, args.model, args.reasoning_effort, args.web_search,
            args.timeout_seconds, args.keep_workspaces,
        )
        run_rows.append(metadata)
        if metadata["status"] == "failed":
            failures += 1
            print(f"  FALHOU: exit={metadata['exit_code']} timeout={metadata['timed_out']}", file=sys.stderr)

    result_fields = [
        "blind_id", "case_id", "condition", "repetition", "status", "exit_code", "timed_out",
        "elapsed_seconds", "response_chars", "response_sha256", "tool_calls",
        "treatment_observed", "discovered",
    ]
    write_csv(
        out / "results.csv",
        [{key: item.get(key, "") for key in result_fields} for item in run_rows],
        result_fields,
    )
    if args.experiment_mode == "efficacy":
        create_grading_sheet(out, rows)

    statuses = Counter(item.get("status") for item in run_rows)
    conditions = sorted({str(item.get("condition")) for item in run_rows})
    summary = {
        "total": len(run_rows),
        "success": statuses.get("success", 0),
        "failed": statuses.get("failed", 0),
        "treatment_not_observed": statuses.get("treatment_not_observed", 0),
        "by_condition": {
            condition: dict(Counter(item.get("status") for item in run_rows if item.get("condition") == condition))
            for condition in conditions
        },
    }
    (out / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Resultados: {out}")
    print(f"Modo: {args.experiment_mode} / {protocol_mode}")
    print(f"Sucesso: {summary['success']}/{summary['total']}")
    if args.experiment_mode == "efficacy":
        print("Entregue grading.csv + responses/ ao avaliador; não entregue operator.csv.")
    else:
        print("Execute scripts/analyze_discoverability.py para calcular leitura espontânea.")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
