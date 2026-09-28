# Memória de engenharia

Memória local e explícita para lessons, patterns, incidents e conhecimento de projeto sanitizado. Nada aqui é promovido automaticamente para o núcleo.

- `lessons/`: aprendizado de uma ocorrência.
- `patterns/`: padrão generalizado apoiado por recorrência/evidência.
- `incidents/`: casos reais anonimizados.
- `project/`: fatos específicos do projeto autorizado; JSON é ignorado pelo Git por padrão no repositório público.
- `index/index.json`: índice reconstruível.

Use `python3 scripts/memory_store.py` para validar, adicionar, reindexar e buscar. O utilitário exige `privacy.sanitized=true` e procura sinais óbvios de segredo antes de gravar.

Para transformar erro recorrente em regressão revisável, use `scripts/create_regression_eval.py`. A memória continua sendo pista histórica, não verdade do caso atual.
