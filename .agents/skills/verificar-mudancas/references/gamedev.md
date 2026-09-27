# Engenharia de jogos

Usar quando a mudança envolver gameplay, game loop, física, input, cenas/telas, assets, geração procedural, save/load, multiplayer ou performance em runtime. Esta referência é independente de engine: combinar com a referência da stack quando houver uma especialização, por exemplo `java.md` em LibGDX ou `unity-csharp.md` em Unity.

## Descobrir o contexto real

- Identificar engine/framework e versão, plataforma alvo, modo de execução (Editor, desktop, mobile, console, headless), cena/tela/estado inicial e comandos reais de build/teste.
- Mapear o caminho relevante: input/evento → atualização de estado → física/simulação → animação/renderização → efeito visível. Não tratar sintoma visual como prova de que a causa está no renderer.
- Identificar ownership e ciclo de vida de entidades, componentes, sistemas, telas/cenas, assets e recursos nativos. Verificar criação, ativação, desativação, troca de estado e descarte.
- Quando houver ECS ou arquitetura semelhante, confirmar quem cria, lê e modifica cada componente e em que ordem os sistemas executam.

## Tempo, game loop e física

- Distinguir update variável, fixed timestep e render. Verificar uso de `delta time`, time scale, pause e ordem das etapas quando o comportamento muda com FPS.
- Movimento, cooldown, animação ou spawn que dependem de tempo devem ser testados em mais de uma taxa de frames quando houver risco de dependência de FPS.
- Em física, conferir timestep, layers/masks, triggers, collision callbacks, teleporte/movimento direto de transform e sincronização entre estado lógico e corpo físico conforme a engine.
- Não corrigir jitter ou tunneling apenas aumentando frequência/timestep sem medir custo e confirmar a causa.

## Estado, input, assets e cenas

- Verificar transições entre menu, gameplay, pause, restart, respawn e mudança de cena/tela. Estado global ou singleton pode sobreviver mais do que o esperado.
- Em input, diferenciar evento único de estado contínuo, device mapping, foco da janela e plataforma. Evitar lógica cujo resultado dependa de quantas vezes o frame atualiza.
- Em assets, conferir carregamento assíncrono, disponibilidade antes do uso, ownership, cache e descarte. Não resolver vazamento apenas mantendo assets vivos indefinidamente.
- Para pooling, confirmar reset completo do objeto antes de reutilização; estado residual pode gerar bugs intermitentes.

## Determinismo e geração procedural

- Para reprodução, registrar seed e todas as fontes de aleatoriedade relevantes. Uma seed só torna o caso reproduzível se o fluxo consumir RNG de forma determinística.
- Verificar fontes adicionais de não determinismo: ordem de iteração, concorrência, tempo do sistema, floats, física e chamadas aleatórias fora do gerador controlado.
- Em geração procedural, provar invariantes do mapa/nível além de apenas comparar uma imagem: conectividade, limites, spawn válido, colisão, navegação e condições de vitória/saída quando pertinentes.

## Multiplayer e estado compartilhado

- Quando houver rede, combinar com `distributed-systems.md` e a referência específica da engine quando existir.
- Seguir ação local → autoridade → estado canônico → replicação → estado observado por cada cliente. Distinguir host, cliente remoto e late join.
- Verificar idempotência de comandos/eventos, ordenação, reconciliação, ownership e comportamento sob latência/perda/reenvio quando fizerem parte da falha.
- Não considerar estado correto no host como prova de sincronização dos demais clientes.

## Save/load e compatibilidade

- Identificar formato e versão do save, campos persistentes e política de compatibilidade. Mudança de estrutura pode exigir migração de saves existentes.
- Testar novo save, save anterior suportado, dados incompletos/corrompidos quando relevante e comportamento após atualizar versão do jogo.
- Não apagar ou recriar automaticamente saves incompatíveis sem requisito explícito e estratégia de recuperação adequada.

## Performance de jogo

- Medir frame time e separar CPU, GPU, memória/GC, I/O, asset loading, física, render/draw calls e rede antes de otimizar.
- Procurar alocações por frame, criação/destruição excessiva, carregamento síncrono no loop, N operações por entidade, atualizações desnecessárias e picos, quando sustentados por profiling.
- FPS médio não mostra sozinho stutter. Considerar distribuição de frame time e picos quando o problema for fluidez.
- Não declarar ganho de FPS, redução de GC ou melhora de loading sem medição comparável antes/depois.

## Provar na fronteira correta

- Regra determinística isolada pode ser testada fora da runtime; lifecycle, física, input, render, multiplayer e integração com a engine precisam de prova em runtime apropriada.
- Quando possível, reproduzir também no build/plataforma alvo. Comportamento no Editor ou desktop não prova Android, console ou build release.
- Para bug visual, registrar estado lógico e visual no mesmo momento para distinguir dado incorreto de apresentação incorreta.
- Para regressão temporal, executar condições controladas de FPS/timestep/seed e preservar um cenário vizinho funcional.

## Entrega específica

Relatar engine/framework e target, estado/cena, condição de reprodução, seed/FPS quando relevantes, fronteira realmente exercitada, métricas medidas e comportamento não verificado. Não afirmar que gameplay, sincronização, física ou performance foram validados apenas porque o código compilou ou um teste unitário passou.
