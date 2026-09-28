# Fixture: runtime port binding

Esta fixture verifica uma propriedade de runtime/container que aparece em PaaS, Docker, ECS, Kubernetes e proxies em geral: **um processo pode anunciar startup e responder dentro do próprio container sem estar alcançável pela fronteira externa**.

Ela não depende de Render nem simula um PaaS completo. O objetivo é provar o mecanismo subjacente sem confundir startup, `EXPOSE`, bind e alcançabilidade.

## Cenário 1 — quebrado

A imagem declara `EXPOSE 10000`, recebe `PORT=10000` e a aplicação registra `LISTENING 127.0.0.1:10000`.

O runner prova que:

- o processo responde em `127.0.0.1:10000` **dentro** do container;
- a porta está publicada pelo Docker;
- mesmo assim, a requisição feita do host para a porta publicada falha porque o processo está bound apenas em loopback.

Isso demonstra que `EXPOSE` e log de startup não substituem um listener alcançável na interface correta.

## Cenário 2 — correto

A única propriedade relevante muda para `BIND_ADDRESS=0.0.0.0`. A mesma porta publicada passa a responder `200 ok` a partir do host.

## Executar

Requer Docker:

```bash
bash evals/fixtures/runtime-port-binding/run.sh
```

## O que esta fixture não prova

- comportamento específico de Render, Railway, Cloud Run ou outro PaaS;
- service discovery, load balancer, firewall, ingress ou health check de uma plataforma real;
- que todo erro de `No open ports` é causado por loopback.

O oracle exige que o agente mantenha essas alternativas abertas e use experimentos progressivos para localizar a primeira fronteira que falha.
