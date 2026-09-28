# Evidência de mudança

Usar quando a saída precisar alimentar revisão, PR, change record, auditoria técnica ou handoff. Este é um **template genérico**; campos específicos de uma organização devem ficar no repositório autorizado daquela organização e podem adaptar nomes/identificadores sem serem publicados aqui.

```markdown
# Evidência de mudança

**Tipo e risco:** bug | feature | refatoração | migração | incidente | dados | infraestrutura · LOW | MEDIUM | HIGH | CRITICAL
**Sintoma ou objetivo, e impacto:**
**Critérios de aceite:**
**Causa confirmada ou hipótese provável, com a evidência:**
**O que mudou (arquivos e comportamento):**
**Provas executadas:** comando · resultado · ambiente
**Regressões e compatibilidade verificadas:**
**Plano de rollout e de rollback/rollforward:**
**Sinal de sucesso e sinal de rollback:**
**Não verificado, e por quê:**
**Dados sensíveis:** nenhum dado de cliente ou segredo usado/exposto? sim | não | não verificável
**Aprovação humana necessária:** papel/responsável, se aplicável
**Registro de mudança:** identificador do processo local, se aplicável e autorizado
```

## Regras

- Campo sem evidência recebe `não verificado`; nunca preencher por suposição.
- Em provas, registrar comando/ação e resultado reais. `Testes passaram` sem prova identificável não conta.
- Não copiar segredo, PII, payload real, ARN/account ID, URL privada ou nome interno para um pacote público.
- HIGH/CRITICAL sempre deixa explícita a aprovação humana necessária e os sinais de rollback/rollforward.
- O template descreve evidência; ele não concede aprovação, acesso, segregação de funções nem autorização para produção.
