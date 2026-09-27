# Dependências e supply chain

Usar quando a mudança adicionar, remover ou atualizar bibliotecas, runtimes, imagens, plugins, providers ou ferramentas de build.

## Investigar impacto
- Identificar versão atual, versão alvo, constraints, lockfile e dependências transitivas. Ler release notes/changelog quando houver mudança relevante de comportamento.
- Verificar requisitos de runtime, compatibilidade binária, mudanças de API/configuração e comportamento de defaults. Não assumir que atualização patch/minor é sempre transparente.
- Quando segurança motivar a atualização, confirmar o componente e versão realmente afetados e se a correção chega ao artifact distribuído.

## Provar
- Executar build/testes relevantes e, quando aplicável, verificar empacotamento, startup e integração que dependem da biblioteca alterada.
- Evitar desbloquear versão ou remover lockfile apenas para resolver conflito sem entender a árvore de dependências.
- Registrar mudanças transitivas relevantes e qualquer risco de downgrade, fork ou pacote não mantido.

## Entrega específica
Relatar versões antes/depois, motivo da mudança, compatibilidade verificada e comportamento que ficou sem teste. Não classificar upgrade como seguro apenas porque instalou ou compilou.
