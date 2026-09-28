# /validar

Objetivo: validar uma alegação de conclusão contra evidência real.

- Liste claims materiais e a evidência de cada um.
- Use `verificador-evidencias` e o hook `pre-finish` quando disponível.
- Confirme que a prova relevante ocorreu depois da última mudança material.
- Se houver quality gate configurado, incorpore seu resultado; plano não executado vale no máximo `PARTIAL`.
- Saída por claim: `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED` ou `BLOCKED`.
