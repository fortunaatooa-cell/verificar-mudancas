---
name: depurar-jogo
description: "Reproduz, investiga, corrige e valida bugs de jogo/runtime quando autorizado."
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write]
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /depurar-jogo

Investigar e, quando autorizado, corrigir bugs de jogos com reprodução, instrumentação e verificação na runtime adequada.

## Roteamento

Fluxo padrão:

`investigador → investigador-gameplay → estrategista-testes → implementador → revisor-codigo → validador-regressao-jogo → verificador-evidencias`

Adicionar:
- `diagnosticador-runtime` para crash, memória, GC, CPU/GPU, startup, filesystem, rede ou limites;
- `revisor-seguranca` quando houver conteúdo não confiável, multiplayer, mods, arquivos externos ou superfície relevante;
- `planejador` para mudança ampla, engine upgrade, migração de save ou múltiplos sistemas;
- `arquiteto` somente quando a causa exigir decisão estrutural durável.

## Regras

1. Carregar `references/gamedev.md` e a referência real da engine/stack quando existir.
2. Registrar engine, target, build, cena/estado inicial e passos de reprodução.
3. Controlar seed, FPS/timestep, input, save e rede quando pertinentes.
4. Reduzir o relato ao menor cenário reproduzível antes de alterar código quando viável.
5. Preferir estado estruturado + logs correlacionados a observação visual isolada.
6. Após a correção, repetir o cenário original e um conjunto mínimo de cenários vizinhos.
7. Sem runtime/ferramenta, produzir roteiro de reprodução e critérios de evidência; não alegar execução.

Usar o playbook `playbooks/game-bug.md`.
