# Status da branch agentic

`feature/agentic-v1-5` permanece **experimental, not evaluated**.

A implementação dos controles da Spec 10/10 foi feita nesta branch por decisão de trabalho, mas isso não transforma as capacidades agentic já existentes em evidência de eficácia. Nenhum agente, adapter ou comando novo deve ser promovido para `main` antes da primeira rodada A/B real (T8).

Depois de T8, T14 exige revisar cada capacidade desta branch pelo mesmo crivo D1–D3. O que não tiver evidência permanece experimental.


## Integração Claude

O adapter Claude já existente foi atualizado para mapear os mesmos papéis/comandos/regras para `CLAUDE.md`, Skills, subagents, rules e hooks nativos. Isso é **compatibilidade de superfície**, não criação de uma nova metodologia nem promoção de capacidades.

Plugins/mods adicionais continuam fora do caminho automático antes de T8. A integração Claude inteira permanece no conjunto agentic/experimental que será revisado em T14.
