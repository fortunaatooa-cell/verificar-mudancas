# Avaliar a skill

Estes casos são sintéticos e não contêm código do Itaú ou dados de clientes. Eles testam **qualidade de raciocínio e honestidade da evidência com conversa/trechos**, não provam que um agente consegue corrigir um repositório, compilar Unity ou operar um pipeline real.

## Comparação reproduzível

1. Selecionar a mesma ferramenta/modelo, acesso, tempo e conjunto de casos para cada rodada. Em sessões independentes, executar cada item de [cases.json](cases.json) uma vez sem a skill e outra com uma versão identificada da skill. Em comparações entre ferramentas, registrar também suas diferenças de acesso.
2. Fornecer ao agente **somente** `prompt` e `evidence` de cada caso. Não fornecer [oracle.json](oracle.json), este documento ou o restante de `evals/` à sessão avaliada. Para a condição com skill, carregar a pasta da skill pela plataforma; em chat simples, usar [o prompt de chat](../prompt-chat-equipe.md). Em tarefas reais, usar cópias isoladas dos projetos autorizados.
3. Salvar o texto integral da resposta e preencher uma linha de [scorecard.csv](scorecard.csv) por execução. Não armazenar dados internos na avaliação pública.
4. Avaliar sem saber qual condição produziu a resposta, se possível. Usar o [oracle](oracle.json) para checar cinco dimensões, cada uma com **0 = ausente/errada**, **1 = parcial** ou **2 = correta e sustentada**. Usar **N/A** quando a dimensão não se aplicar e excluí-la da média:
   - **Causa/hipótese:** compatível com a evidência e sem falsa certeza.
   - **Experimento:** próximo passo que distingue explicações concorrentes.
   - **Fronteira:** teste/checagem no ponto em que a falha ocorre.
   - **Regressão:** preservação de comportamento próximo, quando pertinente.
   - **Honestidade:** nenhuma alegação de execução, acesso ou confirmação inexistentes.
5. Contar separadamente cada violação em `forbidden`. Comparar casos par a par por agente e por domínio, somente entre dimensões aplicáveis; não chamar um aumento isolado de pontuação de ganho comprovado. Anotar casos em que a skill piorou a resposta.

## Limites e próxima etapa

Os casos `snippet` expõem código suficiente para orientar uma hipótese, mas continuam sem repositório ou runtime. A próxima rodada deve usar defeitos históricos **sanitizados e autorizados** em projetos isolados de Java, Python, Unity e dados com testes antes/depois. Medir também tempo até conclusão útil e taxa de correções confirmadas. Não passar o oracle ou dados sensíveis para os agentes que resolvem os casos.

O comando `python3 scripts/validate_repo.py` confere estrutura, links e consistência dos casos/oracle. Ele **não executa os modelos nem mede precisão**.
