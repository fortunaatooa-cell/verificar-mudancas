# Modos de resposta

A mesma análise pode ser entregue em três modos sem mudar o padrão de evidência.

## `simples`

Priorize entendimento rápido: conclusão principal, evidência essencial, riscos/incertezas materiais e próximo passo. Evite detalhe que não mude a decisão. Para desenho técnico: **o que é**, **como funciona/se conecta**, **problemas ou dúvidas principais** e **próximo passo**.

## `aprofundado`

Explique contexto, evidências, análise técnica verificável, alternativas, limitações, riscos e validação. Inclua componentes, interfaces, contratos, medidas/fontes, cenários de erro e implicações de implementação quando pertinentes. Para desenho técnico, acrescente inventário, relações entre vistas/camadas, dimensões/tolerâncias observáveis, inconsistências, suposições e especificação de redesenho.

## `ambos`

Entregue primeiro **Resumo simples** autossuficiente e depois **Análise aprofundada**. A parte detalhada pode expandir o resumo, nunca contradizê-lo.

## Seleção automática

“resumido”, “rápido” ou “simples” → `simples`; “detalhado”, “técnico”, “profundo” ou “completo” → `aprofundado`; pedido dos dois → `ambos`. Sem preferência, ajuste ao risco e complexidade.

Nenhum modo autoriza omitir alerta de segurança, incerteza material, ausência de evidência ou limitação de ferramenta. `simples` reduz detalhe, não rigor.
