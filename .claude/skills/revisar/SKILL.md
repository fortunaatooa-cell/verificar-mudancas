---
name: revisar
description: "Revisa diff ou PR de forma adversarial, procurando regressões, riscos e evidência insuficiente."
disable-model-invocation: true
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /revisar

Revisar uma mudança existente (diff, branch, PR ou conjunto de arquivos) sem assumir que a implementação está correta.

## Saída

- findings priorizados por impacto;
- regressões e incompatibilidades potenciais;
- testes ausentes ou frágeis;
- contraexemplos;
- riscos de segurança/runtime quando aplicáveis;
- lacunas de verificação;
- decisão técnica: `APROVAR`, `AJUSTAR` ou `BLOQUEAR`.

O foco é a mudança observada. Não inventar contexto de negócio ausente; marcar incerteza quando ela altera a avaliação.
