# Verificar Mudanças — orquestração agentic

Este repositório usa a skill `.agents/skills/verificar-mudancas/SKILL.md` como núcleo metodológico. A arquitetura agentic complementa o núcleo; não o substitui.

## Interface canônica em português

Quando o usuário utilizar um destes comandos — ou expressar intenção equivalente — consultar o arquivo correspondente em `.agents/commands/`:

- `/verificar`
- `/investigar`
- `/corrigir`
- `/revisar`
- `/validar`
- `/portao-qualidade`
- `/aprender`

## Roteamento

Antes de executar uma mudança, classificar tarefa, critérios de aceite e risco conforme a skill principal. Depois selecionar apenas os papéis necessários em `.agents/agents/`.

Fluxo base para correção:

`investigador → estrategista-testes → implementador → revisor-codigo → verificador-evidencias`

Para memória, JVM, container, Lambda, deploy, portas, CPU, startup, rede ou limites de recurso, incluir `diagnosticador-runtime`.

Para autenticação, autorização, IAM, secrets, dados sensíveis, entrada externa ou exposição de rede, incluir `revisor-seguranca` quando pertinente.

Em solicitação somente investigativa, não editar. Em ambiente sem subagentes, executar os mesmos papéis sequencialmente no agente atual, mantendo separação lógica entre investigação, implementação, revisão e verificação.

## Invariantes

- evidência antes de confiança;
- distinguir fato, hipótese, inferência e desconhecido quando material;
- não alegar execução inexistente;
- não carregar todos os especialistas por padrão;
- procurar contraexemplo após implementação;
- validar claims finais contra evidência;
- HIGH/CRITICAL exigem controles adicionais definidos no núcleo;
- dados corporativos, secrets e código proprietário não devem ser promovidos ao repositório público.

A especificação da fase está em `docs/agentic-v1.5.md`.