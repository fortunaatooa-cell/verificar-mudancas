# Maturidade do verificar-mudancas

A maturidade é baseada em prova independente por dimensão, não em quantidade de agentes ou testes.

## Dimensões

- **D1 Eficácia:** A/B cego, tratamento observado, efeito mínimo congelado, sem regressão de segurança.
- **D2 Descobribilidade:** experimento `skill_installed_unprompted` separado, com leitura espontânea medida.
- **D3 Correção do gabarito:** fixture executável ou fonte por item + revisão independente.
- **D4 Adequação ao banco:** scanner de dados públicos, aprovação humana explícita e piloto bloqueado até as seis respostas/revisão de segurança.
- **D5 Sustentabilidade:** orçamento do núcleo, regra caso-antes-de-regra, CI/testes/fixtures e revisão humana de feature grande.

## Estado desta branch

`feature/agentic-v1-5` permanece **experimental, not evaluated**. Smoke tests, testes unitários e CI verde provam consistência interna, não D1.

O código implementa os mecanismos necessários para T1–T7, T10–T12 e T14. T8 (24 execuções reais), T9 (decisão após o resultado) e T13 (piloto mínimo de duas semanas) dependem de evidência externa/tempo real e não podem ser fabricados pelo repositório.

## Gates

A rodada real é bloqueada se:
- a revisão humana independente do oracle não corresponder aos hashes atuais;
- a versão/configuração mudar no resume;
- o tratamento estiver instalado mas não for observado, caso em que a execução é excluída e contada.

O piloto regulado é bloqueado por `scripts/check_pilot_readiness.py` até as seis respostas e a aprovação de segurança estarem registradas.
