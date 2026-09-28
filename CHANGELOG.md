# Changelog

Todas as mudanças relevantes da `verificar-mudancas` devem ser registradas aqui. Enquanto o projeto estiver em evolução pré-1.0, mudanças de comportamento podem ocorrer em versões `0.x`, mas nunca devem ser publicadas sem eval ou fixture correspondente quando introduzirem uma nova regra de engenharia.

## Unreleased

### Added
- Arquitetura agentic completa em branch isolada: orquestração, oito papéis, comandos em português, regras, hooks e quatro skills auxiliares.
- Quality gate conservador com modo plano por padrão e execução explícita, além de config para validar o próprio repositório.
- Memória local sanitizada para lessons/patterns/incidents/project knowledge, índice reconstruível, busca e agente de aprendizado sem promoção automática.
- Gerador de eval de regressão revisável a partir de memória sanitizada, com oracle explícito obrigatório.
- Adapters `generic`, `codex`, `claude`, `devin` e `copilot` com capabilities declarativas, incluindo ferramentas externas, detecção conservadora e fallback sequencial.
- Instalador portátil com modos `skill`/`full`, `--dry-run`, seleção de adapter e preservação de arquivos existentes.
- Schemas para tarefa, investigação, evidência, resultado, memória, conhecimento de projeto, capabilities, hooks, quality gate e observabilidade de runs.
- Evals agentic para memória como pista, sanitização, quality gate e degradação de adapter, além de unit tests dos runners.
- Casos `obsolete-test-production-change` e `extracted-selector-unused` para revisão de teste obsoleto, severidade, ligação com o chamador e descoberta de ferramentas locais.
- Doze testes de regressão do validador, dependência de manutenção PyYAML e execução dos testes no CI.
- Política version-aware de evidência externa e sanitização de consultas.
- Fixture de runtime/port binding e evals que distinguem pesquisa necessária de pesquisa desnecessária.
- Base de adoção regulada: pacote de evidência de mudança, perfil regulado genérico e harness para A/B controlado.
- Runner executável de A/B para Codex CLI com workspaces isolados, sessões efêmeras, captura de respostas/logs/tempo e detecção de contaminação por skill global.
- Avaliação cega por `grading.csv` e analisador que gera `comparison.json` + `report.md` depois da pontuação.
- Smoke test com fake Codex para provar no CI que baseline não recebe a skill e o treatment recebe.

### Changed
- O núcleo passa a exigir descoberta de wrappers/toolchains locais antes de declarar ferramenta ausente, distinguir risco de severidade e justificar mudanças em produção ao adaptar testes obsoletos.
- Extração de lógica passa a pedir evidência na entrada/chamador afetados, com falha pelo defeito antes e sucesso depois quando viável; testes apenas do componente novo são evidência parcial.
- Runner Python passa a trabalhar em diretório temporário, sem sujar a fixture.
- Validação do repositório passa a proteger o orçamento do núcleo e arquivos de higiene.
- Helper de preparação A/B passa a expor funções reutilizáveis pelo runner executável.
- Validação agentic passa a cobrir núcleo auxiliar, agentes, comandos, regras, hooks, memória, adapters, schemas, scripts e casos de regressão.

### Fixed
- O validador agora interpreta YAML com carregador seguro e rejeita campos duplicados ou inválidos; tipos incorretos em IDs, modos e domínios dos casos produzem erros de validação em vez de traceback.

## Política de versão

- Fixar uso corporativo por tag ou commit aprovado; nunca por uma branch móvel.
- Antes de criar uma tag, exigir CI verde, changelog atualizado e revisão dos evals afetados.
- Mudança que altera comportamento esperado da skill deve mencionar os casos/evidências que a justificam.
