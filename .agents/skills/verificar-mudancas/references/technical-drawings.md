# Desenhos técnicos e evidência visual

Use esta referência quando a entrada ou a saída principal for um desenho, diagrama, planta, esquema, captura de tela técnica, PDF com figura, exportação CAD ou representação visual de arquitetura/sistema.

## Analisar

1. Identifique o tipo e a finalidade do artefato: arquitetura de software, fluxo, sequência, rede/infra, dados, layout, mecânico, elétrico, civil, P&ID ou outro.
2. Procure título, revisão, escala, unidades, legenda, vistas, cortes, símbolos, notas e fonte do desenho. Ausência desses itens é uma limitação, não licença para inferi-los.
3. Faça inventário do que está **visível**: componentes, identificadores, conexões, direção de fluxo, interfaces, dimensões, tolerâncias, materiais, estados e anotações.
4. Reconstrua relações e caminho funcional. Compare elementos duplicados, desconectados, conflitantes, sem legenda ou inconsistentes entre vistas.
5. Separe a saída em **observado**, **inferido** e **não determinável**. Texto ilegível, escala desconhecida ou parte cortada devem permanecer como incerteza.
6. Quando houver código, especificação, BOM, contrato, configuração ou outro artefato, faça cross-check; o desenho sozinho não prova que a implementação real corresponde a ele.

Para imagens complexas, raciocine por regiões/camadas em vez de tentar resumir tudo de uma vez. Em desenho multivista, preserve a correspondência entre vistas antes de concluir geometria ou conexão.

## Criar ou redesenhar

Comece pela intenção: público, nível de detalhe, padrão/notação, dimensões conhecidas, interfaces obrigatórias e formato de entrega.

Escolha a representação mais verificável disponível:

- arquitetura/fluxo/sequência: Mermaid, PlantUML, Graphviz/DOT ou formato equivalente;
- desenho vetorial geral: SVG quando adequado;
- geometria/CAD: script, DXF/SVG ou ferramenta CAD somente quando houver primitivas, unidades e dimensões suficientes;
- imagem raster/gerativa: útil para comunicação visual, mas trate como **ilustrativa** quando não houver garantia geométrica.

Sempre que possível entregue também a fonte editável do desenho. Se a ferramenta não puder renderizar/criar imagem, produza a especificação ou código do diagrama e diga claramente o que falta para renderizar.

Nunca invente cota, escala, tolerância, material, norma, capacidade, carga ou distância. Quando o usuário pedir um desenho sem dados suficientes, use valores simbólicos ou marque `TBD` em vez de criar falsa precisão.

## Revisar

Verifique, conforme aplicável:

- legibilidade, nomenclatura e legenda;
- consistência de unidades, escala, setas e direções;
- conectividade e interfaces;
- correspondência entre vistas/camadas;
- dimensões e tolerâncias contra a fonte fornecida;
- elementos órfãos, colisões, ambiguidades e informações conflitantes;
- versão/revisão e compatibilidade com o sistema real.

Em contextos mecânicos, elétricos, civis, industriais, segurança ou outros domínios críticos, a análise da skill é apoio técnico e não substitui validação por profissional habilitado nem certificação normativa.
