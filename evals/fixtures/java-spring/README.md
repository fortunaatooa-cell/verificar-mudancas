# Fixture executável — Java/Spring

Exercita pontos centrais de `references/java.md` usando Spring Boot **3.5.16**, Java 17 e H2.

## Executar

```bash
bash evals/fixtures/java-spring/run.sh
```

O runner exige Maven e acesso ao Maven Central.

## Cenários

### `java-404`

O serviço contém intencionalmente um fallback que cria um pedido sintético quando o repositório não encontra o ID. `OrderDesiredContractTest` exige `404` via `MockMvc`.

O runner primeiro executa o teste com o bug habilitado e **exige que ele falhe**; depois desabilita o fallback via propriedade e exige que o mesmo teste passe. Isso prova a diferença na fronteira Spring MVC, não apenas em um mock do serviço.

### HTTP/Jackson/validation

A fixture verifica que `@JsonProperty("customerName")` define o nome realmente serializado, mesmo com o componente Java chamado `name`, e que Bean Validation é observada pela fronteira MVC. `MockMvc` cobre o processamento Spring MVC; não prova transporte de rede, TLS ou proxy reverso.

### transações JPA

`SpringTransactionSemanticsTest` verifica com banco H2 real que:

- `saveAndFlush` seguido de `RuntimeException` dentro de `@Transactional` pode executar o flush e ainda assim terminar em rollback;
- uma checked exception não força rollback por padrão, se nenhuma regra adicional estiver configurada;
- no modo proxy padrão, chamada interna `this.innerTransactional()` não cruza o proxy transacional, enquanto chamada externa ao método anotado cruza;
- `REQUIRES_NEW` em outro bean pode confirmar sua transação mesmo quando a transação externa depois faz rollback.

### JPA queries e locking

A fixture habilita Hibernate Statistics e compara um fluxo LAZY que produz N+1 com um `join fetch` equivalente, medindo prepared statements. Também abre dois `EntityManager` sobre a mesma entidade com `@Version` e confirma que o segundo commit concorrente/stale é rejeitado.

### concorrência Java

O teste usa `CyclicBarrier` para forçar um interleaving que demonstra lost update, evitando depender de uma race probabilística. Em seguida verifica o mesmo invariante com `AtomicInteger`.

## Limites

A fixture não prova comportamento em todos os bancos, drivers, versões Spring ou configurações de transaction manager. H2 não substitui PostgreSQL/MySQL/Oracle quando o defeito depender de lock, SQL, isolation ou constraints específicos. Também não cobre Kafka/RabbitMQ nem servidor HTTP real. Seu objetivo é validar se a referência descreve corretamente fronteiras Spring/Java comuns e exige a prova adequada.
