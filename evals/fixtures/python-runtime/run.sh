#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PYTHON="${PYTHON:-python3}"
rm -rf .venv sample.parquet
"$PYTHON" -m venv .venv
PY="$HERE/.venv/bin/python"
PIP="$PY -m pip"
$PIP install -q --upgrade pip
$PIP install -q -r requirements.txt

echo '=== cria parquet com engine compatível ==='
$PY make_parquet.py

echo '=== remove engine para reproduzir erro de runtime ==='
$PIP uninstall -y -q pyarrow
$PY verify_missing_engine.py

echo '=== reinstala versão pinada e prova leitura + timezone ==='
$PIP install -q pyarrow==21.0.0
$PY verify_success_and_timezone.py
