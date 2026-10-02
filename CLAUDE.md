# Verificar Mudanças — Claude Code

Este workspace usa o `verificar-mudancas` como harness de engenharia. Este arquivo é curto de propósito: procedimentos detalhados ficam em skills e especialistas para preservar contexto.

## Fonte de verdade

- Orquestração portátil: `AGENTS.md`.
- Núcleo metodológico: `.agents/skills/verificar-mudancas/SKILL.md`.
- Papéis: `.agents/agents/`.
- Comandos: `.agents/commands/`.
- Regras: `.agents/rules/`.

Quando houver conflito entre um wrapper nativo de Claude e o arquivo portátil correspondente, o arquivo portátil é canônico.

## Uso nativo no Claude Code

- Skills ficam em `.claude/skills/`; use `/verificar`, `/investigar`, `/corrigir`, `/revisar`, `/validar`, `/depurar-jogo` e os demais comandos existentes.
- Subagents ficam em `.claude/agents/`. Delegue trabalho especializado ou isolável; tarefas independentes podem rodar em paralelo.
- A sessão principal integra resultados, decide conflitos e responde pela validação final.
- Regras em `.claude/rules/` espelham as regras portáteis.
- Hooks em `.claude/settings.json` adicionam guardrails determinísticos sem substituir a metodologia.

## Invariantes

- evidência antes de confiança;
- fato ≠ hipótese ≠ inferência ≠ desconhecido;
- não alegar execução, visão, render, teste ou acesso que não ocorreu;
- investigação retorna à hipótese quando a evidência contradiz a causa;
- implementação usa a menor mudança correta;
- HIGH/CRITICAL exige controles e `aprovacao_humana_necessaria=true`;
- dados corporativos, secrets e código proprietário não entram no repositório público.

A branch `feature/agentic-v1-5` continua experimental até as provas T8/T14 da Spec 10/10.
