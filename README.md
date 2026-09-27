# Verificar mudanças

Skill portátil para agentes de programação, inspirada no ciclo de engenharia do [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Orienta investigação de bugs, planejamento proporcional, testes de comportamento, implementação, revisão crítica e verificação final.

Funciona em projetos Java, Python, dados e outras stacks. Não instala nem depende do ECC. Seu resultado depende do acesso ao código, às ferramentas, aos testes e à evidência disponível; nenhuma skill garante encontrar todos os defeitos.

## Instalação no projeto

Copie o arquivo `SKILL.md` deste repositório para:

```text
SEU-PROJETO/.agents/skills/verificar-mudancas/SKILL.md
```

Faça commit do arquivo para disponibilizá-lo aos agentes que reconhecem o padrão Agent Skills. O Devin descobre skills nessa pasta e pode selecioná-las quando a descrição for relevante. Você também pode pedir `@skills:verificar-mudancas` no prompt do Devin.

Para vários projetos, copie a mesma pasta para cada repositório ou use o mecanismo de skills compartilhadas oferecido pela ferramenta e organização.

## Exemplo de uso

```text
Investigue a falha descrita no processamento de pedidos. Localize a causa,
reproduza com um teste quando possível, implemente a correção, revise o diff
e execute novamente as verificações relevantes.
@skills:verificar-mudancas
```

## Conteúdo

- `.agents/skills/verificar-mudancas/SKILL.md`: procedimento reutilizável.

Em ambientes corporativos, respeite as regras da organização para uso de IA, repositórios, plugins, código e dados internos.
