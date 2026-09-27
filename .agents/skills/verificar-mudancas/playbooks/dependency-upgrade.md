# Playbook: upgrade de dependência

Usar quando biblioteca, runtime, framework, provider, plugin ou imagem for atualizado.

1. Identificar versão atual/alvo, motivo, constraints e dependências transitivas.
2. Ler mudanças relevantes e requisitos de runtime/configuração.
3. Atualizar lockfiles e configuração pelos mecanismos normais do projeto.
4. Rodar build, testes e integração nas fronteiras que dependem da mudança.
5. Verificar startup/empacotamento e comportamento distribuído quando aplicável.
6. Revisar mudanças transitivas, segurança e compatibilidade.
7. Registrar riscos e rollback/downgrade quando a atualização atingir produção.

Não atualizar pacote apenas por ser "mais novo" sem verificar efeito no projeto.
