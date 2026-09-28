#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="verificar-mudancas/runtime-port-binding:${GITHUB_RUN_ID:-local}"
BROKEN="verificar-port-broken-${GITHUB_RUN_ID:-local}"
GOOD="verificar-port-good-${GITHUB_RUN_ID:-local}"
BROKEN_PORT=19080
GOOD_PORT=19081

cleanup() {
  docker rm -f "$BROKEN" "$GOOD" >/dev/null 2>&1 || true
}
trap cleanup EXIT
cleanup

echo "=== Build da fixture ==="
docker build -t "$IMAGE" "$HERE"

wait_for_log() {
  local name="$1"
  local pattern="$2"
  for _ in $(seq 1 30); do
    if docker logs "$name" 2>&1 | grep -Fq "$pattern"; then
      return 0
    fi
    sleep 0.2
  done
  echo "Container $name não anunciou startup esperado" >&2
  docker logs "$name" >&2 || true
  return 1
}

echo "=== Cenário quebrado: processo inicia em loopback ==="
docker run -d \
  --name "$BROKEN" \
  -e PORT=10000 \
  -e BIND_ADDRESS=127.0.0.1 \
  -p "127.0.0.1:${BROKEN_PORT}:10000" \
  "$IMAGE" >/dev/null

wait_for_log "$BROKEN" "LISTENING 127.0.0.1:10000"

docker exec "$BROKEN" python -c "import urllib.request; assert urllib.request.urlopen('http://127.0.0.1:10000/', timeout=2).read() == b'ok\\n'"

echo "Processo responde dentro do próprio container."
if curl --fail --silent --show-error --max-time 2 "http://127.0.0.1:${BROKEN_PORT}/" >/dev/null 2>&1; then
  echo "ERRO: bind em loopback ficou alcançável pela porta publicada; a fixture perdeu a propriedade esperada." >&2
  exit 1
fi

echo "Falha externa esperada confirmada apesar de EXPOSE e log de startup."
docker rm -f "$BROKEN" >/dev/null


echo "=== Cenário correto: listener em todas as interfaces ==="
docker run -d \
  --name "$GOOD" \
  -e PORT=10000 \
  -e BIND_ADDRESS=0.0.0.0 \
  -p "127.0.0.1:${GOOD_PORT}:10000" \
  "$IMAGE" >/dev/null

wait_for_log "$GOOD" "LISTENING 0.0.0.0:10000"

for _ in $(seq 1 30); do
  if body="$(curl --fail --silent --show-error --max-time 2 "http://127.0.0.1:${GOOD_PORT}/" 2>/dev/null)"; then
    if [[ "$body" == "ok" ]]; then
      echo "Alcançabilidade externa confirmada: ${body}"
      exit 0
    fi
  fi
  sleep 0.2
done

echo "ERRO: listener em 0.0.0.0 não ficou alcançável pela porta publicada." >&2
docker logs "$GOOD" >&2 || true
exit 1
