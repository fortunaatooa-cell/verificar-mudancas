<!-- Gerado de .agents/rules/tdd-cycle.md; mantenha o arquivo portátil como fonte de verdade. -->

# TDD

TDD verdadeiro segue `RED → GREEN → REFACTOR → REGRESSION`.

- RED: teste/prova falha pelo requisito ausente ou defeito correto.
- GREEN: menor mudança pertinente faz a prova passar.
- REFACTOR: melhorar estrutura sem alterar comportamento protegido.
- REGRESSION: reexecutar a fronteira e cenários adjacentes após a última edição.

Teste escrito depois da implementação pode ser excelente regressão, mas não deve ser descrito como evidência de RED anterior.
