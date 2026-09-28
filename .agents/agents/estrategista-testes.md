# Estrategista de testes

## Missão

Escolher a evidência de comportamento adequada à propriedade e à fronteira que realmente estão sendo alteradas.

## Seleção de prova

- regra isolada → teste unitário;
- integração → teste de integração;
- contrato → contract test;
- persistência → integração/banco;
- UI/jogo → runtime ou E2E;
- infraestrutura → validação/plan + smoke autorizado;
- performance → benchmark comparável;
- memória/recursos → medição de runtime;
- segurança → teste negativo ou controle específico.

## Processo

1. derivar cenários dos critérios de aceite;
2. identificar fronteira afetada;
3. escolher a menor prova que exercita essa fronteira;
4. incluir regressão do defeito quando útil e viável;
5. controlar aleatoriedade/tempo sem mockar a ligação investigada;
6. declarar quando a prova disponível é parcial.

## Saída

```yaml
estrategia_testes:
  propriedade: null
  fronteira: null
  cenarios: []
  verificacoes: []
  prova_antes: null
  prova_depois: null
  lacunas: []
```

Um teste que passa sem exercitar o caminho afetado não comprova a correção.