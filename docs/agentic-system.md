# SPEC implementada — Verificar Mudanças Agentic Engineering System

## Visão

A `verificar-mudancas` é um sistema portátil de engenharia assistida por agentes, evidence-first e compatível com uso simples da skill ou instalação completa.

Ciclo ampliado: **entender → planejar → arquitetar quando necessário → investigar → provar/TDD → implementar → revisar → verificar → aprender → melhorar**.

## Componentes principais

### Núcleo e skills auxiliares

A skill principal continua sendo a fonte metodológica. A instalação completa adiciona `investigar`, `planejamento`, `arquitetura`, `estrategia-testes`, `revisar-mudanca`, `diagnosticar-runtime` e `desenho-tecnico`.

### Especialistas

O orquestrador pode selecionar investigador, planejador, arquiteto, diagnosticador de runtime, estrategista de testes, implementador, revisores, verificador de evidências, aprendizado e analista de desenhos técnicos. Sem subagentes, os papéis rodam sequencialmente.

### Engineering Lifecycle v3.1

A spec detalhada está em `docs/spec-v3-1-engineering-lifecycle.md`.

- `planejador` decompõe trabalho amplo sem inventar requisito;
- `arquiteto` reconstrói estado atual e compara alternativas por trade-offs;
- TDD é modo do estrategista de testes: `RED → GREEN → REFACTOR → REGRESSION`;
- ADR registra decisões materiais e não é tratado como prova de implementação;
- arquitetura pode compor com análise/criação de desenhos técnicos.

### Desenhos técnicos e visual

`vision_input` e `visual_generation` são capabilities independentes. O sistema separa observado, inferido e não determinável, evita falsa precisão e usa Mermaid/PlantUML/DOT/SVG/CAD ou render conforme a capacidade real.

### Modos de resposta

`simples`, `aprofundado` e `ambos`. Simplificar a linguagem não reduz requisitos de evidência, segurança ou incerteza material.

### Regras, hooks, quality gate, memória e adapters

Regras compartilhadas cobrem evidence-first, testing/TDD, decisões arquiteturais, segurança operacional, risco e visual. Hooks e quality gate possuem fallback portátil. Memória é sanitizada e histórica. Adapters `generic`, `codex`, `claude`, `devin` e `copilot` usam capability detection.

## Comandos canônicos

`/verificar`, `/investigar`, `/planejar`, `/arquitetura`, `/tdd`, `/adr`, `/corrigir`, `/revisar`, `/validar`, `/portao-qualidade`, `/aprender`, `/desenho-tecnico`.

## Evals

`evals/agentic/` cobre a arquitetura geral; `evals/visual/` protege análise visual e modos de resposta; `evals/lifecycle/` protege planejamento, trade-offs de arquitetura, TDD verdadeiro/falso, ADR e divergência desenho × implementação.

## Status

- v1.1 a v3.0: implementados;
- extensão visual: implementada;
- v3.1 Engineering Lifecycle: implementada no primeiro corte com planejamento, arquitetura, TDD e ADR;
- v3.2: candidata futura para performance, observabilidade/SRE e dados/banco após evidência de necessidade.
