# Observabilidade e SRE

Usar quando o diagnóstico depender de comportamento em runtime, incidentes, regressões intermitentes, latência, disponibilidade ou operação em produção.

## Investigar
- Procurar correlação entre logs, métricas e traces usando timestamps, IDs de correlação e versão/deploy quando disponíveis.
- Separar sintoma de causa: erro rate, latência e saturação mostram impacto; a hipótese de causa precisa de evidência no componente ou dependência relevante.
- Verificar health checks, filas, pools, limites, recursos e dependências externas quando fizerem parte da cadeia afetada.

## Provar e operar
- Antes da mudança, registrar baseline observável quando possível. Depois, comparar os mesmos sinais; não concluir melhora apenas porque o erro deixou de aparecer em uma execução.
- Para mudanças de risco, definir sinal de sucesso, sinal de rollback e janela de observação. Quando aplicável, considerar rollout progressivo, canary ou feature flag conforme os mecanismos reais do projeto.
- Alertas devem representar condição acionável; evitar sugerir alerta apenas para mascarar falta de diagnóstico.

## Entrega específica
Relatar quais sinais sustentam a conclusão, período/ambiente observado e o que ainda não foi medido. Indicar como a equipe detectará recorrência quando isso fizer parte do problema.
