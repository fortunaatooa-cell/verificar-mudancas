#!/usr/bin/env bash
set -euo pipefail
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"

if [[ -n "${FIXTURE_WORKDIR:-}" ]]; then
  WORKDIR="$FIXTURE_WORKDIR"
  mkdir -p "$WORKDIR"
  CLEANUP=0
else
  WORKDIR="$(mktemp -d)"
  CLEANUP=1
fi

cleanup() {
  if [[ "$CLEANUP" == "1" ]]; then rm -rf "$WORKDIR"; fi
}
trap cleanup EXIT

cp "$SOURCE_DIR"/requirements.txt "$SOURCE_DIR"/make_parquet.py "$SOURCE_DIR"/verify_missing_engine.py "$SOURCE_DIR"/verify_success_and_timezone.py "$WORKDIR"/
cd "$WORKDIR"

"$PYTHON" -m venv .venv
PY="$WORKDIR/.venv/bin/python"
"$PY" -m pip install -q --upgrade pip
"$PY" -m pip install -q -r requirements.txt

echo '=== cria parquet com engine compatível ==='
"$PY" make_parquet.py

echo '=== remove engine para reproduzir erro de runtime ==='
"$PY" -m pip uninstall -y -q pyarrow
"$PY" verify_missing_engine.py

echo '=== reinstala versão pinada e prova leitura + timezone ==='
"$PY" -m pip install -q pyarrow==21.0.0
"$PY" verify_success_and_timezone.py
