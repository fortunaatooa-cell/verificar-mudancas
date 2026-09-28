#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
MVN="${MVN:-mvn}"
command -v "$MVN" >/dev/null || { echo "ERRO: Maven não encontrado" >&2; exit 1; }
printf '%s\n' '=== Java/Spring fixture: red-before-green HTTP ==='
if "$MVN" -q -Dtest=OrderDesiredContractTest test; then
  echo "ERRO: o teste deveria falhar com fixture.synthetic-fallback=true" >&2
  exit 1
else
  echo "Falha esperada confirmada: o fallback transforma ausência em HTTP 200."
fi
printf '%s\n' '=== Java/Spring fixture: comportamento corrigido ==='
"$MVN" -q -Dfixture.synthetic-fallback=false -Dtest=OrderDesiredContractTest test
printf '%s\n' '=== Java/Spring fixture: semântica transacional ==='
"$MVN" -q -Dtest=SpringTransactionSemanticsTest test
