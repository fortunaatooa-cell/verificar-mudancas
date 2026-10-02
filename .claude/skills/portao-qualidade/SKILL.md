---
name: portao-qualidade
description: "Executa o quality gate proporcional ao risco, sem alegar checks não executados."
disable-model-invocation: true
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /portao-qualidade

Objetivo: produzir decisão estruturada sobre a qualidade da mudança sem fingir execução.

1. Determine critérios/risco e checks aplicáveis.
2. Gere o plano com `python3 scripts/quality_gate.py --config <config>` (ou `.verificar-mudancas/scripts/quality_gate.py` após instalação completa).
3. Revise os comandos detectados/configurados antes de executar.
4. Somente com autorização, execute com `--execute`.
5. Interprete `PASS`, `FAIL`, `PARTIAL`, `BLOCKED` ou `N/A`; nunca converta plano não executado em PASS.
6. Para HIGH/CRITICAL, combine com controles de risco e `pre-finish`.
