# Comandos canônicos em português

Esta pasta define a interface portátil do sistema. O prefixo `/` representa a intenção do comando; cada adapter pode traduzi-lo para o mecanismo real da ferramenta.

- `/verificar` — fluxo completo de mudança.
- `/investigar` — somente investigação, sem edição.
- `/corrigir` — corrigir problema já investigado ou conduzir investigação + correção.
- `/revisar` — revisar diff/PR/mudança existente.
- `/validar` — validar alegações e estado final.
- `/portao-qualidade` — executar quality gate proporcional ao risco.
- `/aprender` — propor aprendizado reutilizável; não promove automaticamente para o núcleo.

Quando a plataforma não suportar comandos ou subagentes, executar as mesmas etapas sequencialmente no agente atual.