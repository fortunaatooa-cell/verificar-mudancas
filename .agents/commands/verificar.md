# /verificar

Executar o fluxo completo de engenharia da `verificar-mudancas`.

## Fluxo

1. classificar tarefa e risco;
2. transformar objetivo em critérios observáveis de aceite;
3. selecionar referências/playbook pertinentes;
4. selecionar somente os agentes necessários;
5. investigar antes de editar quando a causa não estiver sustentada;
6. definir a prova correta;
7. implementar a menor mudança correta;
8. revisar criticamente;
9. validar evidências e estado final;
10. registrar lacunas e eventual aprendizado.

## Roteamento padrão

- bug comum: investigador → estrategista de testes → implementador → revisor → verificador;
- runtime/memória/deploy: adicionar diagnosticador de runtime;
- segurança: adicionar revisor de segurança;
- apenas análise: usar `/investigar`.

Não exigir todas as etapas para LOW quando a evidência tornar alguma delas desnecessária; justificar omissões relevantes.