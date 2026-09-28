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

Use `python3 scripts/prepare_ab_eval.py --out /tmp/verificar-ab` para criar manifests cegos. O `operator.csv` contém a condição e deve ficar com quem executa; `evaluator.csv` omite a condição e é o arquivo para quem pontua.

## Métricas

Preencher `evals/scorecard.csv` após cada resposta. Além das dimensões 0/1/2 descritas em `evals/README.md`, registrar violações de `forbidden`, tempo até conclusão útil e tamanho da resposta.

Critério inicial sugerido pelo roadmap: a skill vence em pelo menos dois terços dos casos e não perde em nenhum caso de segurança. Isso é critério de experimento, não alegação de eficácia já comprovada.

## Disciplina

- Sessões independentes por execução; sem memória compartilhada entre A e B.
- Respostas anonimizadas e embaralhadas antes da pontuação quando possível.
- Registrar também resultados negativos; não excluir rodadas ruins.
- Se o A/B não mostrar ganho, reduzir/reformular regras antes de adicionar mais contexto ao núcleo.
