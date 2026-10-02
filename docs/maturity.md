# Maturidade do verificar-mudancas

A maturidade é baseada em evidência, não em quantidade de instruções.

## Estado atual

O projeto possui núcleo modular, referências por domínio, playbooks, agentes especializados, quality gate, memória controlada, fixtures e runner A/B. Isso sustenta maturidade de engenharia do harness, mas **não prova eficácia causal da skill**.

Uma rodada com agente simulado valida isolamento, cegamento, reconciliação e arquivos produzidos. Ela não conta como evidência de que um modelo real melhora com a skill.

## Gate de eficácia

Uma rodada A/B real só é considerada evidência quando:

1. usa o mesmo modelo, configuração, ferramentas e contexto nos dois braços;
2. mantém sessões independentes e cegamento do avaliador;
3. fixa a versão da skill e os hashes de `cases.json` e `oracle.json`;
4. possui revisão humana independente registrada para todos os casos selecionados;
5. preserva resultados negativos e falhas;
6. aplica o critério de sucesso definido antes da execução.

O runner bloqueia por padrão a rodada real quando `evals/oracle-review.json` está ausente, desatualizado ou incompleto. `--smoke-test` existe apenas para validar o harness sem gastar uma rodada de eficácia.

## Referência de níveis

- **8,5:** arquitetura e fixtures sólidas, sem evidência A/B suficiente.
- **9:** A/B real com pelo menos 8 casos, 3 execuções por braço, gabaritos revisados e scorecard completo.
- **9,5:** A/B ampliado e piloto real aprovado, com métricas, governança e revisão humana.

Nenhuma dessas faixas significa que a skill detecta todo bug ou substitui revisão técnica.
