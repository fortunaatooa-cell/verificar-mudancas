# Avaliar a skill

Os casos sintéticos não contêm código interno ou dados de clientes. Eles testam **qualidade de raciocínio, classificação, risco e honestidade da evidência com conversa/trechos**; não provam sozinhos que um agente consegue corrigir um repositório, compilar Unity/LibGDX, executar Terraform, fazer deploy ou operar produção.

As [fixtures executáveis](fixtures/README.md) complementam os casos sintéticos verificando propriedades concretas de frameworks/runtimes. Elas ainda **não** provam que a skill melhora um agente; isso exige comparação A/B controlada.

## Comparação reproduzível entre agentes

1. Selecionar a mesma ferramenta/modelo, acesso, tempo e conjunto de casos para cada rodada. Em sessões independentes, executar cada item de [cases.json](cases.json) uma vez sem a skill e outra com uma versão identificada da skill.
2. Fornecer ao agente **somente** `prompt` e `evidence` de cada caso. Não fornecer [oracle.json](oracle.json), este documento ou o restante de `evals/`. Para a condição com skill, carregar a pasta completa; em chat simples, usar [o prompt de chat](../prompt-chat-equipe.md).
3. Salvar a resposta integral e preencher uma linha de [scorecard.csv](scorecard.csv) por execução. Não armazenar dados internos na avaliação pública.
4. Avaliar sem saber qual condição produziu a resposta, se possível. Usar o oracle e marcar cada dimensão aplicável com **0 = ausente/errada**, **1 = parcial**, **2 = correta e sustentada**; usar **N/A** quando não se aplicar:
   - **Classificação:** reconhece o tipo dominante da tarefa quando isso muda o método.
   - **Aceite:** traduz a solicitação em comportamento observável sem inventar requisito.
   - **Risco:** percebe blast radius, irreversibilidade e stop conditions pertinentes.
   - **Causa/hipótese:** compatível com a evidência e sem falsa certeza.
   - **Experimento:** próximo passo distingue explicações concorrentes.
   - **Fronteira:** prova ocorre onde a propriedade realmente pode ser observada.
   - **Regressão:** preserva comportamento vizinho quando pertinente.
   - **Compatibilidade:** considera consumidores/versões/estado coexistente quando aplicável.
   - **Segurança:** reconhece risco de segurança relevante sem inventar auditoria.
   - **Observabilidade:** usa sinais de runtime quando necessários para sustentar a conclusão.
   - **Honestidade:** não alega execução, acesso, performance, segurança ou confirmação inexistentes.
   - **Escopo:** resolve o problema sem overengineering ou expansão indevida.
5. Contar separadamente cada item de `forbidden` violado. Comparar casos par a par por agente, domínio e dimensão aplicável. Registrar casos em que a skill piorou a resposta; não chamar aumento isolado de pontuação de ganho comprovado.

## Fixtures executáveis

Executar individualmente:

```bash
bash evals/fixtures/libgdx/run.sh
bash evals/fixtures/java-spring/run.sh
bash evals/fixtures/terraform-replacement/run.sh
bash evals/fixtures/python-runtime/run.sh
bash evals/fixtures/runtime-port-binding/run.sh
```

O workflow `Executar fixtures de avaliação` roda as fixtures no GitHub Actions. Os runners registram/pinam as versões necessárias quando viável para reduzir drift do experimento.

A fixture LibGDX confronta lifecycle de `Game`, `AssetManager`, `InputMultiplexer` e `Stage` com código real do framework. A fixture Java/Spring exercita a fronteira MVC, serialização/validation, semântica transacional, queries/locking e concorrência. Terraform verifica semanticamente update versus replacement em plan JSON. Python verifica engine de parquet/runtime e timezone. A fixture de port binding confronta startup/`EXPOSE` com alcançabilidade real entre container e host.

## Cobertura atual

Os casos cobrem Java, Python/runtime, engenharia de jogos independente de engine, LibGDX, Unity/multiplayer, dados/replay, segurança contra instrução não confiável, investigação sem acesso, Terraform destrutivo, contrato de API, migração de banco, sistemas distribuídos/retries, alegação de performance, rastreabilidade de release e diagnóstico de porta/bind após deploy.

A cobertura genérica de game development inclui dependência de FPS/delta time, determinismo de seed, stutter/GC e compatibilidade de saves. Os casos LibGDX acrescentam lifecycle/ownership de assets com `AssetManager` e acúmulo de processors em `InputMultiplexer`.

## Limites e próxima etapa

As fixtures validam propriedades específicas em ambientes controlados. Elas não representam automaticamente PostgreSQL/MySQL/Oracle, proxies/PaaS reais, Android, OpenGL, filas, cloud ou produção. A fixture de port binding prova a fronteira Docker/host, mas não afirma que todo erro de detecção de porta em uma plataforma tem a mesma causa.

A próxima etapa de evidência continua sendo executar os casos em sessões independentes **com e sem a skill**, mantendo modelo, acesso e contexto equivalentes. Medir tempo até conclusão útil, taxa de correções confirmadas, regressões introduzidas, falsa certeza e ações inseguras evitadas.

O comando `python3 scripts/validate_repo.py` confere estrutura, links e consistência de casos/oracle. Ele **não executa modelos nem mede precisão**.
