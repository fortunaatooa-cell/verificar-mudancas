# Sistemas distribuídos e mensageria

Usar quando a mudança envolver chamadas entre serviços, filas, streams, eventos, concorrência ou consistência distribuída.

## Investigar
- Seguir a operação ponta a ponta e identificar fronteiras de rede, ownership do estado e ponto em que a observação diverge.
- Considerar timeout, retry, retry storm, duplicata, ordering, at-least-once, eventual consistency, falha parcial, race condition, clock/time assumptions, backpressure e limites de concorrência quando pertinentes.
- Não assumir exactly-once porque a ferramenta ou broker usa essa expressão; verificar o efeito observável no domínio e no destino.

## Provar
- Para operações repetíveis, testar idempotência com a mesma chave/evento. Para ordering, construir cenário fora de ordem. Para concorrência, testar interleavings relevantes em vez de apenas execução sequencial.
- Em retries, verificar número máximo, backoff, jitter, timeout total e comportamento quando a dependência permanece indisponível.
- Em publicação e persistência relacionadas, investigar janelas de falha entre as duas operações e padrões já adotados pelo projeto, como outbox, quando aplicável.

## Entrega específica
Relatar semântica de entrega observada, ownership do estado, comportamento em falha parcial e quais propriedades foram realmente testadas. Não declarar consistência ou idempotência apenas por inspeção superficial do código.
