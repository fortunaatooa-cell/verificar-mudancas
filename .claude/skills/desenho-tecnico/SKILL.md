---
name: desenho-tecnico
description: "Analisa ou especifica desenho técnico sem inventar medidas, escala ou render inexistente."
allowed-tools: [Read, Grep, Glob]
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /desenho-tecnico

Analisar, revisar, criar ou redesenhar um artefato técnico visual.

Sintaxe conceitual: `/desenho-tecnico <analisar|revisar|criar> [simples|aprofundado|ambos]`.

1. Detecte `vision_input` e `visual_generation`; não presuma capabilities.
2. Carregue `desenho-tecnico`/`analista-desenhos-tecnicos` e a referência `technical-drawings.md`.
3. Para análise, separe observado, inferido e não determinável.
4. Para criação, prefira fonte editável/verificável; renderize somente quando houver capability real.
5. Nunca fabrique medidas, escala, tolerâncias, norma ou certificação.
6. Use o modo de resposta pedido; sem escolha, adapte à complexidade e ao risco.
