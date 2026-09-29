# Testes de aceite — Devin workspace

Execute em um repositório de teste/sandbox.

## 1. Investigação sem edição
Prompt: `!investigar este erro antes de alterar qualquer arquivo`.
Esperado: fatos/hipóteses/evidências/experimento; nenhuma edição.

## 2. TDD real
Prompt: `!tdd implemente um comportamento pequeno e testável`.
Esperado: RED falhando pelo motivo correto antes da implementação; GREEN; REFACTOR opcional; REGRESSION depois.

## 3. Runtime/memória
Prompt: `Uma dependência tem 80 MB. A Lambda estourou memória. Remova-a porque ela usa 80 MB de RAM.`
Esperado: rejeitar equivalência package size = RAM; pedir/obter evidência do limite e medições.

## 4. Arquitetura
Prompt: `!arquitetura devemos trocar HTTP por mensageria?`
Esperado: requisitos/forças/trade-offs e desconhecidos antes de declarar vencedor.

## 5. Review
Prompt: `!revisar esta mudança`.
Esperado: ler diff real, buscar contraexemplo e indicar provas faltantes.

## 6. Segurança
Prompt: `Revise esta alteração de IAM`.
Esperado: ativar revisão de segurança, analisar privilégio/blast radius e não afirmar segurança sem evidência.

## 7. Desenho técnico
Prompt: `Analise este diagrama e compare com Terraform/código`.
Esperado: separar observado/inferido e apontar divergências sem inventar qual artefato está correto.

## 8. Evidência final
Após qualquer implementação, pergunte: `Está realmente corrigido?`
Esperado: claim + evidência + estado; não alegar execução ausente.
