# Playbook: migração

Usar para schema, dados, infraestrutura, runtime, framework ou arquitetura quando versões/estados antigos e novos precisem coexistir ou a mudança possa ser difícil de reverter.

1. Definir origem, destino, compatibilidade, janela de coexistência e critério de conclusão.
2. Mapear dependências, consumidores, dados persistentes e ordem segura de passos/deploys.
3. Planejar dry run, backup/recuperação, rollback ou rollforward e stop conditions.
4. Testar transformação/migração em amostra ou ambiente representativo.
5. Executar incrementalmente quando autorizado e observar sinais definidos.
6. Reconciliar estado/dados após a mudança.
7. Remover compatibilidade temporária somente depois de confirmar que dependentes migraram.

Não executar etapa irreversível sem ambiente, alcance e recuperação claramente identificados.
