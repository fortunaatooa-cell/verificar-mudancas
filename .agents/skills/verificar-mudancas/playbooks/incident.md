# Playbook: incidente

Usar quando existe impacto operacional ativo ou comportamento degradado em ambiente real.

1. Confirmar impacto, escopo, início aproximado e sinais observáveis.
2. Priorizar contenção segura e preservação de evidência antes de buscar causa perfeita.
3. Correlacionar versão/deploy, logs, métricas, traces e dependências.
4. Manter hipóteses concorrentes até que evidência discrimine a causa.
5. Aplicar mitigação mínima e reversível quando autorizada; definir sinal de rollback.
6. Depois de estabilizar, investigar causa raiz e criar correção permanente com teste preventivo.
7. Registrar timeline, causa confirmada, sinais úteis e melhoria de detecção/prevenção.

Não transformar correlação temporal com um deploy em causa confirmada sem evidência adicional.
