# C# e Unity

Ler quando houver C#; aplicar as partes de Unity somente se o projeto realmente usar o engine. Em .NET sem Unity, descobrir SDK, framework e runner do projeto (xUnit, NUnit, MSTest ou outro) antes de sugerir comandos.

## Separar lógica de runtime

- Em C# comum, proteger regras isoladas com testes unitários e verificar serialização, acesso a arquivos, rede ou banco na respectiva integração quando o defeito cruzar essa fronteira.
- Em Unity, verificar versão do Editor, plataforma alvo, cenas, prefabs, assemblies de testes e solução de rede adotada. Usar **Edit Mode** para lógica/editor apropriados e **Play Mode** para ciclo de vida, física, cena, animação e estado observado em execução. Não tratar um teste de Edit Mode como prova visual ou de integração multiplayer.
- Para estado sincronizado, seguir a ação do jogador → autoridade → alteração do estado compartilhado → replicação → renderização em cada cliente. Separar resultado visto pelo host do resultado visto por outro cliente ou por quem entra depois.

## Provar

- No multiplayer, quando a falha depender de rede, testar ao menos duas instâncias reais, preferencialmente em máquinas/processos distintos conforme o caso, com logs que identifiquem cliente, evento, estado e ordem. Testar latência/retry ou chegada tardia se forem plausíveis.
- Conferir se o teste foi executado na plataforma e cena corretas e após a última alteração. Para mapa e geração procedural, fixar a seed no caso determinístico e verificar também o comportamento de entrada/saída visível.
- Se não houver Editor ou build disponível, propor roteiro de reprodução e critérios de observação; não dizer que Unity, jogo, frame rate ou sincronização foram verificados só porque o código C# compilou.

## Entrega específica

Informar modo de teste, versão/target quando relevantes, instâncias observadas, diferenças entre host e cliente e qual comportamento permanece sem teste na runtime.
