# Modos de resposta

A mesma análise pode ser entregue em três modos sem mudar o padrão de evidência.

## `simples`

Priorize entendimento rápido. Responda com a conclusão principal, o que sustenta essa conclusão, riscos/incertezas materiais e próximo passo. Evite detalhes de implementação que não mudem a decisão.

Para desenho técnico: diga **o que é**, **como funciona/como se conecta**, **problemas ou dúvidas principais** e **o próximo passo**.

## `aprofundado`

Explique contexto, evidências, cadeia de raciocínio técnico em termos verificáveis, alternativas, limitações, riscos e estratégia de validação. Inclua detalhes de componentes, interfaces, contratos, medidas/fontes, cenários de erro e implicações de implementação quando pertinentes.

Para desenho técnico: acrescente inventário de elementos, relações entre vistas/camadas, dimensões/tolerâncias observáveis, inconsistências, suposições, compatibilidade e especificação de eventual redesenho.

## `ambos`

Entregue primeiro uma seção **Resumo simples** autossuficiente e depois **Análise aprofundada**. A parte detalhada pode referenciar o resumo, mas não deve contradizê-lo.

## Seleção automática

Se o usuário pedir “resumido”, “rápido”, “simples” ou equivalente, use `simples`. Se pedir “detalhado”, “técnico”, “profundo”, “completo” ou equivalente, use `aprofundado`. Se pedir os dois, use `ambos`. Sem preferência, ajuste ao risco e complexidade.

Nenhum modo autoriza omitir alerta de segurança, incerteza material, ausência de evidência ou limitação de ferramenta. `simples` reduz detalhe, não rigor.
