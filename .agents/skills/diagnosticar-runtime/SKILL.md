---
name: diagnosticar-runtime
description: Diagnosticar JVM, containers, Lambda, memória, CPU, GC, startup, portas, health checks, rede, timeout e limites de recurso sem confundir tamanho de artefato com RAM.
---
# Diagnóstico de runtime
Distinguir artifact size, heap, metaspace, native memory, container memory, build memory, startup e steady state.
`tamanho de JAR/lib != consumo de RAM`.
Identifique qual processo/limite falhou antes de recomendar mais recurso.
Diferencie OOM da JVM de kill externo.
Compare baseline e estado alterado quando houver medição.
Cálculos devem informar unidade, fonte e premissas.
