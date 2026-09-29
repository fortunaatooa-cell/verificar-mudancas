# Verificar Mudanças — Devin Workspace v3.1

Branch de distribuição específica para **Devin**, baseada em `feature/agentic-v1-5` no commit `6a2c3d8a682a4debb27cba80a346dc9d2fa80268`.

## Arquivo para usar amanhã

Baixe `verificar-mudancas-devin-workspace-v3.1.zip`.

O ZIP é um **workspace overlay**: descompacte-o na raiz do repositório que o Devin vai editar. Ele cria `AGENTS.md`, `.agents/skills/` e a pasta `devin/` sem exigir que o Devin trate um ZIP como uma skill única.

## O que existe no pacote

- skill principal `verificar-mudancas`;
- skills de investigação, planejamento, arquitetura, testes/TDD, review, segurança, runtime e desenho técnico;
- referências de APIs/dados/cloud, performance/SRE, Java/Python, evidências e anti-padrões;
- `AGENTS.md` para orquestração no workspace;
- `devin/repo-setup/ADDITIONAL_NOTES.txt` pronto para o Repo Setup;
- 8 templates de Playbooks para Settings → Playbooks;
- Knowledge condensado opcional;
- testes de aceite para validar o comportamento.

## Instalação recomendada

1. Descompacte o ZIP na raiz do repositório do projeto.
2. Confirme `.agents/skills/verificar-mudancas/SKILL.md`.
3. Em Settings → Devin's Machine → Repo Setup, mantenha os comandos reais de pull/dependências/lint/test/app do projeto.
4. Cole `devin/repo-setup/ADDITIONAL_NOTES.txt` em Additional Notes.
5. Opcionalmente crie macros em Settings → Playbooks usando `devin/playbooks/`.
6. Rode `devin/acceptance-tests/TESTES.md` em um sandbox/repo de teste antes do uso real.

## Importante

O ZIP é transporte e overlay. A parte nativa mais importante para skills locais é `.agents/skills/`. Não coloque segredos no pacote; use Settings → Secrets.
