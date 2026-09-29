# Verificar Mudanças — Custom Skill para Microsoft 365 Copilot

Este branch distribui um pacote **Custom Skill** compatível com o botão **Carregar habilidade** do Agent Builder.

## Arquivo para upload

Use exatamente:

`verificar-mudancas-copilot365-skill-v3.1.zip`

O arquivo acima já contém a revisão **R2** da skill, mantendo o mesmo nome para que o link de download continue estável.

## O que há dentro

- `SKILL.md` na raiz, com `name` e `description` no YAML;
- corpo de instruções com **16.135 caracteres**, abaixo do limite de 20.000 caracteres da Custom Skill;
- **460 linhas** no corpo do `SKILL.md`;
- 14 referências especializadas em `references/`;
- 15 arquivos no total;
- aproximadamente 30 mil caracteres de conteúdo textual distribuído por divulgação progressiva;
- sem scripts executáveis e sem pressupor shell, Git, hooks ou subagentes.

## Áreas cobertas

Investigação, planejamento, arquitetura, ADR, TDD, testes, revisão de código, segurança, runtime, memória/CPU, performance, observabilidade/SRE, APIs, dados, sistemas distribuídos, cloud/Terraform/CI/CD, Java/Spring, Python, desenhos técnicos, evidência final e aprendizado controlado.

## Como usar

No Microsoft 365 Copilot Agent Builder, abra **Habilidades → Adicionar/Carregar habilidade** e selecione diretamente `verificar-mudancas-copilot365-skill-v3.1.zip`.

**Não use** o ZIP automático de `Code → Download ZIP` do GitHub, porque ele envolve os arquivos em uma pasta externa. Use o arquivo acima.

Fonte metodológica: `main` + extensões v3.1 da branch `feature/agentic-v1-5`.
