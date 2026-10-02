---
name: planejar
description: "Planeja uma mudança ampla, dependências, riscos e critérios de aceite antes de editar."
allowed-tools: [Read, Grep, Glob]
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /planejar

Produzir plano proporcional ao risco sem editar arquivos por padrão.

Aceita modo de resposta `simples`, `aprofundado` ou `ambos`.

Saída mínima: objetivo, escopo, desconhecidos materiais, dependências, etapas, critérios de aceite, estratégia de prova, risco e stop conditions aplicáveis.
