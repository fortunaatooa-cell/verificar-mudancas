# AGENTS.md — Verificar Mudanças para Devin

Este workspace instala o **Verificar Mudanças v3.1 Engineering Lifecycle** no Devin.

## Regra principal

Use `.agents/skills/verificar-mudancas/SKILL.md` como núcleo metodológico quando a tarefa envolver engenharia de software, investigação, mudança, testes, arquitetura, runtime, segurança, dados, infraestrutura ou desenho técnico.

As skills auxiliares são especializações carregadas sob demanda. Não carregue tudo automaticamente.

## Orquestração padrão

1. Entenda a solicitação e descubra a capacidade real da sessão.
2. Classifique tarefa, critérios de aceite e risco.
3. Se houver bug/incidente: investigue antes de editar.
4. Se a mudança for ampla/ambígua: use `planejamento`.
5. Se houver decisão estrutural: use `arquitetura`.
6. Se houver comportamento testável: use `estrategia-testes`; TDD somente com RED real.
7. Implemente a menor mudança correta.
8. Faça revisão adversarial; ative segurança quando pertinente.
9. Verifique claims com evidência depois da última alteração.
10. Registre aprendizado somente quando útil e autorizado.

## Skills auxiliares

- `.agents/skills/investigar/SKILL.md`
- `.agents/skills/planejamento/SKILL.md`
- `.agents/skills/arquitetura/SKILL.md`
- `.agents/skills/estrategia-testes/SKILL.md`
- `.agents/skills/revisar-mudanca/SKILL.md`
- `.agents/skills/revisar-seguranca/SKILL.md`
- `.agents/skills/diagnosticar-runtime/SKILL.md`
- `.agents/skills/desenho-tecnico/SKILL.md`

## Uso das capacidades do Devin

Devin normalmente trabalha em uma máquina com repositórios, terminal e ambiente de desenvolvimento configurados. Mesmo assim, **detectar antes de assumir**.

Quando o repositório estiver disponível:
- leia instruções do projeto;
- rode `git status --short` antes de editar;
- preserve trabalho preexistente;
- descubra os comandos reais de build/test/lint;
- execute provas relevantes depois da última alteração;
- revise `git diff` e arquivos não rastreados;
- não faça deploy/ação destrutiva sem escopo e autorização compatíveis.

Quando uma capability não estiver disponível, degrade para análise e instruções verificáveis; nunca fabrique execução.

## Modos de resposta

- `simples`: conclusão + evidência essencial + risco/lacuna + próximo passo.
- `aprofundado`: contexto, evidências, hipóteses, alternativas, prova e riscos.
- `ambos`: resumo simples seguido de análise completa.

## Intenções / macros

Os arquivos em `devin/playbooks/` são templates para Settings → Playbooks:
`!verificar`, `!investigar`, `!planejar`, `!arquitetura`, `!tdd`, `!revisar`, `!runtime`, `!desenho`.

Os playbooks são atalhos; as regras de evidência continuam vindo das skills.

## Invariantes

- evidência antes de confiança;
- observado ≠ inferido ≠ proposto;
- causa antes de correção;
- `tamanho de JAR/lib != consumo de RAM`;
- CI verde != produção saudável;
- ADR != arquitetura implantada;
- desenho != runtime;
- deploy sem erro != serviço saudável;
- teste escrito depois != RED de TDD;
- documentação externa prova contrato, não estado observado;
- não inventar execução, medida, requisito, segredo ou acesso.
