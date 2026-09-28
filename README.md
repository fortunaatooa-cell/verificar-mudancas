# Verificar mudanças

Skill e sistema portátil de engenharia inspirado no ciclo do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Ajuda agentes a investigar falhas, implementar mudanças e apresentar evidências verificáveis sem depender de uma linguagem, ferramenta ou ecossistema específico.

**investigar → classificar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

Antes de implementar, o sistema classifica a tarefa, transforma a solicitação em critérios observáveis de aceite e ajusta a profundidade conforme o risco. Mudanças locais podem ter processo curto; contratos, segurança, dados, infraestrutura e ações difíceis de reverter exigem controles adicionais.

O resultado depende do acesso permitido ao projeto, da qualidade da evidência e das ferramentas disponíveis. Existem casos e fixtures, mas **não há ainda comparação empírica publicada que demonstre ganho de precisão**. Nenhuma skill garante detectar todos os defeitos.

## Arquitetura

O núcleo é `.agents/skills/verificar-mudancas/` e continua utilizável sozinho. A instalação completa adiciona:

1. **Referências e playbooks sob demanda** — stack, runtime, dados, segurança, IaC, contratos e tipos de tarefa.
2. **Skills auxiliares** — `investigar`, `estrategia-testes`, `revisar-mudanca` e `diagnosticar-runtime` para composição em harnesses que suportem skills.
3. **Orquestração** — [AGENTS.md](AGENTS.md) e oito papéis especializados.
4. **Comandos em português** — `/verificar`, `/investigar`, `/corrigir`, `/revisar`, `/validar`, `/portao-qualidade` e `/aprender`.
5. **Regras e hooks** — evidência, testes, mudança segura, HIGH/CRITICAL, ambiente regulado, `pre-edit`, `post-edit` e `pre-finish`.
6. **Quality gate** — plano conservador e execução explícita de checks.
7. **Memória controlada** — lessons, patterns, incidents e project knowledge sanitizados; memória é pista, não verdade.
8. **Continuous learning seguro** — aprendizado explícito e geração revisável de eval de regressão, sem promoção automática ao core.
9. **Adapters** — generic, Codex, Claude, Devin e Copilot com capability detection/fallback, incluindo ferramentas externas.
10. **Instalador** — modo `skill` ou `full`, dry-run e preservação de arquivos existentes.

A especificação implementada está em [docs/agentic-system.md](docs/agentic-system.md) e a instalação em [docs/installation.md](docs/installation.md).

## Conteúdo

- [SKILL.md](.agents/skills/verificar-mudancas/SKILL.md): ciclo universal, classificação, risco, critérios de aceite, stop conditions, revisão e verificação.
- [Referências](.agents/skills/verificar-mudancas/references/) e [playbooks](.agents/skills/verificar-mudancas/playbooks/).
- [Agentes](.agents/agents/README.md), [comandos](.agents/commands/README.md), [regras](.agents/rules/README.md) e [hooks](.agents/hooks/README.md).
- [Memória](memory/README.md), [adapters](adapters/README.md), schemas portáteis em `schemas/` e [regressões geradas](evals/regression/README.md).
- [Avaliações](evals/README.md), [evals agentic](evals/agentic/README.md) e [A/B controlado](evals/ab/README.md).
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

Em uso corporativo, fixe uma **tag ou commit aprovado**; não dependa de `main`.

## Portão de qualidade

No próprio repositório:

```bash
python3 scripts/quality_gate.py --config quality-gate.repo.json
python3 scripts/quality_gate.py --config quality-gate.repo.json --execute
```

Sem `--execute`, o runner não executa os checks. Em projeto instalado, use `.verificar-mudancas/scripts/quality_gate.py`.

## Memória e aprendizado

`/aprender` propõe aprendizado após uma execução. Conteúdo persistido deve estar sanitizado e pode ser validado/pesquisado com `scripts/memory_store.py`. Conhecimento específico do projeto usa `project_knowledge` e fica ignorado pelo Git por padrão no repositório público. Uma ocorrência não vira regra universal automaticamente.

Falhas que não devem retornar podem virar bundles de regressão com `scripts/create_regression_eval.py`; expectativas e proibições são explícitas e o bundle nasce como `REVIEW_REQUIRED`.

## Uso em diferentes ferramentas

Os manifests em `adapters/` evitam assumir capacidades que podem variar por versão/sessão. `scripts/detect_capabilities.py` resolve o observável e mantém `unknown` quando não há prova. Sem subagentes, o sistema executa os mesmos papéis sequencialmente; sem hook nativo, pode usar `scripts/run_hook.py`.

## Avaliação

Fixtures executáveis provam propriedades concretas de frameworks/runtimes. Elas **não** provam que a skill melhora um agente. Para isso existe o protocolo A/B controlado com o mesmo modelo/acesso/contexto nos dois braços e avaliação cega quando possível.

Resultados negativos devem ser preservados. `evals/agentic/` protege também memória como pista, sanitização de aprendizado, quality gate sem falso PASS e degradação de adapter.

## Uso regulado

A skill pública não contém política específica de banco, sistema interno ou dados reais. O perfil regulado parte de defaults conservadores: sem dados de clientes no repositório público, sem ação em produção por inferência, ferramentas externas sujeitas à política local e aprovação humana para ações HIGH/CRITICAL quando aplicável.

## Manutenção

Antes de publicar mudanças:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_repo.py
python3 scripts/validate_agentic.py
python3 scripts/quality_gate.py --config quality-gate.repo.json --execute
```

`SKILL.md` mantém orçamento máximo de **14.420 bytes**; detalhe adicional deve ir para referências ou componentes agentic. Toda nova regra de engenharia deve vir acompanhada de caso/fixture quando aplicável.

Registre aprendizados sem dados corporativos ou código proprietário. Conhecimento específico permanece no projeto autorizado; promova ao núcleo somente padrões recorrentes e verificáveis. A licença está em [LICENSE](LICENSE).
