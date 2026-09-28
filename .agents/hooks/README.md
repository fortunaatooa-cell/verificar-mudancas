# Hooks portáteis

Os hooks são contratos opcionais. Harnesses com suporte nativo podem mapear eventos; os demais podem chamar `python3 scripts/run_hook.py`.

Eventos canônicos:

- `pre-edit`: verifica aceite, hipótese/evidência e condições de segurança antes de mudança relevante.
- `post-edit`: resume arquivos alterados, fronteiras e verificações sugeridas.
- `pre-finish`: impede conclusão confiante sem evidência proporcional.

O runner recebe JSON por `--payload`, `--payload-file` ou stdin e devolve JSON. `block=true` significa que a ação correspondente não deve prosseguir automaticamente.
