# Containers e runtime de cloud

Usar quando a mudança envolver Docker, Kubernetes, ECS, Lambda, containers, runtime, configuração de ambiente ou comportamento após deploy.

## Contexto de execução
- Identificar imagem/artifact, arquitetura, runtime, variáveis, secrets, portas, rede, health checks, limites de CPU/memória e identidade/permissões efetivas.
- Separar infraestrutura declarada do estado em runtime: Terraform/Kubernetes YAML pode estar correto e ainda haver imagem errada, configuração divergente, crash loop, permissão ausente ou dependência indisponível.
- Em containers, verificar base image, usuário, filesystem, entrypoint, layers e compatibilidade de arquitetura quando pertinentes.

## Provar
- Exercitar startup e health/smoke check no target mais próximo disponível. Compilar imagem não prova que serviço inicia nem que recebe tráfego corretamente.
- Em Kubernetes/ECS, observar rollout, readiness/liveness, eventos/logs, recursos e conectividade. Não aumentar limites como correção automática sem evidência de exaustão.
- Em Lambda/serverless, conferir runtime, arquitetura, pacote/layers, timeout, memória, concorrência e permissões realmente implantadas.

## Entrega específica
Relatar artifact/imagem, target, configuração relevante, sinais de runtime e qualquer diferença entre configuração declarada e estado observado.
