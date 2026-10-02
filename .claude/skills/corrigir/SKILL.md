---
name: corrigir
description: "Investiga, corrige com a menor mudança correta e valida regressão e evidência."
disable-model-invocation: true
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /corrigir

Conduzir uma correção com evidência proporcional ao risco.

## Fluxo

1. confirmar ou estabelecer a causa;
2. definir critérios de aceite;
3. escolher prova de regressão/fronteira;
4. implementar a menor mudança correta;
5. executar verificações aplicáveis após a última alteração;
6. revisar diff e procurar contraexemplo;
7. validar as alegações finais.

Se a hipótese for invalidada durante a correção, interromper a implementação e retornar à investigação.

Não usar `/corrigir` como atalho para editar sem diagnóstico quando a causa for incerta.
