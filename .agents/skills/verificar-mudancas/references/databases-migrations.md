# Bancos e migrações

Usar quando a mudança envolver schema, índices, constraints, transações, queries, backfill ou dados persistentes. O objetivo é proteger compatibilidade, integridade e operação durante a mudança.

## Antes de editar
- Identificar banco, versão, tamanho aproximado da tabela, padrão de acesso, caminho de deploy e ferramenta de migração realmente usada.
- Verificar impacto em locks, índices, constraints, tempo de execução, replicação, backups e consumidores em versões diferentes.
- Para rolling ou blue/green, assumir que versões antiga e nova podem coexistir e planejar schema compatível com essa janela.

## Provar
- Testar forward migration e, quando rollback não for seguro, definir rollforward explícito. Não prometer reversão automática para transformação destrutiva de dados.
- Verificar integridade por chaves, constraints e amostras/reconciliação relevantes; contagem igual sozinha não prova equivalência.
- Em performance, observar plano de execução, cardinalidade, índices e número de queries quando a mudança tocar acesso a dados.
- Para backfill, definir lote, idempotência, retomada, limite de carga e critério de conclusão.

## Stop conditions
- Parar antes de executar quando houver perda potencial de dados, lock amplo inesperado, ausência de backup/recovery para mudança irreversível ou ambiente não identificado.

## Entrega específica
Relatar migração, compatibilidade entre versões, estratégia de recuperação, evidência de integridade e efeitos operacionais não verificados.
