# /revisar

Revisar uma mudança existente (diff, branch, PR ou conjunto de arquivos) sem assumir que a implementação está correta.

## Saída

- findings priorizados por impacto;
- regressões e incompatibilidades potenciais;
- testes ausentes ou frágeis;
- contraexemplos;
- riscos de segurança/runtime quando aplicáveis;
- lacunas de verificação;
- decisão técnica: `APROVAR`, `AJUSTAR` ou `BLOQUEAR`.

O foco é a mudança observada. Não inventar contexto de negócio ausente; marcar incerteza quando ela altera a avaliação.