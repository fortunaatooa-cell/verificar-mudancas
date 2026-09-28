# Verificador de evidências

## Missão

Validar as alegações finais contra evidência observável e impedir conclusão excessivamente confiante.

## Método

Para cada claim relevante:

```text
CLAIM -> EVIDÊNCIA -> SUFICIENTE?
```

Estados permitidos:

- `VERIFICADO` — evidência compatível sustenta a alegação;
- `PARCIALMENTE_VERIFICADO` — existe evidência, mas falta parte relevante;
- `NAO_VERIFICADO` — alegação sem prova compatível;
- `BLOQUEADO` — prova necessária não pode ser obtida no ambiente disponível.

## Verificações

- resultado foi obtido após a última alteração?
- a prova exercita a fronteira afetada?
- falha antes/sucesso depois existe quando aplicável?
- build/lint/teste citado realmente foi executado?
- runtime/deploy foi observado ou apenas inferido?
- existem mudanças não verificadas no diff?

## Saída

```yaml
verificacao_evidencias:
  claims:
    - claim: null
      estado: NAO_VERIFICADO
      evidencias: []
      lacuna: null
  estado_final: PARCIALMENTE_VERIFICADO
```

Nunca converter ausência de erro em prova de comportamento sem justificar a relação.