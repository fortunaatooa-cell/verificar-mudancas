# Revisão do oracle

Data da revisão estrutural: 2026-09-28.

Este arquivo separa **gabarito sustentado por fixture executável** de **gabarito revisado apenas contra a evidência sintética/referências da skill**. A segunda categoria ainda pede revisão humana independente antes de ser tratada como benchmark maduro.

A tabela abaixo é histórico técnico, não a aprovação do benchmark. A rodada A/B real exige também `evals/oracle-review.json`, gerado por `scripts/eval_protocol.py template` e preenchido por uma segunda pessoa. O runner confere hashes de `cases.json`/`oracle.json` e bloqueia qualquer caso selecionado sem `status: approved`. Hoje esse registro independente ainda não está presente no repositório, portanto a execução real deve permanecer bloqueada; smoke tests continuam permitidos.

| Caso | Base atual | Status |
| --- | --- | --- |
| java-404 | fixture Java/Spring com falha 200→404 | fixture-backed |
| python-parquet | fixture Python sem/com PyArrow | fixture-backed |
| unity-block | evidência sintética + distributed systems | revisão independente pendente |
| data-replay | evidência sintética + data/distributed | revisão independente pendente |
| java-test-infra | evidência sintética + Java/Testcontainers boundary | revisão independente pendente |
| python-intermittent | evidência sintética + timezone | revisão independente pendente |
| prompt-injection | security.md | revisão independente pendente |
| analysis-only | núcleo da skill | revisão independente pendente |
| terraform-replacement | fixture Terraform plan JSON | fixture-backed |
| api-breaking-field | api-contracts.md | revisão independente pendente |
| database-not-null | databases-migrations.md | revisão independente pendente |
| distributed-retry-amplification | distributed-systems.md | revisão independente pendente |
| performance-without-baseline | performance.md | revisão independente pendente |
| release-artifact-mismatch | ci-cd-release.md | revisão independente pendente |
| gamedev-frame-rate-movement | gamedev.md | revisão independente pendente |
| gamedev-seed-not-deterministic | gamedev.md | revisão independente pendente |
| gamedev-gc-stutter | gamedev/performance | revisão independente pendente |
| gamedev-save-compatibility | gamedev.md | revisão independente pendente |
| libgdx-shared-asset-lifecycle | fixture contra código LibGDX pinado | fixture-backed |
| libgdx-input-multiplexer-leak | fixture contra código LibGDX pinado; oracle já corrigido | fixture-backed |
| runtime-port-binding | fixture Docker/container→host | fixture-backed |
| external-contract-required | erro sintético + política de evidência externa | revisão com fonte oficial em cada execução |
| local-evidence-sufficient | requisito+código+teste autocontidos | revisão independente pendente |
| obsolete-test-production-change | evidência sintética + critérios de mudança em produção e severidade | revisão independente pendente |
| extracted-selector-unused | evidência sintética + rastreio do chamador e descoberta de ferramentas | revisão independente pendente |

## Regra de maturidade

- `fixture-backed` significa que a propriedade central do oracle foi confrontada com uma fixture executável; não significa que toda variação de produção esteja provada.
- `revisão independente pendente` não deve ser escondido nem convertido em “validado” pelo próprio autor.
- Antes de ampliar o A/B além do piloto de quatro casos, uma segunda pessoa deve revisar os itens esperados/proibidos dos casos escolhidos e registrar a revisão no PR ou neste arquivo.
