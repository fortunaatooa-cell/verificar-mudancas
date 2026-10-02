# Playbook: bug de jogo

Usar quando o defeito depende de gameplay, engine/runtime, sequência de ações, cena/tela, física, input, save/load, multiplayer ou performance.

1. Identificar engine/framework, versão, target, build e estado/cena inicial.
2. Transformar o relato em passos reproduzíveis e registrar esperado x observado.
3. Capturar baseline com estado lógico, logs e sinais de runtime disponíveis.
4. Controlar variáveis relevantes como seed, tempo, FPS/timestep, input, save e topologia de rede.
5. Repetir e reduzir o cenário até o menor caso útil; registrar taxa de reprodução se intermitente.
6. Localizar a primeira divergência e testar hipóteses concorrentes.
7. Criar prova automatizada fora da runtime quando a propriedade for isolável; caso contrário, instrumentar a fronteira real.
8. Aplicar a menor correção sustentada.
9. Reexecutar o cenário original nas mesmas condições e verificar cenários vizinhos.
10. Correlacionar estado lógico e resultado visual; em multiplayer, observar as instâncias pertinentes; em performance, comparar métricas.
11. Entregar PASS, FAIL ou INCONCLUSIVE com evidências, build/target e lacunas.

Não considerar o bug corrigido apenas porque deixou de aparecer uma vez. Não usar compilação, FPS médio isolado, screenshot ou teste unitário fora da fronteira como prova universal de runtime.
