# SPEC implementada — Verificar Mudanças Agentic Engineering System

## Visão

A `verificar-mudancas` evolui de skill única para sistema portátil de engenharia assistida por agentes, mantendo o núcleo evidence-first e compatibilidade com o uso simples da pasta da skill.

Ciclo: **investigar → classificar → planejar → provar → implementar → revisar → verificar → aprender → melhorar**.

## Componentes

### Núcleo

`.agents/skills/verificar-mudancas/` continua sendo a fonte metodológica principal, com referências e playbooks carregados sob demanda.

### Orquestração e especialistas

`AGENTS.md` roteia os comandos canônicos em português e seleciona apenas os papéis necessários: investigador, diagnosticador de runtime, estrategista de testes, implementador, revisor de código, revisor de segurança, verificador de evidências e agente de aprendizado.

### Regras

`.agents/rules/` separa invariantes compartilhadas do conhecimento específico: evidência, testes, mudança segura, HIGH/CRITICAL e ambiente regulado.

### Hooks

`.agents/hooks/` define `pre-edit`, `post-edit` e `pre-finish`. `scripts/run_hook.py` oferece fallback executável para harnesses sem hooks nativos. Hooks são conservadores e não executam ações externas.

### Quality gate

`scripts/quality_gate.py` aceita configuração explícita ou detecta candidatos comuns. Sem `--execute`, apenas mostra o plano. Com execução autorizada produz `PASS`, `FAIL`, `PARTIAL`, `BLOCKED` ou `N/A` com evidência dos checks.

### Memória e continuous learning

`memory/` guarda `lesson`, `pattern` e `incident` sanitizados. `scripts/memory_store.py` valida privacidade, indexa e faz busca local. `agente-aprendizado` decide se uma conclusão merece proposta de memória, referência/playbook, regra ou eval. Nenhuma promoção para o core é automática.

Memória é sempre evidência histórica: nunca substitui investigação do caso atual.

### Adapters

`adapters/` contém `generic`, `codex`, `claude`, `devin` e `copilot`. Manifests usam `runtime-detect` quando a capacidade pode variar. `scripts/detect_capabilities.py` resolve apenas o que pode ser observado ou explicitamente informado e preserva fallback sequencial.

### Instalador

`scripts/install.py` suporta instalação `skill` ou `full`, adapter selecionado, dry-run e preservação de arquivos existentes por padrão. A instalação completa coloca runtime auxiliar em `.verificar-mudancas/` para não poluir scripts do projeto alvo.

### Observabilidade do sistema

`schemas/run.schema.json` define registro sanitizado de execução. `scripts/record_run.py` grava registros locais explicitamente fornecidos em `.verificar-mudancas/runs/`; não captura conteúdo automaticamente.

## Comandos canônicos

- `/verificar`: fluxo completo e proporcional ao risco.
- `/investigar`: diagnóstico sem edição.
- `/corrigir`: investigação + menor mudança correta + prova.
- `/revisar`: revisão adversarial de diff/mudança.
- `/validar`: claims versus evidência.
- `/portao-qualidade`: checks operacionais com execução explícita.
- `/aprender`: proposta sanitizada de aprendizado, sem auto-promoção.

## Segurança e stop conditions

O sistema bloqueia ou interrompe automação quando faltam elementos materiais, especialmente em HIGH/CRITICAL: ambiente/alvo, recuperação, aprovação humana quando requerida, blast radius, stop conditions ou evidência após a última mudança.

Nunca automatizar ação externa destrutiva apenas por inferência. Políticas locais mais restritivas prevalecem.

## Compatibilidade e degradação

Se subagentes não existirem, os papéis rodam sequencialmente. Se hooks não existirem, use o runner portátil. Se shell/filesystem não estiverem disponíveis, mantenha os controles como checklist explícito e marque o que não foi executado. Nenhum adapter pode fingir capability ausente.

## Evals e regressão

`evals/agentic/` cobre bug, memória/runtime, segurança, investigação-only, HIGH risk, memória como pista, sanitização de aprendizado, quality gate e degradação de adapter. Unit tests cobrem validadores, hooks, memória, quality gate, capabilities e instalador.

A/B continua sendo a forma de medir se o sistema melhora o mesmo modelo contra baseline sem a skill. Resultado negativo deve ser preservado.

## Status das fases do documento original

- v1.1 — schemas/arquitetura/compatibilidade: implementado.
- v1.5 — orquestrador e especialistas: implementado.
- v1.8 — regras, comandos e quality gate: implementado.
- v2.0 — hooks e capability detection: implementado com fallback portátil.
- v2.5 — memória e aprendizado controlado: implementado sem promoção automática.
- v3.0 — adapters e instalador: implementado.

A branch de desenvolvimento continua separada da `main`; merge/tag dependem de revisão e CI verde.
