# Agentes especializados

Papéis canônicos da arquitetura agentic. Não pressupõem subagentes nativos: adapters podem executá-los separadamente ou como etapas sequenciais no mesmo agente.

## Contrato comum

Todo agente deve receber somente contexto necessário, separar fato/hipótese/inferência/desconhecido, não alegar acesso ou execução inexistente, preservar trabalho preexistente, devolver lacunas de evidência e respeitar stop conditions.

## Agentes

1. `investigador.md` — causa e experimentos discriminantes.
2. `diagnosticador-runtime.md` — memória, JVM, container, Lambda, rede e runtime.
3. `estrategista-testes.md` — prova correta para a fronteira afetada.
4. `implementador.md` — menor mudança correta.
5. `revisor-codigo.md` — revisão adversarial e contraexemplos.
6. `revisor-seguranca.md` — revisão condicional de segurança.
7. `verificador-evidencias.md` — validação das alegações finais.
8. `agente-aprendizado.md` — proposta sanitizada de aprendizado/regressão.
9. `analista-desenhos-tecnicos.md` — interpretação e criação visual técnica com limites de precisão.

O orquestrador seleciona somente os papéis pertinentes.
