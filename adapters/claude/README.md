# Adapter Claude Code

O adapter Claude usa os mecanismos nativos atuais do Claude Code sem substituir a fonte portátil do projeto.

## Mapeamento nativo

- `CLAUDE.md` mantém somente bootstrap, invariantes e roteamento de alto nível.
- `.claude/skills/<nome>/SKILL.md` expõe o núcleo e os comandos existentes como skills nativas; skills são o mecanismo preferido em vez de duplicar comandos legados.
- `.claude/agents/*.md` mapeia os mesmos papéis portáteis para subagents com contexto separado e conjunto de ferramentas proporcional.
- `.claude/rules/*.md` espelha as regras portáteis com carregamento progressivo.
- `.claude/settings.json` conecta hooks determinísticos de `SessionStart`, `PreToolUse` e `PostToolUse`.
- `scripts/claude_hook_bridge.py` bloqueia edição em `VM_MODE=investigation-only` e comandos destrutivos conhecidos sem aprovação explícita.

A sessão principal continua responsável por integrar resultados, resolver conflitos entre especialistas e validar a conclusão. Subagents devem receber tarefas isoláveis; tarefas independentes podem ser paralelizadas quando a instalação do Claude permitir.

## Instalação

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full
```

Arquivos existentes são preservados sem `--force`. O instalador gera os wrappers nativos a partir dos arquivos portáteis, para evitar duas fontes de verdade.

## Atualizações recentes do Claude

O desenho reconhece as superfícies atuais de Skills, subagents, rules e hooks, além de workflows dinâmicos quando disponíveis. Sincronização de skills/plugins da conta pode existir em versões recentes, mas o repositório não depende dela: a instalação local continua determinística.

Plugins/mods podem ampliar o Claude Code, porém **não são instalados automaticamente nesta branch**. Mods recentes executam código com acesso da máquina e a Spec 10/10 proíbe adicionar novos sistemas antes de T8; qualquer adoção fica explícita e adiada para T14.

Quando uma capability não puder ser observada, mantenha `runtime-detect`/fallback e nunca assuma suporte apenas pela versão.
