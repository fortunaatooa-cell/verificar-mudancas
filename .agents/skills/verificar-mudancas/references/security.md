# Segurança de software

Usar esta referência quando a mudança tocar autenticação, autorização, entrada não confiável, segredos, dados sensíveis, permissões, criptografia, dependências vulneráveis ou superfícies expostas. Aplicar somente os tópicos pertinentes ao risco da tarefa; não transformar toda mudança em auditoria completa.

## Perguntas essenciais

- Separar autenticação de autorização: confirmar quem é o usuário e também se ele pode executar a ação sobre aquele recurso. Procurar IDOR/BOLA, escalonamento de privilégio e trust relationships excessivas quando houver controle de acesso.
- Identificar entradas controláveis por usuário ou sistema externo e verificar validação, canonicalização e encoding na fronteira adequada. Considerar SQL/NoSQL injection, command injection, path traversal, SSRF, XSS, desserialização insegura e upload de arquivos quando aplicáveis.
- Verificar se logs, erros, traces, métricas, fixtures ou mensagens de teste podem expor credenciais, tokens, PII ou segredos. Não copiar segredos para exemplos, issues, commits ou relatórios públicos.
- Em mudanças de IAM, roles, scopes ou políticas, avaliar princípio do menor privilégio, curingas, recursos abrangidos e caminhos indiretos de privilégio.

## Provar sem criar risco

- Preferir testes negativos além do fluxo autorizado: usuário sem permissão, recurso de outro tenant, entrada malformada e operação proibida quando relevantes.
- Não recomendar desabilitar controles de segurança apenas para fazer o teste passar. Se um mecanismo bloquear o diagnóstico, explicar o impedimento e escolher ambiente ou fixture segura.
- Se a correção depender de biblioteca ou versão, verificar compatibilidade e advisories relevantes antes de atualizar; não assumir que "mais nova" significa automaticamente segura para o projeto.

## Entrega específica

Relatar somente riscos sustentados pela evidência. Distinguir vulnerabilidade confirmada, possibilidade plausível e área não verificada. Para achados de alto impacto, indicar superfície afetada, pré-condição, impacto, teste de regressão e mitigação/rollback sem divulgar material sensível.
