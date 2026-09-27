# CI/CD e release

Usar quando a mudança afetar build, pipeline, artifact, empacotamento, promoção de ambiente ou deploy.

## Rastrear o que realmente foi entregue
- Identificar trigger, branch/commit, pipeline, artifact gerado, ambiente destino e mecanismo de promoção. Não assumir que o código testado localmente é o mesmo artifact implantado.
- Separar falha de código de falha de runner, credencial, cache, rede, registry, ferramenta ou ambiente. Uma pipeline vermelha antes das mudanças atuais não prova regressão do produto.
- Verificar lockfiles, versões de runtime e etapas condicionais para evitar diferenças silenciosas entre local e CI.

## Verificar release
- Para mudança de risco, definir estratégia de rollout e recuperação conforme o projeto: rolling, blue/green, canary, feature flag, rollback ou rollforward.
- Confirmar que gates relevantes usam o artifact/commit esperado e que smoke checks exercitam a fronteira alterada.
- Não tratar deploy concluído como prova de comportamento correto; observar health, erros e sinais definidos para aceite.

## Entrega específica
Registrar commit/artifact, verificações executadas, ambiente, estratégia de rollout e qualquer diferença entre o que foi testado e o que foi implantado.
