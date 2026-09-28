# Python

Ler quando a mudança envolver Python, serviços, automação, Lambda ou processamento de dados. Descobrir versão, gerenciador de dependências, ambiente virtual, lockfile, empacotamento, CI e comando de teste realmente usados.

## Diagnóstico

- Separar erro de lógica de erro de importação, ambiente, distribuição, arquitetura ou dependência nativa. Confirmar onde o código executa: máquina local, contêiner, Lambda, job ou cluster.
- Em AWS Lambda, conferir runtime, arquitetura, artifact/layers e versões efetivamente implantadas. Uma importação local bem-sucedida não prova que o mesmo pacote existe ou é compatível na runtime.
- Para funcionalidades com dependências opcionais (por exemplo, `pandas.read_parquet`), identificar qual engine/backend realmente executa o formato. Ter `pandas` instalado não implica ter `pyarrow` ou `fastparquet`; confirmar a dependência no mesmo ambiente/artifact que executará o código.
- Em pacotes com extensões nativas, verificar Python ABI, sistema operacional e arquitetura. Um wheel compatível no notebook/local pode não ser compatível no Linux/ARM/x86_64 do runtime alvo.
- Em chamadas externas, examinar timeouts, retries, paginação, throttling, serialização, credenciais sem exibir seus valores e idempotência. Em scripts, inspecionar caminhos relativos, encoding, locale e fuso horário.
- Para datas, distinguir datetime ingênuo de timezone-aware e registrar o timezone da regra de negócio. O mesmo instante pode pertencer a datas civis diferentes em UTC e no timezone local.

## Provar

- Para regra determinística, usar o framework de testes existente (por exemplo, `pytest` se já configurado), com parametrização e casos limite relevantes. Para defeitos de integração, montar prova no ambiente com versões e formato de pacote compatíveis.
- Quando a hipótese for dependência/empacotamento, testar em ambiente isolado ou artifact equivalente: provar a falha sem a dependência e a recuperação ao incluir a versão compatível é evidência mais forte do que apenas inspecionar `requirements.txt`.
- Simular dependências externas nos testes isolados, mas verificar o contrato real quando ele for a causa suspeita. Distinguir teste que passou em ambiente local de execução do pacote distribuído.
- Se o ambiente corporativo não permitir reproduzir o empacotamento ou acessar a nuvem, fornecer verificações de runtime e comandos concretos para a equipe executar, marcando a causa como hipótese.

## Entrega específica

Registrar interpretador, ambiente, arquitetura quando relevante, pacote executado e resultado de teste. Nunca recomendar instalar, remover ou substituir uma biblioteca apenas porque outro pacote possui nome parecido; conferir a dependência efetiva e a compatibilidade.
