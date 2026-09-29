# Adapters

Manifests por superfície para declarar capacidades sem acoplar o núcleo ao produto. `runtime-detect` significa “verificar na sessão”, não “assumir disponível”.

Além de repositório, shell, web, subagentes, hooks, memória e ferramentas externas, os adapters distinguem `vision_input` (inspecionar conteúdo visual real) de `visual_generation` (renderizar/criar saída visual). Mesmo sem `visual_generation`, o sistema pode produzir fonte textual editável como Mermaid/SVG quando a superfície permitir texto/arquivos.
