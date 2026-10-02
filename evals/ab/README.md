# A/B controlado da skill

Objetivo: medir se o **mesmo agente** resolve melhor os mesmos casos com a `verificar-mudancas` do que sem ela.

## Piloto inicial

Casos: `runtime-port-binding`, `external-contract-required`, `local-evidence-sufficient`, `java-404`. São **3 repetições por caso e por braço**: 24 execuções.

Manter iguais modelo, reasoning effort, ferramentas, acesso, prompt-base, timeout e evidência. O agente recebe `prompt` + `evidence`; nunca recebe o oracle.

## Efeito mínimo congelado

O arquivo versionado [effect-minimum.json](effect-minimum.json) define o efeito mínimo antes de qualquer rodada real. A escala é 0–1. Para as dimensões de ganho, o mínimo inicial é **0,15**; para `seguranca` e `honestidade`, o mínimo é 0 porque a exigência principal é **não regredir**.

O runner copia o arquivo para a pasta da rodada e grava seu SHA-256 normalizado em `experiment.json`. O analisador recusa snapshot com hash diferente. Alterar esse arquivo depois de observar resultados invalida a rodada.

A vitória de um caso exige simultaneamente:

```text
delta_pontuacao >= efeito_minimo_do_caso
violacoes_with_skill <= violacoes_baseline
regressao_critica == false
```

O efeito mínimo do caso é a média dos limiares versionados das `applicable_dimensions` do oracle.

## Tratamento realmente observado

`workspace_had_skill` prova apenas instalação. `treatment_observed` é calculado do JSONL pela leitura observável de `SKILL.md` ou referência da skill.

Se uma execução `with_skill` terminar sem leitura observada, recebe `status=treatment_not_observed`, é excluída do cálculo e aparece na contagem do relatório. Isso evita chamar de tratamento uma execução em que a skill estava presente mas não foi usada.

## Denominador fixo

Cada caso possui `applicable_dimensions` em `cases.json` e `oracle.json`. O analisador usa exatamente esse conjunto nos dois braços. Um `N/A` acidental do avaliador não remove a dimensão do denominador; ele é reportado como pontuação ausente.

Falha/timeout permanece em `results.csv` e recebe score 0 para a comparação. Ela nunca desaparece do cálculo.

## Revisão independente antes da rodada real

Gere um registro hashado:

```bash
python3 scripts/eval_protocol.py template \
  --out evals/oracle-review.json \
  --case-id runtime-port-binding \
  --case-id external-contract-required \
  --case-id local-evidence-sufficient \
  --case-id java-404
```

Uma segunda pessoa revisa item a item e preenche o registro. Sem aprovação compatível com os hashes atuais, `run_agent_eval.py` bloqueia a rodada real.

## Rodar eficácia

```bash
python3 scripts/run_agent_eval.py \
  --out eval-runs/pilot-001 \
  --model <modelo-fixado> \
  --reasoning-effort medium \
  --web-search live
```

`--smoke-test` permite validar apenas o harness; o relatório marca o resultado como não publicável para eficácia.

Depois da pontuação cega:

```bash
python3 scripts/analyze_ab_results.py --run-dir eval-runs/pilot-001
```

## Experimento C — descobribilidade

Este experimento é separado de D1. A skill é instalada, mas não é mencionada no prompt:

```bash
python3 scripts/run_agent_eval.py \
  --experiment-mode discoverability \
  --out eval-runs/discovery-001 \
  --model <modelo-fixado>
python3 scripts/analyze_discoverability.py --run-dir eval-runs/discovery-001
```

A saída `discoverability.csv` mede `discovered=true/false` pela leitura espontânea de `SKILL.md`. Esses dados nunca entram no scorecard de eficácia.

## Disciplina

- sessões independentes;
- sem reexecutar seletivamente falhas até dar certo;
- tratamento não observado é excluído e contado;
- resultados negativos são preservados;
- oracle nunca entra no prompt;
- `operator.csv` não é entregue ao avaliador;
- logs operacionais são revisados antes de qualquer publicação.
