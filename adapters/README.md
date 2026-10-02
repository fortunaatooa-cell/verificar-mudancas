# Adapters

Manifests por superfície para declarar capacidades sem acoplar o núcleo ao produto. `runtime-detect` significa “verificar na sessão”, não “assumir disponível”.

Além de repositório, shell, web, subagentes, hooks, memória e ferramentas externas, os adapters distinguem `vision_input` (inspecionar conteúdo visual real) de `visual_generation` (renderizar/criar saída visual). Mesmo sem `visual_generation`, o sistema pode produzir fonte textual editável como Mermaid/SVG quando a superfície permitir texto/arquivos.

## Claude Code

O adapter Claude possui uma camada nativa gerada para `CLAUDE.md`, Skills, subagents, rules e hooks. Ela espelha os arquivos portáteis; não cria uma segunda metodologia. Recursos recentes como workflows dinâmicos, plugins, sincronização de conta e mods ficam em runtime-detect/opt-in e não são presumidos disponíveis.
