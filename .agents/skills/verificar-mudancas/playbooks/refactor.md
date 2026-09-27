# Playbook: refatoração

Usar quando o objetivo principal é melhorar estrutura sem mudar comportamento externo.

1. Definir comportamento que precisa permanecer equivalente.
2. Identificar smells e limites reais do escopo.
3. Proteger contratos/fluxos relevantes com testes antes da mudança.
4. Fazer passos pequenos e verificáveis, preservando compatibilidade.
5. Evitar misturar refatoração com feature ou correção não relacionada.
6. Comparar comportamento antes/depois e revisar dependências, complexidade e legibilidade.
7. Verificar novamente após a última alteração.

Uma refatoração não está provada só porque compila; o comportamento observável relevante deve permanecer preservado.
