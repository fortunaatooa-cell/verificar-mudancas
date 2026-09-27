# Performance e capacidade

Usar quando a tarefa mencionar lentidão, consumo, throughput, memória, CPU, I/O, escalabilidade ou quando o diff introduzir risco plausível de regressão relevante.

## Medir antes de concluir
- Definir baseline e métrica compatível com o problema: latência, throughput, CPU, memória, alocações/GC, I/O, queries, chamadas de rede ou custo por operação.
- Reproduzir com carga e dataset representativos quando possível. Microbenchmark não substitui teste de integração quando o gargalo está em banco, rede ou runtime.
- Procurar N+1, loops de I/O, materialização desnecessária, estruturas inadequadas, contenção, serialização excessiva, queries sem índice e fan-out quando sustentados pela evidência.

## Provar
- Comparar antes/depois sob condições equivalentes e registrar variabilidade. Não dizer "ficou mais rápido" ou "mais eficiente" sem medição.
- Confirmar que otimização preserva correção e não apenas troca latência por uso excessivo de memória, custo ou complexidade operacional.
- Para capacidade, observar comportamento próximo do limite e degradação, não apenas média em carga baixa.

## Entrega específica
Relatar métrica, cenário, baseline, resultado, variância relevante e limites do teste. Separar hipótese de otimização de ganho medido.
