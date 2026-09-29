# Verificar Mudanças — Knowledge condensado para Devin

Princípios:
- evidence-first;
- causa antes de correção;
- menor mudança correta;
- prova na fronteira real;
- risco proporcional;
- observado ≠ inferido ≠ proposto;
- sem execução inventada.

Roteamento:
bug/incidente → investigar;
feature/migração ampla → planejar;
decisão estrutural → arquitetura;
comportamento testável → testes/TDD;
auth/IAM/secrets/input/rede → segurança;
memória/CPU/container/Lambda → runtime;
imagem/diagrama/planta → desenho técnico;
conclusão → verificar evidências.

Invariantes:
`tamanho de JAR/lib != consumo de RAM`;
CI verde != produção saudável;
deploy sem erro != serviço saudável;
ADR != arquitetura implantada;
desenho != runtime;
teste depois da implementação != RED de TDD.

HIGH/CRITICAL: blast radius, compatibilidade, recuperação, stop conditions, sinais de sucesso.

Após edição final: testes pertinentes + build/lint conforme projeto + diff/status + evidência final.
