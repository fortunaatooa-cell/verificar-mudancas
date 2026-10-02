# Status da Spec 10/10 nesta branch

Branch: `feature/agentic-v1-5`.

| Tarefa | Estado | Evidência/controle |
| --- | --- | --- |
| T1 treatment_observed | implementado | detect_skill_read + teste JSONL |
| T2 treatment_not_observed | implementado | exclusão e contagem no relatório |
| T3 applicable_dimensions | implementado | cases/oracle + validador + teste |
| T4 falha como não-vitória | implementado | status failed preservado, score 0, smoke de falha |
| T5 critério de vitória | implementado | efeito mínimo + violações + regressão crítica |
| T6 efeito mínimo hashado | implementado | effect-minimum.json + snapshot/hash |
| T7 local-evidence-sufficient | source-backed; revisão humana pendente | oracle sources + gate de revisão independente |
| T8 24 execuções reais | bloqueado corretamente | depende da revisão independente de T7 |
| T9 decisão pós-D1 | bloqueado por T8 | não é permitido antecipar resultado |
| T10 descobribilidade | implementado | modo unprompted + discovered + analisador separado |
| T11 scanner de dados | implementado | scanner + teste fail/pass + CI |
| T12 seis perguntas | gate implementado; respostas externas pendentes | bank-pilot-restrictions.json + check_pilot_readiness.py |
| T13 piloto 2 semanas | infraestrutura/documentação pronta; execução futura | pilot-metrics.md; depende de T12 e tempo real |
| T14 revisão agentic | checklist pronto; execução bloqueada até T8 | agentic-review-checklist.md |

A distinção entre **implementado** e **evidência externa pendente** é intencional. O repositório não fabrica revisão humana, resultado de 24 execuções ou duas semanas de piloto.


### Atualização de compatibilidade Claude

O adapter Claude existente ganhou integração nativa com `CLAUDE.md`, `.claude/skills`, `.claude/agents`, `.claude/rules` e hooks. A mudança reaproveita os mesmos papéis e regras e **não altera o status de T7–T14**: é consistência/portabilidade agentic, não evidência D1, D2 ou D4.

Nenhum plugin/mod adicional foi ativado automaticamente; isso permanece fora do escopo antes de T8.
