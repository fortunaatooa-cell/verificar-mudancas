# Agentes especializados

Os arquivos desta pasta definem papéis canônicos da arquitetura agentic da `verificar-mudancas`. Eles não pressupõem suporte nativo a subagentes: um adapter pode executá-los como agentes independentes ou como etapas sequenciais no mesmo agente.

## Contrato comum

Todo agente deve:

- receber somente o contexto necessário;
- separar `FATO`, `HIPOTESE`, `INFERENCIA` e `DESCONHECIDO` quando isso afetar a conclusão;
- não alegar execução ou acesso inexistente;
- preservar alterações preexistentes;
- devolver resultado estruturado e lacunas de evidência;
- respeitar stop conditions e políticas do ambiente.

## Agentes v1.5

1. `investigador.md` — causa e experimentos discriminantes.
2. `diagnosticador-runtime.md` — memória, JVM, container, Lambda, rede e runtime.
3. `estrategista-testes.md` — prova correta para a fronteira afetada.
4. `implementador.md` — menor mudança correta.
5. `revisor-codigo.md` — revisão adversarial e contraexemplos.
6. `revisor-seguranca.md` — revisão condicional de segurança.
7. `verificador-evidencias.md` — validação das alegações finais.

O orquestrador deve selecionar apenas os agentes pertinentes ao problema.