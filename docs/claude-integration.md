# Integração com Claude Code

Esta integração atualiza o adapter existente do Claude sem criar novos papéis conceituais. Os mesmos comandos, agentes e regras portáteis são expostos pelas superfícies nativas atuais do Claude Code.

## Arquitetura

```text
fontes canônicas
AGENTS.md + .agents/
        |
        +-- scripts/claude_native.py
        |
        +--> CLAUDE.md
        +--> .claude/skills/
        +--> .claude/agents/
        +--> .claude/rules/
        +--> .claude/settings.json
```

Os wrappers gerados não devem ganhar lógica independente. Se a metodologia mudar, altere primeiro o arquivo portátil e regenere/atualize a superfície Claude.

## Skills

Cada comando canônico existente possui uma skill em `.claude/skills/<nome>/SKILL.md`. O núcleo também existe como `.claude/skills/verificar-mudancas/SKILL.md`.

Exemplos:

- `/investigar`: análise sem edição;
- `/corrigir`: diagnóstico, menor correção e verificação;
- `/revisar`: revisão adversarial;
- `/depurar-jogo`: especialização de gameplay já existente.

As skills de comando usam `disable-model-invocation: true` e **não usam `allowed-tools` para pré-aprovar Bash/Edit/Write**. Assim, os comandos ficam explícitos no menu `/`, enquanto a skill principal `verificar-mudancas` continua descobrível automaticamente e `/corrigir` ou `/depurar-jogo` não contornam o fluxo normal de permissões do Claude Code.

## Subagents

Os papéis existentes em `.agents/agents/` são mapeados para `.claude/agents/`. Cada subagent pré-carrega a skill `verificar-mudancas`, usando o suporte atual de `skills` no frontmatter. A sessão principal continua sendo o orquestrador e integra as conclusões. Especialistas recebem ferramentas proporcionais: investigação/revisão são mais restritivas; o implementador pode editar.

Use paralelismo somente quando as subtarefas forem realmente independentes. Dependências causais continuam sequenciais.

## Hooks

`.claude/settings.json` conecta:

- `SessionStart`: informa que o harness está ativo;
- `PreToolUse`: aplica guardrails determinísticos em Bash/Write/Edit;
- `PostToolUse`: lembra a revalidar fronteiras depois de alterações.

O bridge bloqueia `Write/Edit` quando `VM_MODE=investigation-only`. Também bloqueia comandos destrutivos de alta confiança sem `VM_HUMAN_APPROVED=true`. Isso complementa, não substitui, as permissões e o sandbox do Claude Code.

## Recursos recentes

O adapter está preparado para detectar em runtime workflows dinâmicos, plugins e sincronização de conta, sem depender deles para funcionar. Recursos que alterem o modelo de execução ou carreguem código adicional continuam opt-in.

Mods/plugins com código executável não são habilitados automaticamente nesta branch. A Spec 10/10 mantém a orquestração agentic experimental até T8/T14; adotar outro sistema agora confundiria consistência interna com eficácia comprovada.

## Instalação

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full
```

Sem `--force`, arquivos preexistentes como `CLAUDE.md` e `.claude/settings.json` são preservados.

## Validação

```bash
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_agentic.py
python3 scripts/validate_repo.py
```

`tests/test_claude_native.py` impede drift entre os wrappers Claude versionados e as fontes portáteis.

Ao alterar um comando/agente/regra portátil nesta branch, regenere os wrappers versionados:

```bash
python3 scripts/claude_native.py
```

O teste anti-drift falha se a versão nativa ficar diferente da fonte canônica.
