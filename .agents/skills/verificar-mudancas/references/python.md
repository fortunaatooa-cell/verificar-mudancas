# Python

Ler quando a mudança envolver Python, serviços, automação, Lambda ou processamento de dados. Descobrir versão, gerenciador de dependências, ambiente virtual, lockfile, empacotamento, CI e comando de teste realmente usados.

## Diagnóstico

- Separar erro de lógica de erro de importação, ambiente, distribuição, arquitetura ou dependência nativa. Confirmar onde o código executa: máquina local, contêiner, Lambda, job ou cluster.
- Em AWS Lambda, conferir runtime, arquitetura, artifact/layers e versões efetivamente implantadas. Uma importação local bem-sucedida não prova que o mesmo pacote existe ou é compatível na runtime.
- Em chamadas externas, examinar timeouts, retries, paginação, throttling, serialização, credenciais sem exibir seus valores e idempotência. Em scripts, inspecionar caminhos relativos, encoding, locale e fuso horário.

## Provar

- Para regra determinística, usar o framework de testes existente (por exemplo, `pytest` se já configurado), com parametrização e casos limite relevantes. Para defeitos de integração, montar prova no ambiente com versões e formato de pacote compatíveis.
- Simular dependências externas nos testes isolados, mas verificar o contrato real quando ele for a causa suspeita. Distinguir teste que passou em ambiente local de execução do pacote distribuído.
- Se o ambiente corporativo não permitir reproduzir o empacotamento ou acessar a nuvem, fornecer verificações de runtime e comandos concretos para a equipe executar, marcando a causa como hipótese.

## Entrega específica

Registrar interpretador, ambiente, pacote executado e resultado de teste. Nunca recomendar instalar, remover ou substituir uma biblioteca apenas porque outro pacote possui nome parecido; conferir a dependência efetiva e a compatibilidade.
