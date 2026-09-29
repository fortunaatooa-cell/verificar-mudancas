---
name: estrategia-testes
description: Escolher a prova mínima suficiente na fronteira realmente afetada e conduzir TDD real quando apropriado.
---
# Estratégia de testes

Escolha a prova conforme a propriedade: regra isolada, integração, contrato, persistência, runtime, performance ou segurança. Um teste verde fora da fronteira afetada é evidência parcial ou irrelevante.

Quando TDD for apropriado, use `RED → GREEN → REFACTOR → REGRESSION`. RED precisa falhar pelo comportamento correto antes da implementação; falha de setup/infra não vale. Teste criado apenas depois da implementação é regressão, não evidência de TDD anterior.