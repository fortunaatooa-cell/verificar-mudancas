---
name: aprender
description: "Propõe aprendizado sanitizado e regressões revisáveis sem promoção automática."
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /aprender

Objetivo: transformar uma execução concluída em aprendizado revisável e sanitizado.

1. Use `agente-aprendizado.md` para separar ocorrência específica de padrão generalizável.
2. Remova nomes internos, dados de cliente, secrets, IDs e código proprietário.
3. Escolha `lesson`, `pattern`, `incident`, `project_knowledge`, atualização de referência/playbook, regra ou eval.
4. Persistência em `memory/` é explícita: valide/adicone com `scripts/memory_store.py` (ou o runtime instalado).
5. Memória recuperada é hipótese histórica, nunca verdade do novo caso.
6. Para uma falha que não deve retornar, gere proposta com `create_regression_eval.py`; o oracle exige expectativas e proibições explícitas e revisão humana.
7. Não promova automaticamente para `SKILL.md` ou regras; exija revisão e regressão antes.
