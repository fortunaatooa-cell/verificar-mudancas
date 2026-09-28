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

Por padrão, arquivos existentes são preservados. Use `--force` somente após revisar o dry-run. A instalação completa inclui núcleo, skills auxiliares, agentes/comandos/regras/hooks, schemas, adapter, scripts portáteis e estrutura de memória.

## Detectar capabilities

```bash
python3 scripts/detect_capabilities.py --adapter codex --root /caminho/do/projeto
```

Após instalação completa:

```bash
python3 .verificar-mudancas/scripts/detect_capabilities.py --adapter codex --root .
```

Capabilities não observáveis podem ser declaradas por `VM_CAP_WEB`, `VM_CAP_SUBAGENTS`, `VM_CAP_HOOKS`, `VM_CAP_MEMORY` e `VM_CAP_EXTERNAL_TOOLS`. Ausência de confirmação resulta em `unknown`.

## Quality gate

Primeiro planeje e depois, somente após revisar comandos, use `--execute`:

```bash
python3 .verificar-mudancas/scripts/quality_gate.py --root .
python3 .verificar-mudancas/scripts/quality_gate.py --root . --execute
```

Para uso corporativo, prefira configuração explícita `.verificar-mudancas/quality-gate.json` aprovada pelo time.

## Memória e regressão

```bash
python3 .verificar-mudancas/scripts/memory_store.py --root . search "OOM container"
```

Conhecimento específico do projeto pode usar `kind: project_knowledge`; mantenha-o somente no workspace autorizado. Para transformar uma memória sanitizada em proposta de regressão:

```bash
python3 .verificar-mudancas/scripts/create_regression_eval.py \
  --source memory/lessons/exemplo.json \
  --id regression-exemplo \
  --prompt "Investigue o caso" \
  --expected "verificar a fronteira correta" \
  --forbidden "assumir causa sem evidência"
```

O bundle sai como `REVIEW_REQUIRED`; revise antes de promovê-lo para um pack oficial.
