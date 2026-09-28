# Verificar Mudanças — orquestração agentic

Este repositório usa `.agents/skills/verificar-mudancas/SKILL.md` como núcleo metodológico. Skills auxiliares, agentes, regras, hooks, memória e adapters complementam o núcleo; não o substituem.

## Interface canônica em português

- `/verificar`
- `/investigar`
- `/corrigir`
- `/revisar`
- `/validar`
- `/portao-qualidade`
- `/aprender`

Consulte `.agents/commands/` ou trate intenção equivalente da mesma forma.

## Bootstrap

1. Leia a skill principal.
2. Detecte o adapter/capacidades quando a superfície for desconhecida. No repositório fonte: `python3 scripts/detect_capabilities.py --adapter <nome>`. Em instalação completa: `python3 .verificar-mudancas/scripts/detect_capabilities.py --adapter <nome>`.
3. Aplique as regras mínimas pertinentes em `.agents/rules/`.
4. Carregue skill auxiliar apenas quando ajudar (`investigar`, `estrategia-testes`, `revisar-mudanca`, `diagnosticar-runtime`).
5. Se houver memória local, pesquise somente quando relevante e use resultados como hipótese histórica.

## Roteamento

Fluxo base para correção:

`investigador → estrategista-testes → implementador → revisor-codigo → verificador-evidencias`

Para memória, JVM, container, Lambda, deploy, portas, CPU, startup, rede ou limites de recurso, incluir `diagnosticador-runtime`.

Para autenticação, autorização, IAM, secrets, dados sensíveis, entrada externa ou exposição de rede, incluir `revisor-seguranca` quando pertinente.

Para aprendizado após conclusão, use `agente-aprendizado`; ele propõe, não promove automaticamente. Falha recorrente pode gerar proposta de regressão com oracle explícito.

Em solicitação somente investigativa, não editar. Sem subagentes, execute os papéis sequencialmente mantendo separação lógica.

## Hooks e quality gate

Eventos canônicos: `pre-edit`, `post-edit`, `pre-finish`. Harnesses sem hook nativo podem chamar o runner portátil. `pre-finish` bloqueia conclusão confiante quando a evidência é insuficiente.

`/portao-qualidade` primeiro mostra o plano; comandos detectados/configurados só são executados com autorização explícita (`--execute`).

## Memória

`memory/` aceita apenas conteúdo sanitizado. Use `memory_store.py` para validar, adicionar, indexar e buscar. `project_knowledge` é específico do workspace autorizado e não deve ser promovido ao repositório público. Uma ocorrência não vira regra universal só por existir na memória.

## Invariantes

- evidência antes de confiança;
- fato ≠ hipótese ≠ inferência ≠ desconhecido;
- nunca alegar execução inexistente;
- menor mudança correta;
- contraexemplo e revisão após implementação;
- HIGH/CRITICAL exigem blast radius, recuperação, stop conditions e sinais;
- produção/ações destrutivas exigem autorização apropriada;
- dados corporativos, secrets e código proprietário não entram no repositório público.

A arquitetura completa está em `docs/agentic-system.md`.
