# APIs e contratos

Usar quando a mudança afetar HTTP, RPC, eventos ou schemas consumidos por outros componentes.

## Contrato e compatibilidade
- Identificar consumidores, versão e contrato observado. Comparar método, rota, status, headers, payload, tipos, campos obrigatórios, semântica de erro, paginação e idempotência.
- Tratar remoção ou renomeação de campo, mudança de tipo, enum, default, status ou semântica como potencial breaking change. Compilar não prova compatibilidade entre serviços.
- Em eventos, considerar evolução de schema, consumidores em versões diferentes e mensagens antigas ainda em trânsito.

## Provar
- Derivar critérios de aceite observáveis do contrato e testar fluxo normal, ausência ou erro relevante e compatibilidade próxima quando aplicável.
- Preferir testes de contrato ou integração na fronteira. Mocks não provam sozinhos que provider e consumer continuam compatíveis.
- Em retries, timeouts e operações mutáveis, verificar idempotência e efeitos duplicados.

## Entrega específica
Relatar contrato antes e depois, consumidores potencialmente afetados, evidência de compatibilidade e qualquer parte não exercitada. Não classificar uma mudança como não breaking sem verificar o contrato que realmente mudou.
