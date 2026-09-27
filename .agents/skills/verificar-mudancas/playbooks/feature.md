# Playbook: feature

Usar quando a tarefa adiciona comportamento novo.

1. Traduzir a solicitação em critérios de aceite observáveis e fora de escopo explícito.
2. Identificar contratos, dados, permissões e consumidores afetados.
3. Escolher a menor arquitetura consistente com padrões existentes.
4. Criar testes a partir do comportamento esperado, incluindo erro/limite pertinente.
5. Implementar incrementalmente, evitando generalização especulativa.
6. Revisar compatibilidade, segurança, observabilidade e custo operacional quando aplicáveis.
7. Verificar a feature na fronteira real e preservar fluxos existentes relevantes.
8. Definir rollout/rollback quando a mudança exigir ativação controlada.

Não inventar requisitos ausentes que alterem produto ou contrato sem evidência/autorização.
