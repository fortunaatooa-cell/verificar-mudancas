# LibGDX

Usar quando o projeto for um jogo em LibGDX. Combinar com [engenharia de jogos](gamedev.md) para princípios independentes de engine e com [Java e Spring](java.md) apenas para aspectos gerais de Java/JVM; não aplicar convenções de backend Spring a um jogo.

## Descobrir a estrutura real do projeto

- Identificar versão do LibGDX, JDK, Gradle Wrapper, módulos existentes (`core`, `lwjgl3`, `android`, `ios`, `headless` ou equivalentes) e plataforma alvo. Não presumir a estrutura pelo template atual: projetos antigos podem usar `desktop` ou organização diferente.
- Descobrir tarefas Gradle reais do projeto antes de sugerir comandos de run/build/test. Separar erro do módulo `core` de erro específico de backend/plataforma.
- Identificar a abstração de ciclo de vida usada: `ApplicationListener`, `ApplicationAdapter`, `Game` + `Screen` ou arquitetura própria.

## Lifecycle, Screen e ownership

- Em `Game`/`Screen`, rastrear `show → render(delta) → resize → pause/resume → hide → dispose` e verificar quem realmente possui cada recurso.
- Não assumir que `hide()` implica descarte definitivo. Uma `Screen` pode voltar a ser usada; destruir recursos compartilhados em `hide()` pode quebrar outra tela ou retorno posterior.
- Definir ownership explícito de `Texture`, `Pixmap`, `SpriteBatch`, `ShapeRenderer`, `FrameBuffer`, `ShaderProgram`, `Mesh`, `Stage`, mapas e outros objetos `Disposable`. Recursos compartilhados devem ter um único owner responsável pelo `dispose()`.
- Em troca de telas, verificar estado global, listeners/input processors e referências ainda ativas para evitar vazamentos ou callbacks em objetos já descartados.

## Render loop e tempo

- Em `render(delta)`, distinguir atualização de simulação, física e desenho. Aplicar princípios de `delta time` e fixed timestep de `gamedev.md` conforme o comportamento real do jogo.
- Evitar carregar assets, criar coleções temporárias grandes, compilar shaders ou executar I/O síncrono no caminho de renderização sem evidência de que é aceitável.
- Ao usar `SpriteBatch`, verificar pares `begin()/end()`, troca excessiva de textura/shader e chamadas que forçam flush quando houver problema de render ou performance.
- Não usar FPS médio como única prova de fluidez; medir frame time/picos quando houver stutter.

## Assets

- Quando houver `AssetManager`, confirmar fila de carregamento, `update()`/`finishLoading()`, momento em que `get()` é chamado, referência compartilhada e política de `unload()`/`dispose()`.
- Não misturar ownership entre `AssetManager` e descarte manual do mesmo asset sem entender quem controla o ciclo de vida.
- Em carregamento assíncrono, provar que o recurso está disponível antes do uso e que a tela de loading/transição não bloqueia o render loop desnecessariamente.
- Para atlas, fontes, skins e mapas, verificar dependências carregadas e descarte em conjunto conforme o mecanismo usado pelo projeto.

## Input e Scene2D

- Confirmar se o projeto usa polling (`Gdx.input`) ou `InputProcessor`/`InputMultiplexer`. Verificar instalação e remoção do processor ao trocar de tela.
- Em Scene2D, separar `Stage.act(delta)` de `Stage.draw()` e verificar viewport/camera, foco, propagação de eventos e coordenadas de tela/mundo quando o bug depender de interação.
- Não corrigir input duplicado apenas adicionando guards se houver múltiplos processors/listeners registrados por lifecycle incorreto.

## Física e Box2D

- Se houver Box2D, confirmar timestep, accumulator/fixed step, unidades, criação/destruição de bodies e momento seguro para alterar o `World`.
- Não criar ou destruir bodies durante callback de contato se a API/fluxo do projeto exigir adiar a mutação; usar a estratégia existente do jogo para filas de operações quando necessário.
- Verificar sincronização entre body físico e representação visual. Alterar apenas sprite/posição visual não prova que o estado físico foi atualizado.

## Threads e contexto gráfico

- Tratar objetos gráficos/OpenGL como dependentes da thread/contexto apropriados. Trabalho assíncrono pode preparar dados, mas criação/uso de recursos gráficos precisa respeitar as restrições do backend.
- Ao usar threads, executors ou callbacks assíncronos, verificar sincronização com o estado do jogo e descarte durante troca de tela/shutdown.
- Não considerar um teste headless como prova de renderização, OpenGL, input real ou comportamento do backend desktop/mobile.

## Testes e prova

- Manter regras determinísticas de gameplay separadas do framework quando isso facilitar testes unitários sem contexto gráfico.
- Usar backend/headless ou testes JVM para lógica que não depende de OpenGL, mas executar runtime real para lifecycle, render, input, assets nativos, áudio, física e comportamento específico de plataforma quando esses forem a fronteira da falha.
- Para bug de lifecycle, testar pelo menos entrada na tela, saída e retorno quando esse ciclo for relevante.
- Para asset/resource leak, observar criação/descarte e, quando disponível, profiling/memória antes/depois; não inferir vazamento apenas porque existe um `Disposable` sem `dispose()` visível em um trecho isolado.

## Plataforma alvo

- Diferenciar desktop/LWJGL3, Android, iOS e headless. Filesystem, lifecycle, input, permissões, densidade/resolução, performance e disponibilidade de APIs podem variar.
- Um bug que só ocorre no Android deve ser reproduzido ou verificado no target apropriado quando possível; execução desktop não prova equivalência.

## Entrega específica

Relatar versão do LibGDX/JDK, módulos e target envolvidos, lifecycle observado, owner dos recursos afetados, comandos reais usados, prova em JVM versus runtime gráfico e qualquer comportamento ainda não exercitado na plataforma alvo. Não afirmar que o jogo foi verificado em runtime apenas porque `core` compilou ou testes JVM passaram.
