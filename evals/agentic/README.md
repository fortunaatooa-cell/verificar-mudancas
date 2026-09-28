# Evals agentic

Casos comportamentais para a arquitetura completa. O agente recebe apenas prompt/evidence; o oracle é reservado à avaliação.

Cobertura mínima: bug Java, memória/runtime, segurança, investigação sem edição, HIGH risk, memória como pista, sanitização no aprendizado, quality gate sem falso PASS e degradação sem subagentes/hooks.

Esses casos protegem decisões de orquestração. Unit tests em `tests/` protegem os runners executáveis.
