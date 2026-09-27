# Arquitetura e refatoração

Usar quando a mudança alterar boundaries, responsabilidades, dependências, estrutura de módulos ou quando a solicitação for refatoração relevante.

## Preservar intenção e comportamento
- Identificar qual problema arquitetural existe de fato: acoplamento, ownership confuso, dependência cíclica, baixa coesão, duplicação ou dificuldade operacional. Não introduzir padrão ou microsserviço sem problema sustentado.
- Em refatoração, estabelecer comportamento protegido antes de mover responsabilidades. O objetivo principal é preservar contratos e efeitos observáveis enquanto melhora a estrutura.
- Verificar direção de dependências, ownership de dados, contratos entre módulos e custo operacional da nova separação.

## Decisões maiores
- Para mudança difícil de reverter, registrar alternativas consideradas, trade-offs, compatibilidade/migração e critério de sucesso. Usar ADR ou mecanismo equivalente apenas quando o projeto adotar ou a decisão justificar registro durável.
- Preferir passos incrementais verificáveis a reescritas amplas sem baseline.

## Entrega específica
Relatar comportamento preservado, responsabilidade movida, dependências alteradas, trade-offs e dívida que permaneceu intencionalmente fora do escopo.
