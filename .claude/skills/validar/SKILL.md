---
name: validar
description: "Valida alegações contra evidências e classifica PASS, FAIL ou INCONCLUSIVE."
allowed-tools: [Read, Grep, Glob, Bash]
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /validar

Objetivo: validar uma alegação de conclusão contra evidência real.

- Liste claims materiais e a evidência de cada um.
- Use `verificador-evidencias` e o hook `pre-finish` quando disponível.
- Confirme que a prova relevante ocorreu depois da última mudança material.
- Se houver quality gate configurado, incorpore seu resultado; plano não executado vale no máximo `PARTIAL`.
- Saída por claim: `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED` ou `BLOCKED`.
