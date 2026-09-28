# /aprender

Objetivo: transformar uma execução concluída em aprendizado revisável e sanitizado.

1. Use `agente-aprendizado.md` para separar ocorrência específica de padrão generalizável.
2. Remova nomes internos, dados de cliente, secrets, IDs e código proprietário.
3. Escolha `lesson`, `pattern`, `incident`, atualização de referência/playbook, regra ou eval.
4. Persistência em `memory/` é explícita: valide/adicone com `scripts/memory_store.py` (ou `.verificar-mudancas/scripts/memory_store.py` após instalação).
5. Memória recuperada é hipótese histórica, nunca verdade do novo caso.
6. Não promova automaticamente para `SKILL.md` ou regras; exija revisão e regressão antes.
