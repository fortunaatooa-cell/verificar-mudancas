---
name: verificar-mudancas
description: Investiga bugs e conduz mudanças de engenharia de software ou dados com evidência de causa, testes, implementação, revisão crítica e verificação final. Use quando alguém apontar uma falha, pedir análise de testes, correção, funcionalidade, refatoração ou mudança em pipeline, em frontend, backend ou dados. Funciona com ou sem acesso direto ao repositório; não requer ECC instalado.
---

# Verificar mudanças

Seguir um ciclo inspirado no Everything Claude Code (ECC): entender → planejar → testar → implementar → revisar → verificar → registrar aprendizado. Usar os recursos do agente atual; invocar skills especializadas somente quando disponíveis e relevantes. Priorizar a solicitação, as instruções do repositório e as políticas do ambiente.

## Modos de acesso

- **Com repositório e ferramentas:** ler código e executar os passos abaixo até uma mudança verificada. Descobrir stack e comandos no projeto; não presumir Java, Python ou ferramenta de teste.
- **Somente conversa, prints ou logs:** pedir o mínimo de contexto permitido para discriminar hipóteses: comportamento esperado/observado, mensagem de erro, momento, mudanças recentes e trecho relevante sem dados sensíveis. Propor verificações concretas que a equipe possa executar. Não afirmar que leu código, rodou testes, encontrou causa definitiva ou corrigiu algo sem evidência. Se receber novas saídas, atualizar hipóteses e continuar.
- Respeitar limites da ferramenta: anexar `SKILL.md` ou colar seu texto em um chat não dá acesso automático ao repositório, terminal, histórico ou ferramentas externas.

## 1. Diagnosticar

- Ler instruções do projeto, documentação, código, testes e configuração relacionados. Verificar `git status --short`; preservar alterações existentes.
- Definir o comportamento esperado e o observado, a fronteira da mudança e os contratos afetados. Para um bug apontado pelo usuário, rastrear o caminho de entrada até o efeito, formular hipótese de causa raiz e tentar reproduzi-la. Se a reprodução depender de ambiente indisponível, reunir logs, testes ou outra evidência e explicitar a incerteza.
- Identificar comandos reais de teste, build e lint; não pressupor ferramenta pela linguagem.
- Separar sintomas, evidências e hipótese. Antes de alterar código, explicar como a hipótese produz o sintoma observado; conferir ao menos uma hipótese alternativa plausível quando o diagnóstico for ambíguo. Não apresentar correlação como causa comprovada.
- Priorizar hipóteses pelo poder explicativo e pelo custo de verificação. Identificar o primeiro ponto em que o resultado diverge do esperado; evitar alterar vários componentes ao mesmo tempo. Para falhas intermitentes, considerar tempo, concorrência, configuração, dados e dependências externas.

## 2. Planejar conforme o risco

- Para mudança ampla, arquitetura, migração ou efeito em dados, formular plano breve com arquivos prováveis, compatibilidade, riscos e critérios de aceite. Para correção simples, agir diretamente.
- Não parar após o plano quando a tarefa pedir implementação. Resolver decisões rotineiras pelos padrões do repositório.
- Para dados, definir esquema, granularidade, chaves, nulos, duplicatas, idempotência e reconciliação antes de transformar. Para infraestrutura, examinar plano, custo, acesso e reversão antes de aplicar.

## 3. Criar prova de comportamento

- Em bug ou funcionalidade, escrever primeiro um teste que falhe pelo motivo esperado quando for viável e útil. Confirmar que o teste falha antes da correção, passa depois e cobre também um cenário vizinho que não deve regredir. Em refatoração, proteger comportamento existente.
- Escolher o nível de teste adequado: unitário para regra isolada, integração para fronteiras reais, ponta a ponta para um fluxo crítico. Mockar dependências externas nos testes que precisam ser determinísticos.
- Montar uma pequena matriz de cenários antes de declarar a correção concluída: caso que falhava, caminho normal preservado, limite ou erro próximo e contrato com sistema externo quando envolvido. Selecionar só cenários relevantes ao defeito.
- Não exigir porcentagem arbitrária de cobertura nem criar testes que só repetem a implementação.
- Se não for possível reproduzir ou testar a causa, registrar a lacuna e escolher uma verificação substituta explícita; não inventar uma reprodução.

## 4. Implementar e revisar

- Fazer a menor mudança que satisfaça os critérios de aceite. Seguir estilo local, validar entrada, tratar erros e preservar contratos salvo instrução contrária.
- Examinar diff e arquivos novos como revisor independente: defeitos, regressões, segurança, legibilidade, compatibilidade, desempenho e escopo. Usar ferramentas de revisão disponíveis, mas verificar cada achado antes de mudar código.
- Corrigir achados concretos; não introduzir refatorações especulativas.
- Confirmar que a mudança elimina a causa identificada, e não apenas mascara o sintoma. Se o teste passar sem exercer o caminho defeituoso, corrigir o teste.

## 5. Verificar novamente e entregar

- Executar verificações relevantes após a última alteração: testes afetados e, conforme o caso, build, lint, análise estática, validação de dados, reconciliação ou smoke test. Uma validação anterior à revisão não comprova o estado final.
- Escolher verificação de acordo com a fronteira: frontend → fluxo no navegador, estados de erro e inspeção visual quando houver UI; backend → contrato, integração e falhas de dependência; dados → esquema, contagens, duplicatas, idempotência e reconciliação; infraestrutura → plano/diff, permissões e smoke test autorizado. Não declarar uma fronteira verificada se só testes internos passaram.
- Conferir `git diff --check`, diff completo incluindo arquivos novos e `git status --short`.
- Registrar em documentação ou instruções do projeto decisões e procedimentos realmente reutilizáveis; evitar duplicação de notas temporárias.
- Informar mudança, evidência de testes com comandos e resultados, riscos remanescentes e o que não pôde ser verificado. Nunca relatar build, cobertura ou segurança como aprovados sem medição.
- Para bugs, concluir com uma cadeia curta de evidência: sintoma observado → causa sustentada → teste antes/depois → correção → regressões verificadas. Distinguir causa confirmada de hipótese ainda provável.
- Se a tarefa for análise apenas, entregar diagnóstico e próximo experimento discriminante sem editar. Se for correção, implementar até o estado verificável, informando bloqueios reais.

## Aprendizado para o time

- Após um incidente resolvido, sugerir registrar uma nota curta no local aprovado pelo time: sintoma, causa confirmada, sinal de diagnóstico, teste que previne regressão e decisão tomada. Não guardar logs com dados sensíveis nem fatos não confirmados.
- Converter padrões recorrentes em testes, documentação ou uma skill especializada somente após revisão do time. Esta skill não observa conversas nem aprende automaticamente entre ferramentas, projetos ou pessoas; memória e distribuição dependem de mecanismos e permissões próprios de cada ambiente.

## Limites

- Não vazar segredos, dados de clientes nem código interno a serviços não autorizados. Seguir regras corporativas para IA, plugins e conectores.
- Não descartar trabalho de outra pessoa. Não executar commit, push, PR, publicação, deploy ou alteração externa sem que a tarefa e o ambiente autorizem.
- Quando faltar uma ferramenta, permissão ou acesso, executar as verificações locais disponíveis e relatar exatamente a limitação.
