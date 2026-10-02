# Manifesto de promoção do harness

A implementação permanece em `feature/agentic-v1-5`, conforme a decisão de trabalho atual. Este manifesto existe para preservar a separação exigida pela Spec 10/10 quando chegar o momento de promover conteúdo para `main`.

## Harness elegível para revisão de promoção

- `scripts/run_agent_eval.py`
- `scripts/analyze_ab_results.py`
- `scripts/prepare_ab_eval.py`
- `scripts/analyze_discoverability.py`
- `scripts/check_sensitive_examples.py`
- `scripts/check_pilot_readiness.py`
- `scripts/eval_protocol.py`
- referências reguladas/evidência diretamente necessárias ao harness
- `evals/` e testes correspondentes
- arquivos de manutenção necessários ao protocolo

## Permanecem agentic/experimentais até T14

- `.agents/agents/`
- `.agents/commands/`
- `.agents/hooks/`
- `adapters/`
- `.claude/` e `CLAUDE.md`
- memória/aprendizado agentic
- schemas da orquestração
- especializações de jogo/desenho técnico

A integração Claude adicionada nesta branch é um mapeamento nativo da orquestração experimental existente; não muda esta fronteira e não constitui evidência D1.

Nenhuma promoção para `main` é executada por este manifesto.
