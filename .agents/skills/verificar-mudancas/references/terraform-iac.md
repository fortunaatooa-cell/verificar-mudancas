# Terraform e infraestrutura como código

Usar esta referência quando a mudança envolver Terraform, OpenTofu ou infraestrutura declarativa semelhante. Aplicar também o núcleo de `SKILL.md`: esta referência complementa a investigação, não substitui evidência nem autorização para alterar recursos externos.

## Descobrir o contexto antes de concluir

- Identificar a versão de Terraform/OpenTofu, providers, módulos, lockfile, backend, workspace/ambiente, fontes de variáveis e comandos reais usados pelo projeto. Não assumir ambiente, conta, região ou backend pelo nome dos arquivos.
- Verificar o estado inicial do repositório e separar mudança de configuração, mudança de state e drift remoto. Um `plan` diferente pode decorrer de código, variáveis, provider, versão, state desatualizado ou alteração feita fora do IaC.
- Confirmar qual diretório/root module está sendo avaliado e quais módulos reutilizáveis são afetados. Em monorepos, não extrapolar resultado de um stack para outro.
- Tratar arquivos de state, planos binários, outputs, logs e `*.tfvars` como potencialmente sensíveis. `sensitive = true` reduz exposição em alguns outputs, mas não torna o state isento de segredos.

## Produzir evidência segura

- Preferir os comandos e wrappers definidos pelo projeto. Quando aplicável e autorizado, verificar formatação e sintaxe com `terraform fmt -check` e `terraform validate` após inicialização compatível com o ambiente.
- `terraform validate` verifica configuração, não compara a configuração com state/variáveis/recursos reais. Um `validate` verde não exclui replacement, destroy, drift ou blast radius que só aparecem no `plan` contextualizado.
- Para mudança de comportamento, obter um `terraform plan` no ambiente correto e revisar o diff por endereço de recurso. Distinguir explicitamente **create**, **update in-place**, **destroy** e **replace** (`-/+` ou `+/-`).
- Quando automatizar revisão, um plano salvo seguido de `terraform show -json` permite inspecionar `resource_changes[*].change.actions`. Replacement aparece como combinação `delete/create` ou `create/delete`; não inferir segurança apenas do resumo textual.
- Investigar qualquer `forces replacement`, destruição inesperada, mudança de endereço, alteração de `count`/`for_each`, chave renomeada, provider trocado ou mudança de módulo antes de aceitar o plano. Uma alteração descrita como "só tag" não prova que o restante do plano é seguro.
- Quando útil, salvar o plano (`-out`) e usar uma representação legível ou JSON para revisão automatizada, sem publicar conteúdo sensível. Não tratar `terraform validate` como prova de que a infraestrutura resultante é segura ou funcional.
- Em suspeita de drift, comparar configuração, state e recurso remoto pelos meios autorizados. Um `plan` normal pode detectar diferenças, e um fluxo `-refresh-only` pode ajudar a isolar drift quando suportado e apropriado; não atualizar state apenas para fazer o diff desaparecer.

## State, endereço e migração

- Antes de `state mv`, `state rm`, importação, `moved` blocks ou troca de backend, confirmar o endereço antigo/novo, dependências, ownership e procedimento de rollback. Essas operações alteram a associação entre configuração e recursos reais mesmo quando não mudam o recurso imediatamente.
- Preferir mecanismos declarativos, como `moved` e `import` blocks quando compatíveis com a versão e padrões do projeto, em vez de comandos manuais não reproduzíveis.
- Não editar state manualmente. Se uma operação excepcional sobre state for necessária, exigir autorização explícita, lock/backup conforme o backend, escopo mínimo e verificação posterior.
- Verificar estabilidade das chaves de `for_each` e índices de `count`; reordenação ou mudança de chave pode causar substituições ou associação incorreta de recursos.

## Segurança, blast radius e dados persistentes

- Para recursos com dados ou alto impacto, revisar proteção contra destruição, snapshots/backups, retenção, replicação, criptografia, políticas de acesso, exposição de rede e dependências. Não sugerir destruição/recriação como correção rotineira quando houver risco de perda de dados.
- Em IAM e políticas, revisar aumento de privilégio, wildcards, trust relationships e escopo de recurso. Em rede, verificar exposição pública, regras amplas, portas e caminhos de entrada/saída. Em storage/bancos, verificar criptografia, versionamento, retenção e comportamento de exclusão.
- Confirmar compatibilidade de versões e constraints de providers/módulos. Mudanças de provider podem alterar defaults, schema e comportamento mesmo sem alteração aparente no HCL.
- Não imprimir, commitar ou copiar segredos de variáveis, state, outputs ou credenciais para relatórios públicos. Redigir evidência sensível preservando apenas o necessário para o diagnóstico.

## Aplicação e verificação final

- `terraform apply` altera recursos externos e **não é autorizado apenas pela existência desta skill**. Executar somente quando a tarefa e o ambiente concederem autorização explícita e o plano revisado corresponder ao que será aplicado.
- Não usar `-auto-approve`, `-target`, `-replace`, desbloqueio forçado ou opções equivalentes como atalho sem justificar necessidade, efeitos colaterais e autorização. `-target` pode produzir estado intermediário e não deve virar fluxo normal de correção.
- Antes de aplicar, registrar ambiente, plano esperado, mudanças destrutivas/substitutivas, impacto, dependências, estratégia de rollback/recuperação e critério observável de aceite.
- Após aplicação autorizada, verificar o estado final na fronteira correta: novo `plan` sem mudança inesperada quando apropriado, health/smoke checks do serviço, permissões, conectividade e integridade dos dados afetados. Não declarar sucesso apenas porque o comando `apply` terminou sem erro.
- Para mudanças que não foram aplicadas, entregar claramente **o que o plan indica**, **qual causa está sustentada**, **o que permanece incerto**, **quais riscos existem** e **qual verificação deve preceder qualquer apply**.
