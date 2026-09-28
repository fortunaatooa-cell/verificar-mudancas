# /portao-qualidade

Executar um quality gate proporcional ao risco e ao tipo de mudança.

## Dimensões

1. critérios de aceite;
2. testes pertinentes;
3. build;
4. lint/análise estática;
5. revisão do diff;
6. contratos/compatibilidade;
7. segurança, se aplicável;
8. runtime/performance/dados, se aplicável;
9. evidências finais.

Estados por dimensão:

`PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `N/A`.

Não executar verificações irrelevantes apenas para preencher checklist. O resultado deve informar o que foi realmente executado e o que permaneceu sem prova.