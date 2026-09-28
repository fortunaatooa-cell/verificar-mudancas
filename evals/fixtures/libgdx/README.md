# Fixture executável — LibGDX

Valida os casos `libgdx-shared-asset-lifecycle` e `libgdx-input-multiplexer-leak` contra classes reais do LibGDX, sem exigir OpenGL real.

## Revisão testada

Por padrão o runner fixa o LibGDX em:

`e1d69884015ca19061647505f9509db34df5cc82`

Essa revisão declara `version=1.14.3` em `gradle.properties`. O valor pode ser sobrescrito com `LIBGDX_REF`, mas qualquer resultado deve registrar a revisão efetivamente usada.

## Executar

```bash
bash evals/fixtures/libgdx/run.sh
```

O runner baixa o código-fonte, compila `gdx/src` com stubs mínimos para ambiente sem OpenGL e executa `Fixtures.java`.

## O que a fixture prova

- ordem `hide()` → troca de `Screen` → `show()` em `Game.setScreen`;
- ausência de `dispose()` automático da tela antiga em `setScreen`;
- efeito de reference count de `AssetManager` em `load`/`unload` para asset já carregado;
- diferença entre processor que consome evento e processor que retorna `false` em `InputMultiplexer`;
- `Stage.dispose()` não remove automaticamente o `Stage` de um `InputMultiplexer`.

## Limites

A fixture usa stubs para `Gdx.app`, `Gdx.graphics` e GL, um viewport de teste e um asset falso. Ela valida lifecycle e lógica dessas classes, mas **não** prova renderização, áudio, comportamento Android/iOS, drivers OpenGL ou o runtime de um jogo real. O resultado também não mede impacto da skill sobre agentes; isso exige comparação A/B independente.
