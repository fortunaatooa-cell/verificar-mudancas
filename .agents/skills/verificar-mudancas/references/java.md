# Java e Spring

Ler quando a falha envolver Java, Spring, API, mensageria ou persistência. Descobrir versões, módulos e comandos reais em `pom.xml`, `build.gradle*`, scripts e CI. Escolher JUnit, Mockito, Testcontainers ou outra ferramenta somente se fizerem parte do projeto.

## Localizar a fronteira

- Seguir requisição/evento → validação → controller/consumer → serviço → persistência/integração → resposta ou evento emitido. Comparar HTTP status, corpo, headers, esquema e semântica de erro com o contrato publicado.
- Examinar serialização/deserialização, `null`, fuso horário, transações, flush/commit, rollback, versionamento de schema, migrações e compatibilidade com consumidores existentes quando implicados.
- Em processamento assíncrono, separar publicação de consumo, retry, DLQ, duplicata, ordering e idempotência. Em falha intermitente, examinar concorrência e estado compartilhado.

## Semântica Spring que muda o diagnóstico

Confirmar versão e configuração do projeto antes de transformar estes pontos em regra absoluta:

- `MockMvc` exercita o processamento Spring MVC com requests/responses simulados. É uma boa fronteira para status, body, headers, validação, controller e exception handling, mas não prova transporte de rede, TLS, proxy reverso ou servidor real.
- O contrato no fio depende de Jackson e da configuração efetiva: nome do campo Java não garante o mesmo nome no JSON quando há `@JsonProperty`, naming strategy, mixins, módulos ou DTOs distintos. Para contrato externo, verificar o payload serializado/deserializado na fronteira web, inclusive validação e erros.
- `flush()`/`saveAndFlush()` envia mudanças pendentes ao banco, mas **não é evidência de commit**. Quando a hipótese envolve persistência final, verificar o estado depois que a transação termina, preferencialmente de fora da transação que executou a escrita.
- Em transações declarativas Spring no modo proxy padrão, a chamada precisa cruzar o proxy para que o interceptor transacional seja aplicado. Self-invocation (`this.metodoAnotado()`) pode contornar o proxy; comparar chamada externa e interna quando isso explicar ausência de transação.
- Por padrão, `RuntimeException` e `Error` causam rollback; checked exceptions não causam rollback automaticamente. Regras de `rollbackFor`/`noRollbackFor`, configuração global, transaction manager e versão podem alterar o comportamento, então não inferir rollback apenas pelo tipo do método ou pela presença de `@Transactional`.
- Propagações como `REQUIRES_NEW` mudam a fronteira de commit: uma transação interna pode confirmar mesmo quando a transação externa faz rollback. Provar com beans Spring reais e estado observado após o término das duas transações.
- SQL emitido no log, `save()` retornando entidade ou `flush()` concluindo sem erro não provam sozinho que a transação foi commitada. Observar a fronteira posterior adequada.

## JPA, consultas e concorrência

- Para suspeita de N+1, não concluir apenas pela presença de relacionamento `LAZY`/`EAGER`. Medir queries/statements em um fluxo representativo e comparar uma alternativa sustentada (`join fetch`, entity graph, projeção, batch fetch etc.) sem alterar semântica do resultado.
- Ao usar optimistic locking, confirmar presença/uso de `@Version`, fronteira transacional e comportamento de conflito com duas versões concorrentes reais do mesmo registro. Não transformar conflito legítimo em retry infinito ou last-write-wins sem requisito.
- Em concorrência Java, um teste que passa uma vez não prova ausência de race. Quando possível, controlar interleaving com barreiras/latches ou usar stress tests adequados; verificar estado final e invariantes, não apenas ausência de exceção.

## Provar

- Regra isolada: teste de serviço com dependências controladas. Contrato HTTP: teste no limite web. JPA ou migração: teste com a configuração e o banco mais próximos da fronteira real que o ambiente permitir. Mensageria: teste de integração/contrato da mensagem quando a falha depender dela.
- Confirmar que o teste falhou pelo comportamento relatado, não por `ApplicationContext` incompleto, fixture inválida, container indisponível ou versão de biblioteca diferente. Usar um caso vizinho para preservar o fluxo normal.
- Se apenas o mock reproduzir o erro, questionar se ele substituiu precisamente a integração suspeita. Para dependência externa indisponível, registrar qual contrato ficou sem validação e o teste substituto possível.
- Para transações, distinguir observação feita **durante** a transação de estado observado após commit/rollback. Quando a causa depender de proxy, propagação ou rollback rules, testar pelo bean Spring real em vez de instanciar a classe diretamente.
- Para performance de persistência, medir o comportamento que importa (queries, tempo, linhas, locks) em dataset representativo; um teste funcional que retorna os valores certos não prova que N+1 ou contenção desapareceram.

## Entrega específica

Relatar módulo, versão/runtime, caminho observado, contrato preservado, comando e resultado de cada teste; mencionar quando o banco ou a fila reais não puderam ser exercitados. Não presumir que compilação e testes unitários provam uma mudança de comportamento externo.
