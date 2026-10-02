# Revisão do oracle

Data da revisão estrutural: 2026-10-02.

Este arquivo registra a sustentação técnica do gabarito. **Não substitui a revisão humana independente** exigida para a rodada A/B real; essa aprovação é registrada por `scripts/eval_protocol.py` e vinculada aos hashes de `cases.json` e `oracle.json`.

## Casos com fixture executável

Cada linha abaixo aponta o comando que confronta a propriedade central do caso. Em `oracle.json`, cada item `expected` e `forbidden` também possui `expected_sources`/`forbidden_sources` explícitas.

| Caso | Comando | Estado |
| --- | --- | --- |
| java-404 | `bash evals/fixtures/java-spring/run.sh` | fixture-backed |
| python-parquet | `bash evals/fixtures/python-runtime/run.sh` | fixture-backed |
| terraform-replacement | `bash evals/fixtures/terraform-replacement/run.sh` | fixture-backed |
| libgdx-shared-asset-lifecycle | `bash evals/fixtures/libgdx/run.sh` | fixture-backed |
| libgdx-input-multiplexer-leak | `bash evals/fixtures/libgdx/run.sh` | fixture-backed |
| runtime-port-binding | `bash evals/fixtures/runtime-port-binding/run.sh` | fixture-backed |

`fixture-backed` significa que a propriedade central foi confrontada com execução; itens de honestidade/escopo continuam sustentados pelas normas citadas no próprio oracle.

## Casos sem fixture

Os demais casos usam `expected_sources` e `forbidden_sources` no `oracle.json`, apontando para o código/evidência sintética do caso e para a referência normativa pertinente. Isso torna a origem auditável, mas **não transforma auto-revisão em revisão independente**.

### Revisão independente ainda pendente

| Caso | Sustentação atual | Pendência |
| --- | --- | --- |
| `local-evidence-sufficient` | source-backed pelo requisito, teste reproduzível e trecho `age > 18` do próprio caso | segunda pessoa precisa revisar e assinar o hash |
| `obsolete-test-production-change` | `expected_sources`/`forbidden_sources` no oracle | segunda pessoa precisa revisar e assinar o hash |
| `extracted-selector-unused` | `expected_sources`/`forbidden_sources` no oracle | segunda pessoa precisa revisar e assinar o hash |

`local-evidence-sufficient` pode compor o piloto somente quando essa revisão independente estiver registrada. Até lá, a rodada real permanece bloqueada.

## Regra de maturidade

- alterar `cases.json` ou `oracle.json` invalida o hash da revisão anterior;
- a revisão independente deve ser feita por outra pessoa, item a item;
- resultado de smoke/fake Codex não é evidência D1;
- resultado negativo real é preservado, não rerodado seletivamente.
