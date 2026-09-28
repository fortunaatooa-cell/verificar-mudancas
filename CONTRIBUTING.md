# Contribuindo

## Regra principal

Toda regra nova no `SKILL.md` ou em uma referência deve ter pelo menos um caso em `evals/cases.json` ou uma fixture executável que justifique sua existência. Não adicionar regra apenas porque parece plausível.

## Orçamento do núcleo

`SKILL.md` deve permanecer em até **14.420 bytes**. Se uma nova regra fizer o núcleo ultrapassar esse limite, mova detalhe para uma referência e mantenha no núcleo apenas o princípio e o roteamento necessários.

## Evidência

- Preserve a distinção entre fato, hipótese e inferência.
- Não use exemplos, logs, nomes de sistemas, dados de clientes ou código proprietário de ambientes corporativos no repositório público.
- Casos sintéticos devem ser escritos do zero e usar somente dados fictícios.
- Quando um oracle mudar por causa de uma fixture, registre a razão no PR/changelog.

## Antes do PR

Execute:

```bash
python3 scripts/validate_repo.py
```

Quando houver mudança em referências cobertas por fixtures, execute também as fixtures pertinentes ou deixe o GitHub Actions fazê-lo antes do merge. Mudanças em comportamento do agente devem ser comparadas com a versão anterior usando o protocolo de `evals/ab/` quando aplicável.
