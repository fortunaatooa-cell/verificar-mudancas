# Instalação

## Somente skill

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter generic --mode skill --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter generic --mode skill
```

## Sistema completo

Escolha `generic`, `codex`, `claude`, `devin` ou `copilot`:

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter codex --mode full --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter codex --mode full
```

Por padrão, arquivos existentes são preservados. Use `--force` somente após revisar o dry-run.

A instalação completa coloca skill/agentes/comandos/regras/hooks em `.agents/`, schemas/adapter/scripts portáteis em `.verificar-mudancas/` e a estrutura local de `memory/`.

## Detectar capabilities

```bash
python3 scripts/detect_capabilities.py --adapter codex --root /caminho/do/projeto
```

Após instalação completa:

```bash
python3 .verificar-mudancas/scripts/detect_capabilities.py --adapter codex --root .
```

Capabilities não observáveis podem ser declaradas pelo ambiente (`VM_CAP_WEB`, `VM_CAP_SUBAGENTS`, `VM_CAP_HOOKS`, `VM_CAP_MEMORY`). Ausência de confirmação resulta em `unknown`.

## Quality gate

Primeiro planeje:

```bash
python3 .verificar-mudancas/scripts/quality_gate.py --root .
```

Depois de revisar os comandos:

```bash
python3 .verificar-mudancas/scripts/quality_gate.py --root . --execute
```

Para uso corporativo, prefira configuração explícita `.verificar-mudancas/quality-gate.json` aprovada pelo time.

## Memória

```bash
python3 .verificar-mudancas/scripts/memory_store.py --root . search "OOM container"
```

Adicionar memória é ação explícita e exige conteúdo sanitizado.
