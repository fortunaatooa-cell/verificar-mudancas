---
name: verificar
description: "Executa o ciclo completo de investigação, mudança e verificação com evidência."
---

Este é o wrapper nativo do Claude Code para o comando portátil. Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.

# /verificar

Workflow principal.

1. Detecte capacidades do harness; use adapter e fallback quando necessário.
2. Classifique tarefa, risco, critérios de aceite e stop conditions.
3. Carregue somente referências, playbook, regras e especialistas pertinentes.
4. Consulte memória somente quando puder ajudar; trate resultados como pistas.
5. Investigue e procure evidência contrária antes de corrigir.
6. Em edição material, aplique `pre-edit`; depois `post-edit` quando suportado.
7. Implemente a menor mudança correta.
8. Execute prova na fronteira afetada, revisão adversarial e busca de contraexemplo.
9. Use `pre-finish`, `/validar` e `/portao-qualidade` conforme risco.
10. Após conclusão, `/aprender` pode propor memória/eval sem promoção automática.

Sem subagentes, execute os mesmos papéis sequencialmente no agente atual.
