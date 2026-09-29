# Changelog

Todas as mudanças relevantes da `verificar-mudancas` devem ser registradas aqui. Enquanto o projeto estiver em evolução pré-1.0, mudanças de comportamento podem ocorrer em versões `0.x`, mas nunca devem ser publicadas sem eval ou fixture correspondente quando introduzirem uma nova regra de engenharia.

## Unreleased

### Added
- Capacidade de análise e especificação de desenhos técnicos/evidência visual, com separação entre observado, inferido e desconhecido, além de geração em formatos verificáveis quando a ferramenta suportar.
- Modos de resposta `simples`, `aprofundado` e `ambos`, mantendo alertas e incertezas materiais em qualquer nível de detalhe.
- Evals visuais para dimensões ilegíveis, limite de geração/renderização e resposta simplificada.
- Casos `obsolete-test-production-change` e `extracted-selector-unused` para revisão de teste obsoleto, severidade, ligação com o chamador e descoberta de ferramentas locais.
- Doze testes de regressão do validador, dependência de manutenção PyYAML e execução dos testes no CI.
- Política version-aware de evidência externa e sanitização de consultas.
- Fixture de runtime/port binding e evals que distinguem pesquisa necessária de pesquisa desnecessária.
- Base de adoção regulada: pacote de evidência de mudança, perfil regulado genérico e harness para A/B controlado.
- Runner executável de A/B para Codex CLI com workspaces isolados, sessões efêmeras, captura de respostas/logs/tempo e detecção de contaminação por skill global.
- Avaliação cega por `grading.csv` e analisador que gera `comparison.json` + `report.md` depois da pontuação.
- Smoke test com fake Codex para provar no CI que baseline não recebe a skill e o treatment recebe.

### Changed
- O núcleo agora trata `desenho técnico/visual` como tipo de tarefa e adapta a profundidade da resposta sem confundir brevidade com menor rigor.
- O núcleo passa a exigir descoberta de wrappers/toolchains locais antes de declarar ferramenta ausente, distinguir risco de severidade e justificar mudanças em produção ao adaptar testes obsoletos.
- Extração de lógica passa a pedir evidência na entrada/chamador afetados, com falha pelo defeito antes e sucesso depois quando viável; testes apenas do componente novo são evidência parcial.
- Runner Python passa a trabalhar em diretório temporário, sem sujar a fixture.
- Validação do repositório passa a proteger o orçamento do núcleo e arquivos de higiene.
- Helper de preparação A/B passa a expor funções reutilizáveis pelo runner executável.

### Fixed
- O validador agora interpreta YAML com carregador seguro e rejeita campos duplicados ou inválidos; tipos incorretos em IDs, modos e domínios dos casos produzem erros de validação em vez de traceback.

## Política de versão

- Fixar uso corporativo por tag ou commit aprovado; nunca por uma branch móvel.
- Antes de criar uma tag, exigir CI verde, changelog atualizado e revisão dos evals afetados.
- Mudança que altera comportamento esperado da skill deve mencionar os casos/evidências que a justificam.
