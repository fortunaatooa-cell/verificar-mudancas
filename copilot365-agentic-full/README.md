# Copilot 365 — Agentic Full v3.1

Distribuição para Microsoft 365 Copilot Agent Builder baseada na arquitetura completa da branch `feature/agentic-v1-5`.

## Objetivo

Preservar a arquitetura conceitual do sistema agentic no formato suportado por uma Custom Skill do Copilot 365:

- papéis especializados (investigador, planejador, arquiteto, diagnosticador de runtime, estrategista de testes, implementador, revisores, verificador de evidências, analista de desenhos e aprendizado);
- comandos/intents;
- rules;
- gates pre-edit, post-edit e pre-finish;
- planejamento;
- arquitetura e ADR;
- TDD RED → GREEN → REFACTOR → REGRESSION;
- review adversarial e segurança;
- runtime/performance/SRE;
- APIs, dados, distribuídos, cloud, Terraform e CI/CD;
- desenhos técnicos;
- aprendizado governado;
- quality gate.

## Adaptação para Copilot 365

Os papéis são executados sequencialmente pelo mesmo agente; não são anunciados como subagentes reais. Comandos são intenções conversacionais. Hooks viram gates conceituais. Nenhuma execução, shell, Git, escrita ou renderização é alegada se a plataforma não expuser essa capacidade.

## Pacote validado

O ZIP pronto para `Carregar habilidade` possui:

- `SKILL.md` com 15.455 caracteres de instruções;
- 61 arquivos;
- 11 papéis especializados;
- 12 comandos/intents;
- 9 rules;
- 15 referências;
- 7 playbooks;
- schemas de Plan e ADR;
- 3 lifecycle gates.

O pacote está abaixo dos limites atuais do Agent Builder (20.000 caracteres de instruções por skill, até 350 arquivos por pacote e ZIP de até 50 MB).

Fonte-base: `feature/agentic-v1-5` @ `6a2c3d8a682a4debb27cba80a346dc9d2fa80268`.
