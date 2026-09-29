# Verificar Mudanças — Devin Plugin v3.1

Distribuição específica para instalar o Verificar Mudanças no Devin **sem copiar a skill para cada repositório**.

## Arquivo para upload

Use exatamente:

`verificar-mudancas-devin-plugin-v3.1.zip`

## Instalação

No Devin Web:

1. Abra **Customize**.
2. Vá em **Plugins**.
3. Clique em **Add plugin**.
4. Escolha **Upload .zip**.
5. Selecione `verificar-mudancas-devin-plugin-v3.1.zip`.
6. Instale no escopo **Personal** se for apenas para você. Organization/Enterprise dependem de permissão administrativa.
7. Abra uma **nova sessão** após a instalação.

## Uso

Skill principal:

`/verificar-mudancas:verificar`

Skills focadas:

- `/verificar-mudancas:investigar`
- `/verificar-mudancas:planejar`
- `/verificar-mudancas:arquitetura`
- `/verificar-mudancas:tdd`
- `/verificar-mudancas:revisar`
- `/verificar-mudancas:seguranca`
- `/verificar-mudancas:runtime`
- `/verificar-mudancas:desenho`

O plugin também inclui um `AGENTS.md` compacto como regra sempre ativa para reforçar evidence-first, risco, verificação e prevenção de falsa confiança mesmo quando um modelo mais barato estiver em uso.

## Estrutura do ZIP

- `.devin-plugin/plugin.json`
- `AGENTS.md`
- `skills/verificar/SKILL.md`
- 8 skills focadas
- `README.md`

## Fonte metodológica

Baseado em `feature/agentic-v1-5`, incluindo planejamento, arquitetura, TDD, ADR, review, segurança, runtime/performance e desenhos técnicos.

O plugin não altera permissões de repositórios. Ele funciona em qualquer projeto ao qual a sessão do Devin já tenha acesso.