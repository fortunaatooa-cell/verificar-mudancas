# Restrições antes do piloto

Este arquivo acompanha bank-pilot-restrictions.json. As seis respostas são externas ao código e não devem ser inventadas pelo agente.

O piloto fica bloqueado até haver resposta registrada para: ferramenta aprovada, propriedade do material, dados, segregação de funções, busca externa e confirmação da IBM/parte responsável quando aplicável. Além disso, deve existir aprovação de segurança registrada.

Valide antes do piloto:

    python3 scripts/check_pilot_readiness.py

O arquivo versionado começa com pending de propósito. Preencher somente com registros autorizados e sem publicar informação confidencial.
