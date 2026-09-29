# Configuração recomendada no Devin

## Forma preferida
Descompacte este pacote **na raiz do repositório que o Devin vai editar**.
O resultado deve conter:
- `AGENTS.md`
- `.agents/skills/...`
- `devin/...`

A documentação atual do Devin usa `.agents/skills/` para skills locais no repositório.

## Devin's Machine / Repo Setup
Configure normalmente:
1. Git Pull
2. Secrets
3. Install dependencies
4. Maintain dependencies
5. Lint
6. Tests
7. Run app locally
8. Additional Notes

Em **Additional Notes**, cole o conteúdo de `devin/repo-setup/ADDITIONAL_NOTES.txt`.

Não substitua os comandos reais do seu projeto pelos exemplos deste pacote. O Devin deve descobrir/validar os comandos reais do repo.

## Playbooks
Os arquivos em `devin/playbooks/` são templates prontos para Settings → Playbooks.
Crie somente os macros que forem úteis; não é obrigatório cadastrar todos para a skill funcionar.

## Knowledge
`devin/knowledge/VERIFICAR_MUDANCAS.md` é uma versão condensada para Knowledge caso sua organização use essa camada.
Não duplique Knowledge se as mesmas regras já estiverem sendo recuperadas adequadamente das skills.

## Teste inicial
Use `devin/acceptance-tests/TESTES.md` para validar roteamento e disciplina de evidência antes de usar em trabalho real.
