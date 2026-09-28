# Java e Spring

Ler quando a falha envolver Java, Spring, API, mensageria ou persistência. Descobrir versões, módulos e comandos reais em `pom.xml`, `build.gradle*`, scripts e CI. Escolher JUnit, Mockito, Testcontainers ou outra ferramenta somente se fizerem parte do projeto.

## Localizar a fronteira

- Seguir requisição/evento → validação → controller/consumer → serviço → persistência/integração → resposta ou evento emitido. Comparar HTTP status, corpo, headers, esquema e semântica de erro com o contrato publicado.
- Examinar serialização/deserialização, `null`, fuso horário, transações, flush/commit, rollback, versionamento de schema, migrações e compatibilidade com consumidores existentes quando implicados.
- Em processamento assíncrono, separar publicação de consumo, retry, DLQ, duplicata, ordering e idempotência. Em falha intermitente, examinar concorrência e estado compartilhado.

## Semântica Spring que muda o diagnóstico

Confirmar versão e configuração do projeto antes de transformar estes pontos em regra absoluta:

- `MockMvc` exercita o processamento Spring MVC com requests/responses simulados. É uma boa fronteira para status, body, headers, validação, controller e exception handling, mas não prova transporte de rede, TLS, proxy reverso ou servidor real.
- `flush()`/`saveAndFlush()` envia mudanças pendentes ao banco, mas **não é evidência de commit**. Quando a hipótese envolve persistência final, verificar o estado depois que a transação termina, preferencialmente de fora da transação que executou a escrita.
- Em transações declarativas Spring no modo proxy padrão, a chamada precisa cruzar o proxy para que o interceptor transacional seja aplicado. Self-invocation (`this.metodoAnotado()`) pode contornar o proxy; comparar chamada externa e interna quando isso explicar ausência de transação.
- Por padrão, `RuntimeException` e `Error` causam rollback; checked exceptions não causam rollback automaticamente. Regras de `rollbackFor`/`noRollbackFor`, configuração global, transaction manager e versão podem alterar o comportamento, então não inferir rollback apenas pelo tipo do método ou pela presença de `@Transactional`.
- SQL emitido no log, `save()` retornando entidade ou `flush()` concluindo sem erro não provam sozinho que a transação foi commitada. Observar a fronteira posterior adequada.

## Provar

- Regra isolada: teste de serviço com dependências controladas. Contrato HTTP: teste no limite web. JPA ou migração: teste com a configuração e o banco mais próximos da fronteira real que o ambiente permitir. Mensageria: teste de integração/contrato da mensagem quando a falha depender dela.
- Confirmar que o teste falhou pelo comportamento relatado, não por `ApplicationContext` incompleto, fixture inválida, container indisponível ou versão de biblioteca diferente. Usar um caso vizinho para preservar o fluxo normal.
- Se apenas o mock reproduzir o erro, questionar se ele substituiu precisamente a integração suspeita. Para dependência externa indisponível, registrar qual contrato ficou sem validação e o teste substituto possível.
- Para transações, distinguir observação feita **durante** a transação de estado observado após commit/rollback. Quando a causa depender de proxy, propagação ou rollback rules, testar pelo bean Spring real em vez de instanciar a classe diretamente.

## Entrega específica

Relatar módulo, versão/runtime, caminho observado, contrato preservado, comando e resultado de cada teste; mencionar quando o banco ou a fila reais não puderam ser exercitados. Não presumir que compilação e testes unitários provam uma mudança de comportamento externo.
