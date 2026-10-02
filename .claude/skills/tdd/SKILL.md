---
name: tdd
description: "Executa TDD somente quando houver RED observável antes da implementação."
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write]
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /tdd

Modos: `planejar`, `executar`, `revisar`.

Aplicar `RED → GREEN → REFACTOR → REGRESSION` quando TDD for adequado. RED precisa falhar pelo comportamento esperado; erro de setup/infra não vale. Não declarar TDD se o teste foi criado apenas depois da implementação.
