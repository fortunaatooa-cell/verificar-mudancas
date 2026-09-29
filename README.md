# Verificar Mudanças — Pacote Microsoft 365 Copilot

Versão: **Copilot 365 / v3.1 Engineering Lifecycle**  
Fonte metodológica: `feature/agentic-v1-5`  
Commit-base: `6a2c3d8a682a4debb27cba80a346dc9d2fa80268`

Esta branch existe **somente para distribuição do pacote otimizado para Microsoft 365 Copilot Agent Builder**. Ela não substitui a `main` nem a branch agentic.

## Como baixar

Use o botão **Code → Download ZIP** nesta branch ou o link de download direto da branch.

## Como instalar

1. Baixe e descompacte o ZIP da branch.
2. Copie todo o conteúdo de `INSTRUCOES_PARA_COLAR_NO_AGENTE.txt` para o campo **Instruções** do agente.
3. Em **Conhecimento**, envie somente os 14 arquivos `.txt` dentro de `CONHECIMENTO/`.
4. Não envie o próprio ZIP como fonte de conhecimento.
5. Use `TESTES-DE-ACEITE.txt` para validar o comportamento.

## Limites considerados

- Instruções: abaixo de 8.000 caracteres.
- Conhecimento: 14 arquivos, abaixo do limite de 20 uploads diretos considerado neste pacote.
- O pacote não presume shell, Git, hooks, subagentes reais, deploy ou execução local.

## Estrutura

- `INSTRUCOES_PARA_COLAR_NO_AGENTE.txt` — prompt principal do agente.
- `CONHECIMENTO/` — 14 arquivos de conhecimento numerados e roteados.
- `TESTES-DE-ACEITE.txt` — cenários para validar o agente.
- `MANIFEST.json` — metadados do pacote.
