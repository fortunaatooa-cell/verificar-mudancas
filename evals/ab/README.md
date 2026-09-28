# A/B controlado da skill

Objetivo: medir se o **mesmo agente** resolve melhor os mesmos casos com a `verificar-mudancas` do que sem ela. Fixtures validam propriedades técnicas; este protocolo mede comportamento do agente.

## Piloto inicial

Casos padrão:

- `runtime-port-binding`
- `external-contract-required`
- `local-evidence-sufficient`
- `java-404`

Rodar **3 repetições por caso e por braço**:

- A: mesmo modelo/ferramenta sem a skill.
- B: mesmo modelo/ferramenta com uma versão identificada da skill.

Manter iguais: modelo, esforço/configuração, ferramentas, acesso, prompt-base, tempo máximo e evidência fornecida. O agente recebe somente `prompt` + `evidence`; nunca `oracle.json`.

## Preparar apenas os manifests

```bash
python3 scripts/prepare_ab_eval.py --out /tmp/verificar-ab
```

`operator.csv` contém a condição e fica com quem executa. `evaluator.csv` não contém a condição.

## Executar automaticamente com Codex CLI

Pré-requisitos:

- Codex CLI autenticado;
- versão que exponha `codex exec` com `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, sandbox, JSON e `--output-last-message`;
- checkout limpo da pasta `.agents/skills/verificar-mudancas`, para que o tratamento seja associado a um commit exato;
- nenhuma cópia global da `verificar-mudancas` em `~/.agents/skills` ou `${CODEX_HOME:-~/.codex}/skills`, pois isso contaminaria o baseline.

Exemplo:

```bash
python3 scripts/run_agent_eval.py \
  --out eval-runs/pilot-001 \
  --model <modelo-fixado> \
  --reasoning-effort medium \
  --web-search live
```

O runner cria **24 sessões independentes** por padrão (4 casos × 3 repetições × 2 braços). Cada execução usa workspace temporário novo, `codex exec --ephemeral`, sandbox read-only e stdin fechado. O braço `with_skill` recebe uma cópia da pasta da skill; o baseline não recebe. A ordem é embaralhada pelo seed do experimento.

O runner salva:

- `experiment.json`: versão do Codex, modelo, configuração e commit da skill;
- `operator.csv`: mapeamento secreto entre `blind_id` e condição;
- `responses/<blind_id>.md`: respostas brutas sem nome do braço;
- `operator_logs/`: JSONL/stderr/metadata operacional por execução;
- `results.csv`: status, tempo, tamanho, hash da resposta e tool calls observáveis;
- `grading.csv`: planilha **cega**, sem a coluna `condition`, para o avaliador.

Se uma execução falhar, ela é preservada. Use `--resume` para continuar sem repetir rodadas já concluídas com sucesso.

### Por que o runner bloqueia skill global

Codex pode descobrir skills em escopo de usuário. Se `verificar-mudancas` estiver instalada globalmente, uma execução chamada de baseline pode recebê-la mesmo sem a pasta no workspace. O runner aborta nesse caso. `--allow-global-skill-contamination` existe somente para teste/depuração; não use em um benchmark que será reportado como evidência.

## Avaliar às cegas

Entregue ao avaliador apenas `grading.csv` e `responses/`. Não entregue `operator.csv`, `experiment.json` nem `operator_logs/` antes da pontuação.

Para cada dimensão aplicável, preencher **0, 1 ou 2**; usar `N/A` quando realmente não se aplicar. `violacoes` deve ser a contagem inteira de itens `forbidden` violados.

Depois da avaliação:

```bash
python3 scripts/analyze_ab_results.py --run-dir eval-runs/pilot-001
```

Isso reconecta a condição somente após a pontuação e gera `comparison.json` e `report.md`, incluindo resultado por caso, violações, delta de segurança, tempo e tamanho das respostas.

Critério inicial pré-definido: a skill vence em pelo menos dois terços dos casos e não perde em nenhum caso pontuado em segurança. Isso é critério de experimento, não alegação de eficácia já comprovada.

## Disciplina

- Sessões independentes por execução; sem `resume` de conversa entre A e B.
- Mesmo modelo, reasoning effort, web search, sandbox e timeout nos dois braços.
- Oracle nunca entra no prompt do agente.
- Respostas são pontuadas sem revelar a condição quando possível.
- Registrar também resultados negativos; não excluir rodadas ruins.
- Não publicar `operator_logs/` sem revisar conteúdo; são artefatos operacionais, não documentação pública.
- Se o A/B não mostrar ganho, reduzir/reformular regras antes de adicionar mais contexto ao núcleo.

## Teste do runner

O CI usa `fake_codex.py` para provar a propriedade central do harness: baseline recebe workspace sem skill e `with_skill` recebe workspace com skill, sem chamar um modelo real nem gastar tokens.
