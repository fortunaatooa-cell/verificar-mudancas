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

`MockMvc` cobre o processamento Spring MVC com request/response simulados; não é prova de transporte de rede ou servidor real.

### transações JPA

`SpringTransactionSemanticsTest` verifica com banco H2 real que:

- `saveAndFlush` seguido de `RuntimeException` dentro de `@Transactional` pode executar o flush e ainda assim terminar em rollback;
- uma checked exception não força rollback por padrão, se nenhuma regra adicional estiver configurada;
- no modo proxy padrão, chamada interna `this.innerTransactional()` não cruza o proxy transacional, enquanto chamada externa ao método anotado cruza.

## Limites

A fixture não prova comportamento em todos os bancos, drivers, versões Spring ou configurações de transaction manager. Ela também não substitui Testcontainers quando o defeito depender de semântica específica de PostgreSQL/MySQL/Oracle. Seu objetivo é validar se a referência da skill descreve corretamente fronteiras Spring comuns e se exige a prova adequada.
