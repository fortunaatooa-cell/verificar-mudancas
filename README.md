# Verificar mudanças

Skill portátil de engenharia inspirada no ciclo do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Ajuda agentes a investigar falhas, analisar testes, implementar mudanças e apresentar evidências da verificação. O núcleo não depende do ECC nem de uma linguagem específica; as referências opcionais tratam Java/Spring, Python, C#/Unity, dados e Terraform/IaC.

O ciclo principal da skill é:

**investigar → planejar → testar/provar → implementar → revisar → verificar → aprender → melhorar**

A profundidade das etapas varia conforme o risco. Uma correção pequena pode ter planejamento mínimo; mudanças amplas, migrações, infraestrutura e efeitos em dados exigem planejamento explícito, critérios de aceite e estratégia de reversão.

O resultado depende do acesso permitido ao projeto, da qualidade da evidência e das ferramentas disponíveis. Esta versão contém casos de avaliação, mas **não há ainda comparação empírica publicada que demonstre ganho de precisão**. Nenhuma skill garante detectar todos os defeitos.

## Conteúdo

- [SKILL.md](.agents/skills/verificar-mudancas/SKILL.md): procedimento universal e critérios de evidência.
- [Referências](.agents/skills/verificar-mudancas/references/): perguntas e verificações por contexto; carregar somente a referência aplicável, incluindo Terraform/IaC para mudanças de infraestrutura declarativa.
- [Prompt para chat](prompt-chat-equipe.md): uso quando a ferramenta tem apenas conversa ou prints.
- [Avaliações](evals/README.md): casos sem dados internos e critérios de comparação entre ferramentas e versões.

## Usar em diferentes ferramentas

| Superfície | Como disponibilizar | Limite a verificar |
| --- | --- | --- |
| Devin | Conectar este repositório à organização; o Devin indexa `SKILL.md` em `.agents/skills/`. Invocar `@skills:verificar-mudancas` ou permitir seleção automática. | Uma nova skill ativa substitui a anterior no Devin. As referências devem estar acessíveis no contexto da sessão; caso contrário, usar o núcleo. |
| GitHub Copilot para programação | Instalar a pasta `.agents/skills/verificar-mudancas/` no projeto ou no local de skills pessoais suportado pela superfície. | Confirmar a descoberta da skill e o acesso ao código/testes na modalidade usada. |
| Claude Code, Codex ou outro agente de programação | Instalar a pasta completa no local de skills aceito pela ferramenta e verificar sua descoberta. | Localização, composição de skills e ferramentas variam; `SKILL.md` não concede acesso por si só. |
| Copilot no Teams / Microsoft 365 | Para chat comum, fornecer [o prompt](prompt-chat-equipe.md) e o contexto permitido. Skills de agente declarativo exigem configuração própria, quando disponíveis para a organização. | Não presumir que publicar no GitHub instala a skill no Teams, nem que o chat consegue executar testes. |
| Qualquer chat sem acesso ao projeto | Colar [o prompt](prompt-chat-equipe.md) e compartilhar apenas trechos, prints ou logs autorizados. | Receber um roteiro de diagnóstico, não uma correção verificada. |

Para projetos que precisem de uma versão fixada, copiar a **pasta inteira** da skill a partir de uma tag ou commit específico. Registrar qual versão cada projeto usa e revisar atualizações em conjunto; copiar somente `SKILL.md` elimina as referências especializadas. Para o Devin, o repositório separado conectado pode servir como catálogo; a cópia para cada projeto é uma decisão de distribuição, não um requisito universal.

Exemplo de instalação em um projeto já clonado, a partir de uma cópia revisada deste repositório:

```bash
mkdir -p /caminho/do/projeto/.agents/skills
cp -R .agents/skills/verificar-mudancas /caminho/do/projeto/.agents/skills/
```

No Windows PowerShell, use `Copy-Item -Recurse` para copiar a pasta inteira. Substitua o caminho de exemplo pelo projeto autorizado e confirme no próprio agente que a skill aparece e consegue abrir a referência aplicável.

## Exemplo

```text
Investigue a falha descrita no processamento de pedidos. Diferencie hipótese
de causa confirmada, reproduza quando possível, corrija o problema e verifique
o contrato afetado após a última alteração. Use verificar-mudancas.
```

## Manutenção pelo time

Antes de publicar mudanças na skill, execute `python3 scripts/validate_repo.py` e use os casos de [evals](evals/README.md) para comparar a versão nova com a anterior. A verificação automática confere estrutura e integridade dos exemplos; a avaliação da qualidade de diagnóstico exige execução e revisão humana ou um avaliador aprovado pelo time.

Registre novos aprendizados sem dados de clientes ou código interno no repositório público. Adicione referências de projeto apenas no ambiente autorizado e revise mudanças na skill por PR ou pelo processo acordado pela equipe. A licença deste repositório está em [LICENSE](LICENSE).
