---
name: investigar
description: "Investiga causa e evidência sem editar arquivos ou aplicar correções."
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /investigar

Executar investigação sem editar arquivos ou aplicar correções.

## Entrega

- fatos observados;
- comportamento esperado x observado;
- primeira divergência conhecida;
- hipóteses concorrentes;
- evidência favorável/contrária;
- hipótese mais forte, se sustentada;
- próximo experimento discriminante;
- lacunas e limitações.

Usar `investigador` e adicionar `diagnosticador-runtime` ou `revisor-seguranca` somente quando o domínio exigir.

Se a causa não puder ser fechada, não forçar conclusão. Entregar o experimento que mais reduz a incerteza.
