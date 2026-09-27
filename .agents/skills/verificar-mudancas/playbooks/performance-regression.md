# Playbook: regressão de performance

Usar quando uma mudança degradou latência, throughput, consumo ou capacidade.

1. Definir métrica e baseline comparável antes/depois.
2. Localizar o gargalo por evidência: CPU, memória, GC, I/O, banco, rede, lock, fila ou algoritmo.
3. Formular hipótese e medir a fronteira suspeita antes de otimizar.
4. Criar benchmark/teste representativo e reproduzível quando possível.
5. Aplicar a menor mudança que afete o gargalo sustentado.
6. Comparar novamente sob condições equivalentes e verificar correção funcional.
7. Observar comportamento próximo do limite e impacto em custo/recursos.

Não declarar ganho sem medição nem trocar regressão por consumo excessivo em outro recurso sem registrar o trade-off.
