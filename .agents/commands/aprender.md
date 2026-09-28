# /aprender

Analisar uma tarefa concluída e propor aprendizado reutilizável sem alterar automaticamente o núcleo.

## Classificação

- específico do projeto → conhecimento local;
- ocorrência útil, ainda não recorrente → lesson;
- padrão observado em múltiplos contextos → pattern/reference;
- processo recorrente → playbook;
- princípio universal sustentado → rule/core;
- erro que não deve retornar → regression eval.

## Saída

```yaml
aprendizado:
  novidade: true
  categoria: lesson|pattern|reference|playbook|rule|eval
  proposta: null
  evidencias: []
  generalizacao: null
  riscos_de_overfit: []
```

Nunca promover dados de clientes, secrets, código proprietário ou identificadores internos para o repositório público.