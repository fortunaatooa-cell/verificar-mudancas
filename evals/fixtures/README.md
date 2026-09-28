# Fixtures executáveis

As fixtures complementam `cases.json` e `oracle.json` com comportamento reproduzível.

Há três níveis de evidência distintos:

1. `cases.json` + `oracle.json`: avaliam qualidade de raciocínio sobre evidência fornecida.
2. `evals/fixtures/`: verificam propriedades concretas de frameworks/runtimes em cenários controlados.
3. comparação A/B entre agentes: mede se usar a skill melhora a resposta; as fixtures, sozinhas, não provam isso.

Fixtures atuais:

- `libgdx/`: lifecycle de assets e input usando classes reais do LibGDX em revisão fixa.
- `java-spring/`: fronteira HTTP, serialização/validação, transações, N+1, optimistic locking e concorrência usando Spring Boot + H2.
- `terraform-replacement/`: diferencia update e replacement por plano JSON usando Terraform pinado e state local descartável.
- `python-runtime/`: reproduz `read_parquet` sem engine, depois prova recuperação com PyArrow pinado e verifica fronteira de timezone.
