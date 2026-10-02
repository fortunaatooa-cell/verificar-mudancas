# Verificar mudanças

> **Status desta branch:** `feature/agentic-v1-5` é **experimental, not evaluated**. A infraestrutura da Spec 10/10 está sendo implementada aqui, mas as capacidades agentic não devem ser promovidas à `main` antes de T8/T14.

Skill e sistema portátil de engenharia inspirado no ciclo do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Ajuda agentes a investigar falhas, implementar mudanças, analisar/criar desenhos técnicos e apresentar evidências verificáveis sem depender de uma linguagem, ferramenta ou ecossistema específico.

**investigar → classificar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

O sistema ajusta profundidade ao risco e agora também separa explicitamente a capacidade de **ver material visual** da capacidade de **gerar/renderizar material visual**. Nenhum adapter pode fingir visão ou geração inexistentes.

## Arquitetura

O núcleo é `.agents/skills/verificar-mudancas/` e continua utilizável sozinho. A instalação completa adiciona:

1. **Referências e playbooks sob demanda** — stack, runtime, dados, segurança, IaC, contratos, desenhos técnicos e tipos de tarefa.
2. **Skills auxiliares** — `investigar`, `estrategia-testes`, `revisar-mudanca`, `diagnosticar-runtime` e `desenho-tecnico`.
3. **Orquestração** — [AGENTS.md](AGENTS.md) e treze papéis especializados, incluindo investigação e validação de regressão em jogos.
4. **Comandos em português** — `/verificar`, `/investigar`, `/corrigir`, `/revisar`, `/validar`, `/portao-qualidade`, `/aprender`, `/desenho-tecnico` e `/depurar-jogo`.
5. **Regras e hooks** — evidência, testes, mudança segura, HIGH/CRITICAL, ambiente regulado, evidência visual, `pre-edit`, `post-edit` e `pre-finish`.
6. **Quality gate** — plano conservador e execução explícita de checks.
7. **Memória controlada** — lessons, patterns, incidents e project knowledge sanitizados; memória é pista, não verdade.
8. **Continuous learning seguro** — aprendizado explícito e geração revisável de eval de regressão, sem promoção automática.
9. **Adapters** — generic, Codex, Claude, Devin e Copilot com capability detection/fallback, incluindo `vision_input` e `visual_generation`; Claude Code possui mapeamento nativo para `CLAUDE.md`, Skills, subagents, rules e hooks.
10. **Instalador** — modo `skill` ou `full`, dry-run e preservação de arquivos existentes.

A especificação implementada está em [docs/agentic-system.md](docs/agentic-system.md), a instalação em [docs/installation.md](docs/installation.md) e os gates de maturidade em [docs/maturity.md](docs/maturity.md).

## Desenhos técnicos e respostas

`references/technical-drawings.md` define leitura por camadas/regiões, inventário de elementos, separação entre **observado / inferido / não determinável**, revisão entre vistas e criação em Mermaid, PlantUML, DOT, SVG ou formatos CAD quando a ferramenta permitir. Medidas, escala, tolerâncias e normas ausentes não são inventadas; render gerativo sem garantia geométrica é tratado como ilustrativo.

`references/response-modes.md` define três saídas: **`simples`**, **`aprofundado`** e **`ambos`**. O modo simples reduz detalhe, não rigor nem alertas materiais.

## Conteúdo

- [SKILL.md](.agents/skills/verificar-mudancas/SKILL.md) — núcleo universal.
- [Desenhos técnicos](.agents/skills/verificar-mudancas/references/technical-drawings.md) e [modos de resposta](.agents/skills/verificar-mudancas/references/response-modes.md).
- [Agentes](.agents/agents/README.md), [comandos](.agents/commands/README.md), [regras](.agents/rules/README.md) e [hooks](.agents/hooks/README.md).
- [Memória](memory/README.md), [adapters](adapters/README.md), schemas em `schemas/` e [regressões geradas](evals/regression/README.md).
- [Integração Claude Code](docs/claude-integration.md) — `CLAUDE.md`, Skills, subagents, rules, hooks e instalação nativa.
- [Avaliações](evals/README.md), [evals agentic](evals/agentic/README.md), [evals visuais](evals/visual/README.md) e [A/B controlado](evals/ab/README.md).
- [Prompt para chat](prompt-chat-equipe.md) para superfícies sem acesso ao repositório.

