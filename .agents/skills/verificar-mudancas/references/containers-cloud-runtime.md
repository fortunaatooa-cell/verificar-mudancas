# Containers e runtime de cloud

Usar quando a mudança envolver Docker, Kubernetes, ECS, Lambda, PaaS, containers, runtime, configuração de ambiente, portas/rede ou comportamento após deploy. Quando o sintoma aparece depois de build/deploy, combinar quando pertinente com [CI/CD e release](ci-cd-release.md) e [observabilidade e SRE](observability-sre.md).

## Regra central: processo iniciado != serviço alcançável

Um log como `server started`, `Tomcat started` ou equivalente comprova apenas parte do lifecycle da aplicação. Ele **não** prova, sozinho, que existe um socket escutando na interface/porta esperada, que outro namespace consegue alcançá-lo, que o proxy/plataforma aponta para ele ou que o health check está correto.

Quando sinais contradisserem — por exemplo, a aplicação diz que iniciou, mas container/proxy/plataforma diz que não há porta ou endpoint alcançável — localizar a primeira divergência nesta cadeia antes de editar:

`processo -> configuração efetiva -> socket/listener -> bind/interface -> namespace do container/host -> service/proxy/load balancer -> health check -> requisição externa`

Não saltar diretamente para controller, Actuator, rota de health, firewall ou configuração de plataforma sem evidência de que a etapa anterior funciona.

## Contexto de execução

- Identificar imagem/artifact, commit/digest/revisão quando disponível, arquitetura, runtime, entrypoint/start command, variáveis, secrets, portas, rede, health checks, limites de CPU/memória e identidade/permissões efetivas.
- Separar configuração no repositório do estado em runtime: Dockerfile, Terraform, manifesto ou `application.yml` correto não prova que esse artifact/config está efetivamente implantado.
- Em containers, verificar base image, usuário, filesystem, entrypoint, layers e compatibilidade de arquitetura quando pertinentes.
- Confirmar precedência de configuração quando há múltiplas fontes: argumento de linha de comando, variável de ambiente, arquivo, profile, secret/config map ou default.

## Porta, bind e alcançabilidade

- Descobrir a porta **efetiva** usada pelo processo e compará-la com a porta esperada pela plataforma. Não assumir que o valor no arquivo fonte é o valor em runtime.
- Descobrir em qual endereço/interface o processo realmente escuta. Bind em loopback (`127.0.0.1`/`localhost`) pode funcionar dentro do mesmo namespace e continuar inalcançável de fora; bind em todas as interfaces (`0.0.0.0`) tem semântica diferente.
- `EXPOSE` no Dockerfile é metadado/documentação da imagem; não cria um listener e não corrige um processo bound na interface/porta errada.
- Health endpoint só é útil depois que a camada anterior consegue alcançar o listener. Adicionar Actuator ou outra rota não corrige, por si só, ausência de socket alcançável.
- Verificar se o processo permanece vivo após anunciar startup; uma porta que abre e fecha por crash/restart exige diagnóstico de lifecycle, não apenas de configuração de rede.
- Quando permitido, observar sockets (`ss`, `netstat` ou equivalente) e testar progressivamente a mesma propriedade: dentro do processo/container, do próximo namespace/host, através do service/proxy e finalmente externamente. Registrar onde começa a falhar.
- Em plataformas com porta dinâmica/fornecida por ambiente, confirmar o contrato real da plataforma e a variável efetivamente injetada; não hardcodar porta como primeira correção sem necessidade sustentada.

## Provar

- Exercitar startup e a menor prova de alcançabilidade no target mais próximo disponível. Compilar imagem não prova que o serviço inicia; log de startup não prova socket; socket local não prova tráfego pelo proxy.
- Reproduzir, quando viável, o start command e as variáveis relevantes do ambiente. Se o problema é pós-deploy, rastrear o commit até o artifact/digest executado antes de concluir que a configuração fonte está em uso.
- Em Kubernetes/ECS, observar rollout, readiness/liveness, service/target, eventos/logs, recursos e conectividade. Não aumentar limites como correção automática sem evidência de exaustão.
- Em Lambda/serverless, conferir runtime, arquitetura, pacote/layers, timeout, memória, concorrência e permissões realmente implantadas.
- Depois da correção, repetir a prova na **mesma fronteira que falhava** e um fluxo normal vizinho. Não declarar resolvido apenas porque o log mudou.

## Evitar correção por tentativa

Não aplicar várias mudanças plausíveis ao mesmo tempo (`EXPOSE`, porta hardcoded, health endpoint, proxy, controller, timeout) sem um experimento discriminante. Cada mudança deve responder a uma hipótese sustentada e preservar a capacidade de identificar qual fronteira estava quebrada.

## Entrega específica

Relatar artifact/imagem, target, start command/configuração relevante, porta e bind efetivos quando pertinentes, primeira fronteira que divergiu, sinais de runtime, experimento executado e qualquer diferença entre configuração declarada e estado observado. Separar causa confirmada de hipótese ainda não medida.
