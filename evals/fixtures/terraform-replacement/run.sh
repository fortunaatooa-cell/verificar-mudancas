#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
command -v terraform >/dev/null || { echo "ERRO: terraform não encontrado" >&2; exit 1; }
rm -rf .terraform terraform.tfstate terraform.tfstate.backup tag.tfplan replacement.tfplan tag.json replacement.json
terraform version
terraform fmt -check
terraform init -input=false
terraform validate

echo '=== baseline local: terraform_data apenas, sem cloud ==='
terraform apply -input=false -auto-approve -var='identifier=orders-prod' -var='owner=team-a' >/dev/null

echo '=== mudança somente de owner deve ser update in-place ==='
terraform plan -input=false -out=tag.tfplan -var='identifier=orders-prod' -var='owner=team-b' >/dev/null
terraform show -json tag.tfplan > tag.json
python3 - <<'PY'
import json
p=json.load(open('tag.json'))
rc=next(x for x in p['resource_changes'] if x['address']=='terraform_data.orders')
a=rc['change']['actions']
print('owner change actions:', a)
assert a == ['update'], a
PY

echo '=== mudança de identifier deve causar replacement ==='
terraform plan -input=false -out=replacement.tfplan -var='identifier=orders-main' -var='owner=team-b' >/dev/null
terraform show -json replacement.tfplan > replacement.json
python3 - <<'PY'
import json
p=json.load(open('replacement.json'))
rc=next(x for x in p['resource_changes'] if x['address']=='terraform_data.orders')
a=rc['change']['actions']
print('identifier change actions:', a)
assert set(a) == {'delete','create'} and len(a) == 2, a
PY

echo 'Terraform fixture OK: validate verde coexistiu com plans de update e replacement distintos.'
