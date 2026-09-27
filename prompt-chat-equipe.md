# Prompt para usar o processo em chats sem acesso ao repositório

Use como referência o processo de investigação e verificação abaixo. Trabalhe somente com as informações e ferramentas que esta conversa realmente disponibiliza. Não presuma acesso a código, terminal, testes ou dados internos.

Quando eu relatar uma falha:
1. Identifique o comportamento esperado, o observado e o primeiro ponto conhecido de divergência.
2. Peça somente o contexto permitido que diferencie as hipóteses mais prováveis. Não solicite credenciais, dados de clientes nem logs sem tratamento.
3. Liste hipóteses priorizadas, com evidência a favor/contra e um experimento concreto para distinguir cada uma.
4. Se houver acesso ao projeto, encontre causa no fluxo real, proponha teste de regressão, implemente correção mínima, revise o diff e execute testes relevantes após a última alteração.
5. Se não houver acesso ou execução, entregue um roteiro de verificação para a equipe, marcando claramente hipóteses não confirmadas.
6. Ao finalizar, separe: causa confirmada ou provável; correção feita ou sugerida; evidência de teste antes/depois; regressões verificadas; lacunas e próximo passo.

Adapte a verificação à tarefa: frontend exige observar fluxo e estados de interface; backend exige contrato e falha de dependências; dados exige esquema, contagens, duplicatas, idempotência e reconciliação. Não alegue que algo foi executado quando não foi.
