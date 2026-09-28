# Hook `pre-edit`

Use antes de edição material. LOW pode receber aviso; HIGH/CRITICAL bloqueiam quando faltarem critérios de aceite, alvo/ambiente ou plano de recuperação quando aplicável. Em investigação-only, editar é bloqueado.

Exemplo:

```bash
python3 scripts/run_hook.py pre-edit --payload-file task.json
```
