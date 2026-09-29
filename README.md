# Verificar mudanças

Skill portátil de engenharia inspirada no ciclo do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Ajuda agentes a investigar falhas, implementar mudanças, analisar desenhos técnicos e apresentar evidências verificáveis sem depender de uma linguagem, ferramenta ou ecossistema específico.

**investigar → classificar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

Antes de implementar, a skill classifica a tarefa, transforma a solicitação em critérios observáveis de aceite e ajusta a profundidade conforme o risco. Mudanças locais podem ter processo curto; contratos, segurança, dados, infraestrutura e ações difíceis de reverter exigem blast radius, recuperação, stop conditions e verificação mais ampla.

O resultado depende do acesso permitido ao projeto, da qualidade da evidência e das ferramentas disponíveis. Existem casos e fixtures, mas **não há ainda comparação empírica publicada que demonstre ganho de precisão**. Nenhuma skill garante detectar todos os defeitos.

## Arquitetura

O núcleo é combinado sob demanda com:

1. **Referência de stack/contexto** — Java/Spring, Python, game development, LibGDX, C#/Unity, dados ou Terraform/IaC.
2. **Referências transversais** — segurança, APIs/contratos, bancos/migrações, distribuídos, observabilidade, CI/CD, performance, supply chain, arquitetura, frontend/E2E, containers/cloud runtime, evidência de mudança e perfil regulado.
3. **Capacidades visuais** — [desenhos técnicos e evidência visual](.agents/skills/verificar-mudancas/references/technical-drawings.md), com leitura evidence-first e criação em representação compatível com a ferramenta.
4. **Modos de resposta** — [simples, aprofundado ou ambos](.agents/skills/verificar-mudancas/references/response-modes.md), sem reduzir o rigor da evidência.
5. **Playbook de tarefa** — bug fix, feature, refatoração, migração, incidente, upgrade de dependência ou regressão de performance.

O agente deve carregar somente o que for pertinente. A arquitetura modular existe para ampliar a análise sem inflar o contexto de todas as tarefas.

## Desenhos técnicos

A skill pode interpretar diagramas de arquitetura, fluxo, sequência, rede/infra, dados e outros desenhos técnicos quando a ferramenta realmente tiver acesso ao artefato. Também orienta a criação/redesenho em Mermaid, PlantUML, DOT, SVG ou formatos CAD quando houver capability e dados suficientes. Medidas, escala, tolerâncias e normas ausentes nunca devem ser inventadas; imagem gerativa sem garantia geométrica é tratada como ilustrativa.

## Conteúdo

- [SKILL.md](.agents/skills/verificar-mudancas/SKILL.md): ciclo universal, classificação, risco, critérios de aceite, stop conditions, revisão e verificação.
- [Referências](.agents/skills/verificar-mudancas/references/): conhecimento por stack e por preocupação transversal.
- [Desenhos técnicos](.agents/skills/verificar-mudancas/references/technical-drawings.md): análise visual estruturada, incerteza, criação/redesenho e limites de precisão.
- [Modos de resposta](.agents/skills/verificar-mudancas/references/response-modes.md): saída simples, aprofundada ou combinada.
- [Evidência de mudança](.agents/skills/verificar-mudancas/references/change-evidence.md): pacote genérico para PR/change record/auditoria.
- [Perfil regulado](.agents/skills/verificar-mudancas/references/regulated-profile.md): baseline conservador para ambientes controlados; políticas locais mais restritivas prevalecem.
- [Playbooks](.agents/skills/verificar-mudancas/playbooks/): variações conforme o tipo de tarefa.
- [Prompt para chat](prompt-chat-equipe.md): versão para ferramentas sem acesso ao repositório.
- [Avaliações](evals/README.md): casos, oracle, fixtures e protocolo A/B; [evals visuais](evals/visual/README.md) cobrem a nova capacidade.
- [Contribuição](CONTRIBUTING.md) e [changelog](CHANGELOG.md): regras de evolução e versionamento.

## Uso em diferentes ferramentas

| Superfície | Como disponibilizar | Limite a verificar |
| --- | --- | --- |
| Devin | Conectar o repositório e carregar `.agents/skills/verificar-mudancas/`. | Confirmar acesso real a imagens/arquivos e ferramentas de desenho. |
| GitHub Copilot | Instalar a pasta da skill no projeto/local suportado. | Confirmar descoberta, código e capabilities visuais disponíveis. |
| Claude Code, Codex ou outro agente | Instalar a pasta completa no local aceito pela ferramenta. | Ferramentas, visão, geração de imagem e composição de skills variam por harness. |
| Chat/Teams sem acesso ao projeto | Fornecer [o prompt](prompt-chat-equipe.md) e contexto permitido. | Receber diagnóstico/roteiro; imagens só podem ser analisadas se a superfície realmente as fornecer. |

Para uso corporativo, fixe uma **tag ou commit aprovado**; não dependa de `main`. Copiar somente `SKILL.md` remove referências e playbooks.

## Avaliação

As fixtures executáveis provam propriedades concretas de frameworks/runtimes. Elas **não** provam que a skill melhora um agente. Para isso existe o protocolo [A/B controlado](evals/ab/README.md).

Piloto inicial: quatro casos (`runtime-port-binding`, `external-contract-required`, `local-evidence-sufficient`, `java-404`), três repetições por braço e o mesmo modelo/acesso/contexto. Com Codex CLI autenticado, o benchmark pode ser executado em sessões isoladas com:

```bash
python3 scripts/run_agent_eval.py \
  --out eval-runs/pilot-001 \
  --model <modelo-fixado> \
  --reasoning-effort medium \
  --web-search live
```

O runner produz respostas cegadas, metadata operacional e `grading.csv`. Depois da pontuação cega:

```bash
python3 scripts/analyze_ab_results.py --run-dir eval-runs/pilot-001
```

Também é possível apenas gerar manifests com `scripts/prepare_ab_eval.py`. O `scorecard.csv` registra pontuação, violações, tempo até conclusão útil e tamanho da resposta. Resultados negativos também devem ser preservados.

## Uso regulado

A skill pública **não contém política específica de banco, sistema interno ou dados reais**. O perfil regulado parte de defaults conservadores: sem dados de clientes, sem segredo, sem ação em produção por inferência, busca externa desabilitada até política local permitir e aprovação humana para HIGH/CRITICAL. O processo local autorizado deve adaptar os campos de mudança e controles específicos sem publicá-los aqui.

## Manutenção

Antes de publicar mudanças:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_repo.py
```

As dependências acima servem à manutenção do repositório; não são necessárias para usar a pasta da skill em outro projeto. Os testes do validador cobrem YAML e entradas inválidas, não o raciocínio do agente.

O CI também executa as fixtures. `SKILL.md` possui orçamento máximo de **14.420 bytes**; detalhe adicional deve ir para referências. Toda nova regra precisa de caso/fixture correspondente, conforme [CONTRIBUTING.md](CONTRIBUTING.md).

Registre aprendizados sem dados de clientes ou código interno. Conhecimento específico deve permanecer no projeto autorizado; promova para o núcleo somente padrões recorrentes e verificáveis. A licença está em [LICENSE](LICENSE).
