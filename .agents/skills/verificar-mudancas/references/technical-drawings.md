# Desenhos técnicos e evidência visual

Use esta referência quando a entrada ou a saída principal for um desenho, diagrama, planta, esquema, captura de tela técnica, PDF com figura, exportação CAD ou representação visual de arquitetura/sistema.

## Analisar

1. Identifique tipo e finalidade: arquitetura de software, fluxo, sequência, rede/infra, dados, layout, mecânico, elétrico, civil, P&ID ou outro.
2. Procure título, revisão, escala, unidades, legenda, vistas, cortes, símbolos, notas e fonte. Ausência é limitação, não licença para inferir.
3. Inventarie o que está **visível**: componentes, IDs, conexões, direção de fluxo, interfaces, dimensões, tolerâncias, materiais, estados e anotações.
4. Reconstrua relações e caminho funcional. Procure elementos duplicados, desconectados, conflitantes, sem legenda ou inconsistentes entre vistas.
5. Separe **observado**, **inferido** e **não determinável**. Texto ilegível, escala desconhecida ou área cortada permanecem como incerteza.
6. Faça cross-check com código, especificação, BOM, contrato ou configuração quando disponíveis; o desenho sozinho não prova o sistema real.

Em imagens complexas, raciocine por regiões/camadas. Em multivista, preserve a correspondência entre vistas antes de concluir geometria ou conexão.

## Criar ou redesenhar

Defina intenção, público, nível de detalhe, notação, dimensões conhecidas, interfaces obrigatórias e formato de entrega. Prefira a representação mais verificável disponível:

- arquitetura/fluxo/sequência: Mermaid, PlantUML ou Graphviz/DOT;
- vetorial geral: SVG;
- geometria/CAD: script, DXF/SVG ou ferramenta CAD apenas com primitivas, unidades e dimensões suficientes;
- imagem raster/gerativa: comunicação visual **ilustrativa** quando não houver garantia geométrica.

Entregue fonte editável quando possível. Sem capacidade de renderização, produza especificação/código do diagrama e declare que não houve render. Nunca invente cota, escala, tolerância, material, norma, capacidade, carga ou distância; use valor simbólico ou `TBD`.

## Revisar

Verifique legibilidade, nomenclatura, legenda, unidades, escala, setas, conectividade, interfaces, correspondência entre vistas/camadas, dimensões contra a fonte, elementos órfãos, colisões, ambiguidades, revisão e compatibilidade com o sistema real.

Em domínios mecânicos, elétricos, civis, industriais ou de segurança, a análise é apoio técnico e não substitui validação por profissional habilitado nem certificação normativa.
