# Performance e SRE
Defina baseline e métrica: p50/p95/p99, throughput, CPU, memória, GC, I/O, cold start.
Compare cargas/ambientes equivalentes.
Use logs, métricas, traces, health checks e eventos para achar o primeiro sinal compatível com a degradação.
Quando pertinente: timeout, retry limitado com backoff/jitter, circuit breaker, backpressure, DLQ, idempotência, capacidade e rollback signal.
Deploy sem erro não prova saúde.
