# Verificar Mudanças — Devin Workspace v3.1

Pacote de distribuição específico para **Devin**, baseado no estado atual do sistema agentic v3.1.

## O que inclui

- `AGENTS.md` — orquestração do workspace;
- `.agents/skills/verificar-mudancas/` — skill principal;
- 8 skills especializadas: investigação, planejamento, arquitetura, testes/TDD, review, segurança, runtime e desenho técnico;
- referências para APIs/dados/cloud, performance/SRE, Java/Python, segurança, desenhos e evidência;
- `devin/repo-setup/ADDITIONAL_NOTES.txt`;
- templates de Playbooks para `!verificar`, `!investigar`, `!planejar`, `!arquitetura`, `!tdd`, `!revisar`, `!runtime`, `!desenho`;
- Knowledge condensado opcional;
- testes de aceite.

## Instalação recomendada

1. Descompacte o ZIP na **raiz do repositório** usado pelo Devin.
2. Confirme que existe `.agents/skills/verificar-mudancas/SKILL.md`.
3. Em Settings → Devin's Machine → Repo Setup, configure os comandos reais do projeto.
4. Cole `devin/repo-setup/ADDITIONAL_NOTES.txt` em Additional Notes.
5. Opcional: crie os macros em Settings → Playbooks usando os arquivos em `devin/playbooks/`.
6. Rode os testes de `devin/acceptance-tests/TESTES.md`.

O ZIP é um **workspace overlay**, não um formato mágico de importação. Se sua interface tiver um upload de workspace, use-o somente se ele preservar a estrutura de diretórios. O caminho `.agents/skills/` é a parte essencial.

## Segurança

Não inclua secrets no pacote. Configure credenciais em Settings → Secrets no Devin.
