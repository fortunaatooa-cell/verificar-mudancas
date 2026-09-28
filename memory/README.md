# Memória de engenharia

Memória local e explícita para lessons, patterns e incidents sanitizados. Nada aqui é promovido automaticamente para o núcleo.

- `lessons/`: aprendizado de uma ocorrência.
- `patterns/`: padrão generalizado apoiado por mais de uma evidência ou revisão explícita.
- `incidents/`: casos reais anonimizados.
- `index/index.json`: índice reconstruível.

Use `python3 scripts/memory_store.py` para validar, adicionar, reindexar e buscar. O utilitário recusa documentos não marcados como sanitizados e procura sinais óbvios de segredo antes de gravar.
