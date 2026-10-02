# Verificar Mudanças — orquestração agentic

Este repositório usa `.agents/skills/verificar-mudancas/SKILL.md` como núcleo metodológico. Skills auxiliares, agentes, regras, hooks, memória e adapters complementam o núcleo; não o substituem.

## Interface canônica em português

- `/verificar`
- `/investigar`
- `/planejar`
- `/arquitetura`
- `/tdd`
- `/adr`
- `/corrigir`
- `/revisar`
- `/validar`
- `/portao-qualidade`
- `/aprender`
- `/desenho-tecnico`
- `/depurar-jogo`

## Bootstrap

1. Leia a skill principal.
2. Detecte capabilities quando a superfície for desconhecida.
3. Aplique somente regras pertinentes.
4. Carregue skills auxiliares sob demanda: `investigar`, `planejamento`, `arquitetura`, `estrategia-testes`, `revisar-mudanca`, `diagnosticar-runtime`, `desenho-tecnico`.
5. Memória histórica é pista, não verdade atual.
6. Respeite `simples`, `aprofundado` ou `ambos`.

## Roteamento

Correção base: `investigador → estrategista-testes → implementador → revisor-codigo → verificador-evidencias`.

Mudança ampla, multi-componente, migração ou dependências relevantes: incluir `planejador` antes da implementação.

Novo serviço, integração estrutural, fronteira de dados, alteração difícil de reverter ou pedido de arquitetura: incluir `arquiteto`. O arquiteto reconstrói estado atual antes de propor futuro e pode chamar `analista-desenhos-tecnicos`.

TDD é modo do `estrategista-testes`, não agente separado. Só declarar TDD com evidência de RED antes da implementação.

Decisão arquitetural material/durável: usar `/adr`; ADR registra decisão, não prova implantação.

Runtime/recursos: incluir `diagnosticador-runtime`. Segurança pertinente: incluir `revisor-seguranca`. Visual/desenho: incluir `analista-desenhos-tecnicos`, respeitando `vision_input` e `visual_generation`.

Bug de jogo/runtime interativo: usar `/depurar-jogo`; incluir `investigador-gameplay` para reprodução/redução e `validador-regressao-jogo` após a implementação. Eles especializam o fluxo geral e não substituem `investigador`, `estrategista-testes` ou `verificador-evidencias`.

Aprendizado: `agente-aprendizado` propõe; não promove automaticamente.

Sem subagentes, executar os mesmos papéis sequencialmente.

## Invariantes

- evidência antes de confiança;
- fato ≠ hipótese ≠ inferência ≠ desconhecido;
- arquitetura observada ≠ proposta ≠ implantada;
- ADR ≠ prova de runtime;
- nunca alegar TDD sem RED anterior demonstrável;
- nunca alegar execução, visão ou render inexistentes;
- menor mudança correta;
- HIGH/CRITICAL exigem blast radius, recuperação, stop conditions e sinais;
- dados corporativos, secrets e código proprietário não entram no repositório público.

Specs: `docs/agentic-system.md` e `docs/spec-v3-1-engineering-lifecycle.md`.
