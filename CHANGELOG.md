# Changelog

Todas as mudanças relevantes da `verificar-mudancas` devem ser registradas aqui. Enquanto o projeto estiver em evolução pré-1.0, mudanças de comportamento podem ocorrer em versões `0.x`, mas nunca devem ser publicadas sem eval ou fixture correspondente quando introduzirem uma nova regra de engenharia.

## Unreleased

### Added
- Implementação da Spec 10/10 na branch experimental: observação real do tratamento, denominador fixo por oracle, falhas como não-vitória, efeito mínimo versionado/hashado, experimento de descobribilidade separado, fontes por item do oracle, scanner de dados sensíveis e gates do piloto regulado.
- Gate de revisão humana independente para rodadas A/B reais, com hashes normalizados de `cases.json`/`oracle.json`, template verificável e modo `--smoke-test` explicitamente não publicável como evidência de eficácia.
- Documento `docs/maturity.md` separando maturidade do harness, prova A/B e piloto real.
- Especialização agentic para bugs de jogos: `investigador-gameplay`, `validador-regressao-jogo`, comando `/depurar-jogo` e playbook `game-bug`, reutilizando o mesmo harness e as referências de engine existentes.
- Capacidade de análise, revisão e especificação de desenhos técnicos com especialista `analista-desenhos-tecnicos`, skill auxiliar `desenho-tecnico`, comando `/desenho-tecnico` e regra de evidência visual.
- Capabilities `vision_input` e `visual_generation` independentes em todos os adapters, com fallback textual/editável quando visão ou render não estiverem disponíveis.
- Modos de resposta `simples`, `aprofundado` e `ambos` aplicáveis a engenharia e desenhos técnicos.
- Evals visuais e agentic para falsa precisão, ausência de escala/cotas, geração sem render e resposta simplificada.
- Arquitetura agentic completa em branch isolada: orquestração, especialistas, comandos em português, regras, hooks e skills auxiliares.
- Quality gate conservador com modo plano por padrão e execução explícita.
- Memória local sanitizada para lessons/patterns/incidents/project knowledge e agente de aprendizado sem promoção automática.
- Gerador de eval de regressão revisável com oracle explícito obrigatório.
- Adapters `generic`, `codex`, `claude`, `devin` e `copilot` com detecção conservadora e fallback sequencial.
- Instalador portátil com modos `skill`/`full`, `--dry-run` e preservação de arquivos existentes.
- Schemas para tarefa, investigação, evidência, resultado, memória, conhecimento de projeto, capabilities, hooks, quality gate e observabilidade.
- Casos `obsolete-test-production-change` e `extracted-selector-unused`, fixtures de runtime e harness A/B controlado.

### Changed
- O núcleo trata `desenho técnico/visual` como tipo de tarefa e adapta profundidade da resposta sem confundir brevidade com menor rigor.
- O instalador full inclui a skill de desenho técnico; a validação agentic exige especialista, regra, comando, evals e capabilities visuais.
- O núcleo exige descoberta de wrappers/toolchains locais antes de declarar ferramenta ausente, distingue risco de severidade e reforça prova na fronteira afetada.

### Fixed
- O validador aceita checkouts CRLF do Windows sem alterar a semântica do frontmatter nem inflar artificialmente o orçamento do `SKILL.md`.
- O validador interpreta YAML com carregador seguro e rejeita campos duplicados/ inválidos sem traceback.

## Política de versão

- Fixar uso corporativo por tag ou commit aprovado; nunca por branch móvel.
- Antes de criar tag, exigir CI verde, changelog atualizado e revisão dos evals afetados.
- Mudança comportamental deve mencionar os casos/evidências que a justificam.
