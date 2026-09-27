# Verificar mudanças

Skill portátil de engenharia inspirada no ciclo do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Ajuda agentes a investigar falhas, implementar mudanças e apresentar evidências verificáveis sem depender de uma linguagem, ferramenta ou ecossistema específico.

O ciclo principal é:

**investigar → classificar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

Antes de implementar, a skill classifica o tipo de tarefa, transforma a solicitação em critérios observáveis de aceite e ajusta a profundidade conforme o risco. Mudanças locais podem ter processo curto; contratos, segurança, dados, infraestrutura e ações difíceis de reverter exigem blast radius, recuperação, stop conditions e verificação mais ampla.

O resultado depende do acesso permitido ao projeto, da qualidade da evidência e das ferramentas disponíveis. Existem casos de avaliação, mas **não há ainda comparação empírica publicada que demonstre ganho de precisão**. Nenhuma skill garante detectar todos os defeitos.

## Arquitetura

A skill evita concentrar toda engenharia em um único prompt. O núcleo pode ser combinado, sob demanda, com três camadas:

1. **Referência de stack/contexto** — Java/Spring, Python, engenharia de jogos independente de engine, C#/Unity, dados ou Terraform/IaC.
2. **Referências transversais** — segurança, APIs/contratos, bancos/migrações, sistemas distribuídos, observabilidade/SRE, CI/CD, performance, dependências/supply chain, arquitetura/refatoração, frontend/E2E e containers/cloud runtime.
3. **Playbook de tarefa** — bug fix, feature, refatoração, migração, incidente, upgrade de dependência ou regressão de performance.

Em jogos, `gamedev.md` cobre conceitos independentes de engine e deve ser combinado com a stack específica quando pertinente. Exemplos:

```text
"API Java duplicando mensagens após retry"

core
+ java.md
+ distributed-systems.md
+ observability-sre.md
+ bug-fix.md
```

```text
"Personagem do LibGDX anda mais rápido em monitor de 144 Hz"

core
+ gamedev.md
+ java.md
+ performance.md
+ bug-fix.md
```

```text
"No Unity o host destrói o bloco, mas o cliente ainda o vê"

core
+ gamedev.md
+ unity-csharp.md
+ distributed-systems.md
+ bug-fix.md
```

O agente deve carregar somente o que for pertinente ao problema; a arquitetura modular existe para ampliar a análise sem inflar o contexto de todas as tarefas.

## Conteúdo

- [SKILL.md](.agents/skills/verificar-mudancas/SKILL.md): ciclo universal, classificação, risco, critérios de aceite, stop conditions, revisão e verificação.
- [Referências](.agents/skills/verificar-mudancas/references/): conhecimento por stack e por preocupação transversal, incluindo [engenharia de jogos](.agents/skills/verificar-mudancas/references/gamedev.md) independente de engine.
- [Playbooks](.agents/skills/verificar-mudancas/playbooks/): variações do processo conforme o tipo de tarefa.
- [Prompt para chat](prompt-chat-equipe.md): versão para ferramentas sem acesso ao repositório.
- [Avaliações](evals/README.md): casos, oracle e critérios para comparar versões e ferramentas.

## Usar em diferentes ferramentas

| Superfície | Como disponibilizar | Limite a verificar |
| --- | --- | --- |
| Devin | Conectar este repositório à organização; o Devin indexa `SKILL.md` em `.agents/skills/`. Invocar `@skills:verificar-mudancas` ou permitir seleção automática. | Uma nova skill ativa pode substituir a anterior. As referências/playbooks precisam estar acessíveis na sessão. |
| GitHub Copilot para programação | Instalar a pasta `.agents/skills/verificar-mudancas/` no projeto ou no local de skills suportado pela superfície. | Confirmar descoberta da skill e acesso real ao código/testes. |
| Claude Code, Codex ou outro agente de programação | Instalar a pasta completa no local aceito pela ferramenta e verificar descoberta. | Localização, composição de skills e ferramentas variam; `SKILL.md` não concede acesso por si só. |
| Copilot no Teams / Microsoft 365 | Para chat comum, fornecer [o prompt](prompt-chat-equipe.md) e o contexto permitido. | Não presumir execução de testes ou instalação automática da skill a partir do GitHub. |
| Qualquer chat sem acesso ao projeto | Colar [o prompt](prompt-chat-equipe.md) e compartilhar apenas trechos, prints ou logs autorizados. | Receber diagnóstico e roteiro de verificação, não uma correção executada. |

Para projetos que precisem de uma versão fixada, copiar a **pasta inteira** da skill a partir de uma tag ou commit específico. Copiar somente `SKILL.md` remove referências e playbooks especializados.

Exemplo de instalação em um projeto já clonado:

```bash
mkdir -p /caminho/do/projeto/.agents/skills
cp -R .agents/skills/verificar-mudancas /caminho/do/projeto/.agents/skills/
```

No Windows PowerShell, use `Copy-Item -Recurse`. Confirme no próprio agente que a skill aparece e consegue abrir os arquivos pertinentes.

## Exemplo

```text
Investigue a falha descrita no processamento de pedidos. Classifique a tarefa e o risco,
defina critérios de aceite, diferencie hipótese de causa confirmada, reproduza quando
possível, implemente a menor correção, revise riscos e verifique a fronteira afetada
após a última alteração. Use verificar-mudancas.
```

## Manutenção pelo time

Antes de publicar mudanças, execute `python3 scripts/validate_repo.py` e use os casos de [evals](evals/README.md) para comparar a versão nova com a anterior. A validação automática confere estrutura e integridade; qualidade de diagnóstico exige execução dos casos e revisão humana ou avaliador aprovado pelo time.

Registre aprendizados sem dados de clientes ou código interno no repositório público. Conhecimento específico deve permanecer no projeto autorizado; promova para o núcleo somente padrões recorrentes e verificáveis. A licença está em [LICENSE](LICENSE).
