# SPEC implementada — Verificar Mudanças Agentic Engineering System

## Visão

A `verificar-mudancas` evolui de skill única para sistema portátil de engenharia assistida por agentes, mantendo núcleo evidence-first e compatibilidade com o uso simples da pasta da skill.

Ciclo: **investigar → classificar → planejar → provar → implementar → revisar → verificar → aprender → melhorar**.

## Componentes

### Núcleo e skills auxiliares

`.agents/skills/verificar-mudancas/` continua sendo a fonte metodológica principal. A instalação completa fornece `investigar`, `estrategia-testes`, `revisar-mudanca`, `diagnosticar-runtime` e `desenho-tecnico`.

### Orquestração e especialistas

`AGENTS.md` roteia comandos em português e seleciona somente os papéis necessários: investigador, runtime, testes, implementação, código, segurança, evidências, aprendizado e análise de desenhos técnicos.

### Desenhos técnicos e visual

O sistema trata entrada e saída visual como capacidades independentes. `vision_input` permite afirmar inspeção de imagem real; `visual_generation` permite afirmar render/criação visual. Ambas podem variar por harness e são `runtime-detect` nos adapters.

`analista-desenhos-tecnicos` e a skill auxiliar `desenho-tecnico` usam `references/technical-drawings.md` para:

- identificar tipo, finalidade, revisão, escala, unidades, legenda e vistas;
- inventariar componentes, conexões, cotas e anotações por região/camada;
- separar observado, inferido e não determinável;
- fazer cross-check com código/especificação quando disponível;
- criar fonte editável em Mermaid/PlantUML/DOT/SVG/CAD conforme capacidade;
- impedir falsa precisão e falsa alegação de renderização.

### Modos de resposta

`references/response-modes.md` define `simples`, `aprofundado` e `ambos`. O modo simples reduz detalhe, não requisitos de evidência, segurança ou incerteza material.

### Regras, hooks e quality gate

`.agents/rules/` inclui evidência, testes, mudança segura, HIGH/CRITICAL, ambiente regulado e evidência visual. Hooks `pre-edit`, `post-edit` e `pre-finish` possuem runner portátil. `quality_gate.py` planeja por padrão e só executa com `--execute`.

### Memória e continuous learning

`memory/` guarda `lesson`, `pattern`, `incident` e `project_knowledge` sanitizados. Memória é hipótese histórica. `create_regression_eval.py` exige oracle explícito e gera bundle revisável; não há auto-promoção ao core.

### Adapters e capabilities

`generic`, `codex`, `claude`, `devin` e `copilot` declaram `repository_read`, `repository_write`, `shell`, `web`, `subagents`, `hooks`, `persistent_memory`, `external_tools`, `vision_input` e `visual_generation`. `detect_capabilities.py` mantém `unknown` quando não há prova e aplica fallback sequencial/textual.

### Instalador e observabilidade

`install.py` suporta `skill` ou `full`; o modo full instala também o especialista visual. `record_run.py` registra execução sanitizada explicitamente fornecida; não captura conteúdo automaticamente.

## Comandos

- `/verificar` — fluxo completo.
- `/investigar` — diagnóstico sem edição.
- `/corrigir` — investigação + correção + prova.
- `/revisar` — revisão adversarial.
- `/validar` — claims versus evidência.
- `/portao-qualidade` — checks operacionais.
- `/aprender` — aprendizado sanitizado.
- `/desenho-tecnico` — analisar, revisar, criar ou redesenhar artefato técnico visual.

## Segurança e degradação

HIGH/CRITICAL exigem blast radius, recuperação, stop conditions, sinais e aprovação humana quando aplicável. Sem subagentes, papéis rodam sequencialmente; sem hooks, use runner portátil; sem visão, não alegue inspeção; sem geração visual, entregue fonte/especificação e marque o render como não executado.

Em desenho mecânico, elétrico, civil, industrial ou de segurança, a análise é assistiva e não substitui validação por profissional habilitado/certificação normativa.

## Evals

`evals/agentic/` cobre bug, runtime/memória, segurança, investigação-only, HIGH risk, memória como pista, sanitização, quality gate, adapter degradation e os fluxos visuais. `evals/visual/` cobre falsa precisão, fallback de geração e modo simples. Unit tests cobrem validadores, capabilities, installer e demais runners.

## Status das fases

- v1.1 — schemas/arquitetura/compatibilidade: implementado.
- v1.5 — orquestrador e especialistas: implementado.
- v1.8 — regras, comandos e quality gate: implementado.
- v2.0 — hooks e capability detection: implementado com fallback portátil.
- v2.5 — memória, project knowledge, retrieval e aprendizado/regressão controlados: implementado.
- v3.0 — adapters e instalador: implementado.
- extensão visual — desenho técnico, visão/render capability e modos de resposta: implementado.
