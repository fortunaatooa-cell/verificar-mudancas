# Frontend, UI e E2E

Usar quando a mudança afetar interface, estado no cliente, navegação, browser, acessibilidade ou fluxo visual do usuário.

## Investigar a fronteira visível
- Seguir ação do usuário → estado local → chamada de rede → resposta → renderização. Separar bug de UI de contrato backend, cache, race ou estado obsoleto.
- Considerar loading, vazio, erro, retry, navegação, responsividade, foco/teclado e acessibilidade quando fizerem parte do fluxo afetado.
- Não assumir que teste de função ou componente isolado prova comportamento real no browser.

## Provar
- Usar teste unitário/componente para lógica isolada e E2E/browser para fluxo que depende de integração, routing, storage, layout ou rede.
- Verificar ao menos o caminho corrigido e um caminho vizinho preservado. Para regressão visual, comparar estados determinísticos e não depender apenas de screenshot manual quando houver ferramenta do projeto.
- Quando browser/platform específica estiver implicada, registrar versão/target testado.

## Entrega específica
Relatar fluxo do usuário, estados testados, browser/target quando relevante e diferenças entre comportamento de componente e comportamento E2E.