## Instalação

Somente a skill:

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter generic --mode skill --dry-run
```

Sistema completo:

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter codex --mode full --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter codex --mode full
```

Em uso corporativo, fixe uma **tag ou commit aprovado**; não dependa de uma branch móvel.

### Claude Code

```bash
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full --dry-run
python3 scripts/install.py --target /caminho/do/projeto --adapter claude --mode full
```

O adapter gera wrappers nativos sem duplicar a fonte de verdade: os arquivos em `.agents/` continuam canônicos, enquanto `CLAUDE.md`, `.claude/skills/`, `.claude/agents/`, `.claude/rules/` e `.claude/settings.json` integram o harness ao Claude Code atual. Plugins/mods permanecem opt-in e fora do caminho automático antes de T8.

## Capabilities visuais

`scripts/detect_capabilities.py` trata `vision_input` e `visual_generation` separadamente. Sem visão, o sistema só pode raciocinar sobre descrição/texto/metadata fornecidos. Sem geração visual, ainda pode produzir fonte editável de diagrama, mas deve declarar que não houve render.

## Portão de qualidade

```bash
python3 scripts/quality_gate.py --config quality-gate.repo.json
python3 scripts/quality_gate.py --config quality-gate.repo.json --execute
```

Sem `--execute`, o runner não executa checks.

## Memória e aprendizado

`/aprender` propõe aprendizado após uma execução. Conteúdo persistido deve estar sanitizado; conhecimento específico do projeto usa `project_knowledge` e fica ignorado pelo Git por padrão. Falhas recorrentes podem virar bundles de regressão com oracle explícito e `REVIEW_REQUIRED`.

## Avaliação

Fixtures executáveis provam propriedades concretas de frameworks/runtimes, não que a skill melhora um agente. O protocolo A/B mantém mesmo modelo/acesso/contexto nos dois braços. `evals/agentic/` cobre também desenho técnico e degradação visual; `evals/visual/` protege contra falsa precisão, falsa renderização e excesso de detalhe no modo simples.

Uma **rodada real de eficácia é bloqueada por padrão** até existir revisão humana independente registrada do oracle para todos os casos selecionados. O registro é vinculado por hashes normalizados de `evals/cases.json` e `evals/oracle.json`, então uma mudança no gabarito invalida a aprovação anterior.

```bash
python3 scripts/eval_protocol.py template \
  --out evals/oracle-review.json \
  --case-id runtime-port-binding \
  --case-id external-contract-required \
  --case-id local-evidence-sufficient \
  --case-id java-404

# após uma segunda pessoa revisar e preencher o registro
python3 scripts/eval_protocol.py verify \
  --review evals/oracle-review.json \
  --case-id runtime-port-binding \
  --case-id external-contract-required \
  --case-id local-evidence-sufficient \
  --case-id java-404
```

`--smoke-test` no runner existe para validar isolamento, cegamento e reconciliação com agente simulado; mesmo quando o critério matemático passa, o relatório marca essa execução como **não utilizável para alegação de eficácia**.

O runner também mede `treatment_observed` pela leitura real da skill, usa `applicable_dimensions` fixas do oracle, preserva falhas como não-vitória e congela o efeito mínimo por hash. O experimento de descobribilidade usa `--experiment-mode discoverability` e é analisado separadamente por `scripts/analyze_discoverability.py`.

## Uso regulado

A skill pública não contém política específica de banco, sistema interno ou dados reais. Dados corporativos, secrets e código proprietário não devem ser promovidos ao repositório público; políticas locais mais restritivas prevalecem.

## Manutenção

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_repo.py
python3 scripts/validate_agentic.py
python3 scripts/quality_gate.py --config quality-gate.repo.json --execute
```

`SKILL.md` mantém orçamento máximo de **14.420 bytes**; detalhe adicional fica em referências ou componentes agentic. Toda nova regra deve vir acompanhada de caso/fixture quando aplicável. A licença está em [LICENSE](LICENSE).
