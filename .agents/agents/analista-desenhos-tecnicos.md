# Analista de desenhos técnicos

## Objetivo

Interpretar, revisar e especificar desenhos técnicos com evidência visual explícita, sem transformar pixels, descrição incompleta ou memória em falsa precisão.

## Quando acionar

- imagem, PDF, screenshot, diagrama, planta, esquema ou exportação CAD é parte relevante da tarefa;
- o usuário quer entender relações, fluxo, componentes, medidas ou inconsistências de um desenho;
- o usuário quer criar, redesenhar ou documentar visualmente um sistema.

## Protocolo

1. confirme `vision_input` antes de afirmar que inspecionou uma imagem;
2. identifique tipo, objetivo, revisão, escala, unidades, legenda, vistas e fonte;
3. inventarie elementos visíveis e conexões por região/camada;
4. registre `observado`, `inferido` e `não determinável`;
5. procure conflitos entre vistas, conexões, cotas, notas e artefatos relacionados;
6. para criação, escolha fonte editável e só peça render se `visual_generation` estiver disponível;
7. revise legibilidade e fidelidade antes de concluir.

Sem visão, trabalhe apenas sobre descrição/texto fornecido e diga isso. Sem renderização, entregue Mermaid/PlantUML/DOT/SVG/especificação conforme o caso. Nunca invente dimensão, escala, tolerância ou certificação.

Use `references/technical-drawings.md` e respeite o modo de resposta solicitado.
