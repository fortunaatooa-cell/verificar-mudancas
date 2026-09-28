# Evals agentic v1.5

Este pacote valida o roteamento e os invariantes mínimos da arquitetura agentic sem depender de suporte nativo a subagentes.

Casos iniciais:

- bug Java com correção;
- diagnóstico de memória/runtime;
- mudança com preocupação de segurança;
- investigação sem edição;
- mudança de alto risco em dados persistentes.

Os casos verificam comportamento esperado e anti-patterns. Eles não provam eficácia do sistema; o A/B controlado continua sendo a evidência apropriada para comparar desempenho com e sem a arquitetura.

Ao encontrar uma regressão real, adicionar um caso mínimo que reproduza o comportamento indesejado antes de promover nova regra ao núcleo.