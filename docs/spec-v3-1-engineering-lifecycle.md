# SPEC v3.1 — Engineering Lifecycle

## Visão

Expandir a `verificar-mudancas` para cobrir, além de investigação e correção, as etapas anteriores e transversais do ciclo de engenharia: planejamento, arquitetura, TDD e registro de decisões arquiteturais.

A expansão deve preservar o diferencial evidence-first, carregamento sob demanda, portabilidade entre harnesses e degradação segura.

## Objetivos

1. decompor mudanças grandes antes de editar;
2. analisar arquitetura atual e alternativas com trade-offs explícitos;
3. integrar arquitetura com desenhos técnicos e implementação real;
4. oferecer TDD verdadeiro como modo do estrategista de testes;
5. registrar decisões relevantes em ADRs rastreáveis;
6. evitar transformar toda tarefa em processo pesado.

## Não objetivos

- não criar dezenas de agentes por especialidade;
- não exigir TDD para toda mudança;
- não transformar proposta arquitetural em fato sem evidência;
- não gerar ADR para decisão trivial/local;
- não substituir revisão humana em decisões HIGH/CRITICAL.

## Novos especialistas

### Planejador

Responsável por transformar objetivo em plano executável, identificando:

- resultado esperado;
- restrições e desconhecidos;
- dependências e ordem;
- componentes prováveis;
- critérios de aceite;
- estratégia de prova;
- riscos e stop conditions;
- etapas que podem ser paralelas e etapas obrigatoriamente sequenciais.

O planejador não deve inventar arquitetura ou requisito ausente.

### Arquiteto

Responsável por:

- reconstruir arquitetura atual a partir de evidências;
- separar arquitetura observada, inferida e proposta;
- mapear contratos, dependências, dados, trust boundaries e operação;
- comparar alternativas por trade-offs;
- considerar compatibilidade, migração, rollback/rollforward, observabilidade, custo e segurança quando pertinentes;
- produzir ou atualizar desenho técnico quando houver capacidade;
- propor ADR para decisões materialmente relevantes.

## TDD como modo

TDD é um modo do `estrategista-testes`, não um agente separado.

Ciclo obrigatório quando TDD for selecionado:

`RED → GREEN → REFACTOR → REGRESSION`

### RED

Criar primeiro prova que falha pelo comportamento ausente/defeituoso esperado. Falha de setup, sintaxe ou infraestrutura não conta como RED válido.

### GREEN

Implementar a menor mudança que faz a prova pertinente passar.

### REFACTOR

Melhorar estrutura sem alterar o comportamento protegido. Reexecutar provas após a refatoração.

### REGRESSION

Executar fronteira afetada e cenários adjacentes pertinentes depois da última alteração.

TDD não deve ser alegado quando o teste foi escrito apenas depois da implementação.

## ADR

Decisões arquiteturais relevantes podem produzir um ADR contendo:

- título e status;
- contexto e forças;
- decisão;
- alternativas consideradas;
- trade-offs/consequências;
- compatibilidade/migração;
- evidências e desconhecidos;
- sinais de sucesso e reversão quando aplicável.

ADR registra decisão; não substitui código, teste ou validação operacional.

## Comandos canônicos

- `/planejar [simples|aprofundado|ambos]`
- `/arquitetura [analisar|propor|revisar] [simples|aprofundado|ambos]`
- `/tdd [planejar|executar|revisar]`
- `/adr [criar|revisar]`

Os comandos representam intenção. Adapters podem traduzi-los para mecanismos locais.

## Roteamento

Mudança ampla/ambígua → `planejador` antes do implementador.

Mudança estrutural, integração, novo serviço, fronteira de dados, desenho técnico de arquitetura ou decisão difícil de reverter → `arquiteto`.

Bug/feature com comportamento testável e feedback rápido → `estrategista-testes` em modo TDD quando apropriado.

Decisão arquitetural material → `arquiteto` + ADR.

## Critérios de aceite v3.1

1. `planejador` e `arquiteto` existem como papéis canônicos;
2. skills auxiliares `planejamento` e `arquitetura` podem ser instaladas;
3. comandos em português existem;
4. estrategista de testes define TDD real e rejeita falso RED;
5. schema de plano e ADR existem;
6. arquitetura pode chamar análise de desenho técnico sem assumir visão/render;
7. evals cobrem planejamento, trade-offs, TDD e ADR;
8. validador agentic protege esses componentes;
9. instalador full inclui as novas skills;
10. ausência de subagentes continua degradando para execução sequencial.

## Próxima fase candidata — v3.2

Somente após avaliação da v3.1: performance, observabilidade/SRE e dados/banco como especialistas adicionais se casos reais demonstrarem ganho.