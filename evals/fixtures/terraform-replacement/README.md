# Fixture executável — Terraform replacement

Usa Terraform **1.16.4** e o recurso built-in `terraform_data`, sem provider/cloud, para validar a distinção entre validação de configuração, update in-place e replacement.

## Executar

```bash
bash evals/fixtures/terraform-replacement/run.sh
```

O runner cria apenas state local descartável. O `apply -auto-approve` existe **somente na fixture isolada**, sobre `terraform_data`, sem recurso externo; não é recomendação para ambientes reais.

## Prova

1. `terraform fmt -check` e `terraform validate` passam.
2. Baseline local usa `identifier=orders-prod`, `owner=team-a`.
3. Alterar apenas `owner` gera `change.actions == ["update"]`.
4. Alterar `identifier`, que alimenta `triggers_replace`, gera ações `delete/create` (ou ordem equivalente de replacement).

Isso demonstra uma propriedade importante de `terraform-iac.md`: `validate` verde não prova ausência de replacement; a evidência precisa vir do `plan` contextualizado. A fixture usa `terraform show -json` para que a classificação seja verificável automaticamente.

## Limites

Não há AWS, Azure, GCP, provider externo, backend remoto, lock, drift real, credencial, banco nem dados persistentes. A fixture valida semântica de plan/replacement do Terraform, não segurança operacional de uma substituição real.
