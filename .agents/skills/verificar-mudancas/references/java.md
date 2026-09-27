# Java e Spring

Ler quando a falha envolver Java, Spring, API, mensageria ou persistência. Descobrir versões, módulos e comandos reais em `pom.xml`, `build.gradle*`, scripts e CI. Escolher JUnit, Mockito, Testcontainers ou outra ferramenta somente se fizerem parte do projeto.

## Localizar a fronteira

- Seguir requisição/evento → validação → controller/consumer → serviço → persistência/integração → resposta ou evento emitido. Comparar HTTP status, corpo, headers, esquema e semântica de erro com o contrato publicado.
- Examinar serialização/deserialização, `null`, fuso horário, transações, flush/commit, rollback, versionamento de schema, migrações e compatibilidade com consumidores existentes quando implicados.
- Em processamento assíncrono, separar publicação de consumo, retry, DLQ, duplicata, ordering e idempotência. Em falha intermitente, examinar concorrência e estado compartilhado.

## Provar

- Regra isolada: teste de serviço com dependências controladas. Contrato HTTP: teste no limite web. JPA ou migração: teste com a configuração e o banco mais próximos da fronteira real que o ambiente permitir. Mensageria: teste de integração/contrato da mensagem quando a falha depender dela.
- Confirmar que o teste falhou pelo comportamento relatado, não por `ApplicationContext` incompleto, fixture inválida, container indisponível ou versão de biblioteca diferente. Usar um caso vizinho para preservar o fluxo normal.
- Se apenas o mock reproduzir o erro, questionar se ele substituiu precisamente a integração suspeita. Para dependência externa indisponível, registrar qual contrato ficou sem validação e o teste substituto possível.

## Entrega específica

Relatar módulo, versão/runtime, caminho observado, contrato preservado, comando e resultado de cada teste; mencionar quando o banco ou a fila reais não puderam ser exercitados. Não presumir que compilação e testes unitários provam uma mudança de comportamento externo.
