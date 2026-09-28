# Playbook: bug fix

Usar quando existe comportamento observado diferente do esperado.

1. Reproduzir ou reunir evidência discriminante do defeito.
2. Definir critério de aceite e fronteira afetada.
3. Formular hipótese principal e ao menos uma alternativa quando houver ambiguidade.
4. Criar prova que falhe pelo motivo esperado quando útil e viável.
5. Aplicar a menor correção sustentada pela evidência.
6. Rodar prova antes/depois e cenário vizinho de regressão; se houver componente novo, exercitar também sua ligação com a entrada original, conforme o critério de conclusão do núcleo.
7. Revisar diff, risco, compatibilidade e efeitos colaterais.
8. Verificar novamente após a última alteração e registrar causa confirmada ou incerteza remanescente.

Não transformar bug fix em refatoração ampla sem necessidade demonstrada.
