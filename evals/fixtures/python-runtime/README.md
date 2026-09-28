# Fixture executável — Python runtime/parquet

Usa Python 3.12 no CI, `pandas==2.3.3` e `pyarrow==21.0.0` para validar dois pontos de `references/python.md`: dependência opcional/runtime e timezone.

## Executar

```bash
bash evals/fixtures/python-runtime/run.sh
```

O runner cria um venv descartável, gera um parquet com PyArrow, remove o PyArrow e executa `pandas.read_parquet` em um novo processo. A leitura **deve falhar** sem uma engine parquet instalada. Em seguida reinstala a versão pinada e exige leitura correta.

Também demonstra que o mesmo instante (`2026-09-28T02:30Z`) pertence a `2026-09-27` em `America/Sao_Paulo`, evitando tratar data UTC e data civil local como equivalentes.

## O que isso prova

- `pandas` sozinho não garante capacidade de ler parquet;
- a dependência precisa existir no ambiente que executa o código;
- incluir uma engine compatível altera o comportamento na fronteira real (`read_parquet`);
- timezone pode mudar a data civil para o mesmo instante.

## Limites

Não simula Lambda layer, wheel ARM64, manylinux, Glue/Spark ou packaging ZIP. Portanto a fixture sustenta a disciplina de runtime/dependência, mas não prova compatibilidade de um artifact AWS específico.
