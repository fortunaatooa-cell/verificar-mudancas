# SPEC — Arquitetura agentic v1.5

## Objetivo

Evoluir `verificar-mudancas` de uma skill única para um sistema portátil de engenharia assistida por agentes, mantendo compatibilidade com o uso atual.

O núcleo continua seguindo:

**investigar → classificar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

## Interface em português

Comandos canônicos:

- `/verificar`
- `/investigar`
- `/corrigir`
- `/revisar`
- `/validar`
- `/portao-qualidade`
- `/aprender`

Adapters futuros podem traduzir esses conceitos para mecanismos nativos de cada harness, mas a interface do projeto permanece em português.

## Orquestração

O coordenador deve:

1. classificar tarefa e risco;
2. criar critérios observáveis de aceite;
3. selecionar referências e playbook sob demanda;
4. selecionar somente os agentes pertinentes;
5. coordenar investigação, prova, implementação, revisão e verificação;
6. degradar para etapas sequenciais quando subagentes não existirem.

### Roteamento inicial

Bug comum:

`investigador → estrategista-testes → implementador → revisor-codigo → verificador-evidencias`

Runtime/memória/deploy:

`investigador → diagnosticador-runtime → estrategista-testes → implementador → revisor-codigo → verificador-evidencias`

Segurança:

adicionar `revisor-seguranca` quando a fronteira justificar.

Investigação apenas:

`investigador` + especialistas necessários, sem edição.

## Agentes v1.5

- Investigador: hipóteses, evidência contrária e experimento discriminante.
- Diagnosticador de runtime: JVM, containers, memória, CPU, rede, startup e limites.
- Estrategista de testes: prova adequada à propriedade e fronteira.
- Implementador: menor mudança correta.
- Revisor de código: revisão adversarial e contraexemplo.
- Revisor de segurança: somente quando aplicável.
- Verificador de evidências: valida claims finais.

## Contratos estruturados

`schemas/task.schema.json` define classificação, risco, aceite e agentes selecionados.

`schemas/investigation.schema.json` define saída mínima de investigação.

`schemas/result.schema.json` define conclusão, claims e quality gate.

Schemas são contratos portáteis; não exigem que o modelo exponha JSON ao usuário.

## Requisitos não funcionais

- lazy loading de referências e agentes;
- compatibilidade com skill atual;
- nenhuma dependência obrigatória de um fornecedor;
- nenhum aprendizado automático promovido ao core;
- nenhuma alegação de execução inexistente;
- regras proporcionais ao risco;
- dados corporativos não entram no repositório público.

## Critérios de aceite

A v1.5 foundation está pronta quando:

1. comandos canônicos em português existem;
2. sete agentes possuem contratos separados;
3. schemas de tarefa/investigação/resultado são válidos;
4. evals cobrem bug, runtime/memória, segurança, investigação-only e HIGH risk;
5. validador rejeita ausência desses componentes;
6. testes do validador cobrem as novas invariantes;
7. `main` permanece intacta até revisão/merge.

## Fora do escopo desta fase

- hooks executáveis;
- memória persistente;
- promotion automática de lessons;
- adapters específicos de Codex/Claude/Devin/Copilot;
- instalador multiplataforma.

Esses itens entram somente depois de medir a v1.5 e evitar crescimento especulativo.