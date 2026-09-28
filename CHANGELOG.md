# Changelog

Todas as mudanças relevantes da `verificar-mudancas` devem ser registradas aqui. Enquanto o projeto estiver em evolução pré-1.0, mudanças de comportamento podem ocorrer em versões `0.x`, mas nunca devem ser publicadas sem eval ou fixture correspondente quando introduzirem uma nova regra de engenharia.

## Unreleased

### Added
- Política version-aware de evidência externa e sanitização de consultas.
- Fixture de runtime/port binding e evals que distinguem pesquisa necessária de pesquisa desnecessária.
- Base de adoção regulada: pacote de evidência de mudança, perfil regulado genérico e harness para A/B controlado.

### Changed
- Runner Python passa a trabalhar em diretório temporário, sem sujar a fixture.
- Validação do repositório passa a proteger o orçamento do núcleo e arquivos de higiene.

## Política de versão

- Fixar uso corporativo por tag ou commit aprovado; nunca por uma branch móvel.
- Antes de criar uma tag, exigir CI verde, changelog atualizado e revisão dos evals afetados.
- Mudança que altera comportamento esperado da skill deve mencionar os casos/evidências que a justificam.
