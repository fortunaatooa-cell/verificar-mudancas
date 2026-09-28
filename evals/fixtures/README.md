# Fixtures executáveis

As fixtures complementam `cases.json` e `oracle.json` com comportamento reproduzível.

Há três níveis de evidência distintos:

1. `cases.json` + `oracle.json`: avaliam qualidade de raciocínio sobre evidência fornecida.
2. `evals/fixtures/`: verificam propriedades concretas de frameworks/runtimes em cenários controlados.
3. comparação A/B entre agentes: mede se usar a skill melhora a resposta; as fixtures, sozinhas, não provam isso.

Fixtures atuais:

- `libgdx/`: lifecycle de assets e input usando classes reais do LibGDX em revisão fixa.
- `java-spring/`: fronteira HTTP, transações JPA e proxy transacional usando Spring Boot + H2.
