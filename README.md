# Verificar Mudanças — Custom Skill para Microsoft 365 Copilot

Este branch distribui um pacote **Custom Skill** compatível com o botão **Carregar habilidade** do Agent Builder.

## Arquivo para upload

Use exatamente:

`verificar-mudancas-copilot365-skill-v3.1.zip`

O ZIP já contém `SKILL.md` na raiz, com `name` e `description` no YAML, além de referências auxiliares.

## Não use

Não use o ZIP da branch gerado pelo botão **Code → Download ZIP** como habilidade, porque ele adiciona uma pasta raiz extra. Use o arquivo de pacote acima.

## Validação do pacote

- `SKILL.md` na raiz do ZIP
- instruções da skill: 9.116 caracteres
- 12 arquivos no pacote
- ~11,5 KB
- profundidade máxima interna: 1
- sem scripts executáveis
- sem pressupor shell, Git, hooks ou subagentes

Fonte metodológica: `main` + extensões v3.1 da branch `feature/agentic-v1-5`.
