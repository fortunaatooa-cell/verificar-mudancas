# Dados e pipelines

Ler quando a mudança envolver SQL, ETL/ELT, Spark, Glue, ingestão por eventos, CDC, migração, relatórios ou qualidade de dados. Definir antes de editar: fonte e destino, esquema, granularidade, chave, janela temporal, nulos e contrato de consumo.

## Distinguir causa de sintoma

- Reconstruir um registro de ponta a ponta: origem → extração/evento → transformação → carga → consulta/consumidor. Identificar o primeiro estágio da divergência e a versão dos dados/código.
- Analisar duplicatas, mudanças de schema, valores nulos, late arrivals, fuso horário, watermark, correções retroativas, retries, falhas parciais, replay, ordering e entrega ao menos uma vez quando houver eventos.
- Em CDC/filas, verificar o identificador de evento, chave de negócio, operação (insert/update/delete), ordem, checkpoint e idempotência do destino. Não supor que a criação de um lote implica disponibilidade imediata em todo downstream.

## Provar e reconciliar

- Preparar amostras com caso normal, duplicado, ausente, fora de ordem, reprocessado e limite de janela **quando relevantes ao defeito**. Verificar idempotência executando o mesmo lote/evento novamente em ambiente permitido.
- Comparar esquema, contagens, soma de medidas relevantes e chaves entre fonte independente e destino, com filtros/janelas explicitados. Contagem idêntica sozinha pode ocultar substituições e duplicatas compensadas.
- Para migração/backfill, planejar dry run, alcance, reversão e validação antes/depois. Não executar escrita destrutiva nem usar dados sensíveis em exemplos públicos sem autorização.

## Entrega específica

Registrar janela, fonte de verdade, consulta ou procedimento de reconciliação, diferenças encontradas e limites de ambiente. Separar validade lógica em amostra de qualidade histórica completa.
