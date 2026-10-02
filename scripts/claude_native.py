#!/usr/bin/env python3
"""Generate/install Claude Code native wrappers for verificar-mudancas.

The portable files remain the source of truth. Native Claude files are generated
from them so Claude Code can use CLAUDE.md, skills, subagents, rules and hooks
without duplicating the methodology by hand.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

COMMANDS: dict[str, dict[str, Any]] = {
    "verificar": {
        "description": "Executa o ciclo completo de investigação, mudança e verificação com evidência.",
        "tools": ["Read", "Grep", "Glob", "Bash", "Edit", "Write"],
    },
    "investigar": {
        "description": "Investiga causa e evidência sem editar arquivos ou aplicar correções.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "planejar": {
        "description": "Planeja uma mudança ampla, dependências, riscos e critérios de aceite antes de editar.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "arquitetura": {
        "description": "Reconstrói a arquitetura atual e propõe decisões estruturais com trade-offs explícitos.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "tdd": {
        "description": "Executa TDD somente quando houver RED observável antes da implementação.",
        "tools": ["Read", "Grep", "Glob", "Bash", "Edit", "Write"],
    },
    "adr": {
        "description": "Registra decisão arquitetural material sem confundir ADR com prova de implantação.",
        "tools": ["Read", "Grep", "Glob", "Write"],
    },
    "corrigir": {
        "description": "Investiga, corrige com a menor mudança correta e valida regressão e evidência.",
        "tools": ["Read", "Grep", "Glob", "Bash", "Edit", "Write"],
    },
    "revisar": {
        "description": "Revisa diff ou PR de forma adversarial, procurando regressões, riscos e evidência insuficiente.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "validar": {
        "description": "Valida alegações contra evidências e classifica PASS, FAIL ou INCONCLUSIVE.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "portao-qualidade": {
        "description": "Executa o quality gate proporcional ao risco, sem alegar checks não executados.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "aprender": {
        "description": "Propõe aprendizado sanitizado e regressões revisáveis sem promoção automática.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "desenho-tecnico": {
        "description": "Analisa ou especifica desenho técnico sem inventar medidas, escala ou render inexistente.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "depurar-jogo": {
        "description": "Reproduz, investiga, corrige e valida bugs de jogo/runtime quando autorizado.",
        "tools": ["Read", "Grep", "Glob", "Bash", "Edit", "Write"],
    },
}

AGENTS: dict[str, dict[str, Any]] = {
    "investigador": {
        "description": "Use para investigar bugs, localizar a primeira divergência e comparar hipóteses concorrentes.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "planejador": {
        "description": "Use para decompor mudanças amplas, dependências, riscos e sequência de implementação.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "arquiteto": {
        "description": "Use para decisões estruturais duráveis, fronteiras de dados e trade-offs arquiteturais.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "diagnosticador-runtime": {
        "description": "Use para memória, JVM, containers, Lambda, rede, recursos, startup e problemas de runtime.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "estrategista-testes": {
        "description": "Use para escolher a prova correta, teste discriminante e fronteira de regressão.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "implementador": {
        "description": "Use quando a causa e o aceite estiverem claros e for preciso aplicar a menor mudança correta.",
        "tools": ["Read", "Grep", "Glob", "Bash", "Edit", "Write"],
    },
    "revisor-codigo": {
        "description": "Use depois da implementação para revisão adversarial, contraexemplos e regressões.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "revisor-seguranca": {
        "description": "Use quando houver superfície de segurança, dados sensíveis, IAM, conteúdo não confiável ou alto risco.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "verificador-evidencias": {
        "description": "Use no fim para confrontar alegações com evidências e emitir PASS, FAIL ou INCONCLUSIVE.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "agente-aprendizado": {
        "description": "Use após uma resolução para propor aprendizado sanitizado sem promover memória automaticamente.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "analista-desenhos-tecnicos": {
        "description": "Use para interpretar ou criar material técnico visual com limites explícitos de precisão.",
        "tools": ["Read", "Grep", "Glob"],
    },
    "investigador-gameplay": {
        "description": "Use para reproduzir, reduzir e instrumentar bugs de gameplay ou runtime interativo.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
    "validador-regressao-jogo": {
        "description": "Use depois do fix para repetir o cenário original e validar regressões do jogo.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
    },
}

RULES = (
    "evidence-first.md",
    "testing.md",
    "tdd-cycle.md",
    "architecture-decisions.md",
    "safe-change.md",
    "high-risk.md",
    "regulated.md",
    "visual-evidence.md",
)

CLAUDE_MD = """# Verificar Mudanças — Claude Code

Este workspace usa o `verificar-mudancas` como harness de engenharia. Este arquivo é curto de propósito: procedimentos detalhados ficam em skills e especialistas para preservar contexto.

## Fonte de verdade

- Orquestração portátil: `AGENTS.md`.
- Núcleo metodológico: `.agents/skills/verificar-mudancas/SKILL.md`.
- Papéis: `.agents/agents/`.
- Comandos: `.agents/commands/`.
- Regras: `.agents/rules/`.

Quando houver conflito entre um wrapper nativo de Claude e o arquivo portátil correspondente, o arquivo portátil é canônico.

## Uso nativo no Claude Code

- Skills ficam em `.claude/skills/`; podem ser chamadas por `/verificar`, `/investigar`, `/corrigir`, `/revisar`, `/validar`, `/depurar-jogo` e demais comandos existentes.
- Subagents ficam em `.claude/agents/`. Delegue somente trabalho especializado ou isolável; tarefas independentes podem rodar em paralelo.
- A sessão principal integra resultados, decide conflitos e é responsável pela validação final.
- Regras em `.claude/rules/` espelham as regras portáteis.
- Hooks em `.claude/settings.json` adicionam guardrails determinísticos sem substituir a metodologia.

## Invariantes

- evidência antes de confiança;
- fato ≠ hipótese ≠ inferência ≠ desconhecido;
- não alegar execução, visão, render, teste ou acesso que não ocorreu;
- investigação retorna à hipótese quando a evidência contradiz a causa;
- implementação usa a menor mudança correta;
- HIGH/CRITICAL exige controles e `aprovacao_humana_necessaria=true`;
- dados corporativos, secrets e código proprietário não entram no repositório público.

A branch `feature/agentic-v1-5` continua experimental até as provas T8/T14 da Spec 10/10.
"""


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _frontmatter(name: str, description: str, tools: list[str] | None = None, agent: bool = False) -> str:
    lines = ["---", f"name: {name}", f"description: {_yaml_string(description)}"]
    if tools and agent:
        lines.append(f"tools: [{', '.join(tools)}]")
    if agent:
        lines.append("model: inherit")
        lines.append("skills: [verificar-mudancas]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def render_skill(source_root: Path, name: str) -> str:
    if name == "verificar-mudancas":
        return (source_root / ".agents/skills/verificar-mudancas/SKILL.md").read_text(encoding="utf-8")
    meta = COMMANDS[name]
    body = (source_root / ".agents/commands" / f"{name}.md").read_text(encoding="utf-8").strip()
    prefix = (
        "Este é o wrapper nativo do Claude Code para o comando portátil. "
        "Aplique também o núcleo em `.agents/skills/verificar-mudancas/SKILL.md`.\n\n"
    )
    return _frontmatter(name, meta["description"], meta["tools"]) + prefix + body + "\n"


def render_agent(source_root: Path, name: str) -> str:
    meta = AGENTS[name]
    body = (source_root / ".agents/agents" / f"{name}.md").read_text(encoding="utf-8").strip()
    prefix = (
        "Você é um especialista delegado pelo harness verificar-mudancas. "
        "Seu papel portátil abaixo é a fonte de verdade desta subtask. "
        "Trabalhe somente no escopo recebido e devolva fatos, evidências, limitações e resultado ao agente principal.\n\n"
    )
    return _frontmatter(name, meta["description"], meta["tools"], agent=True) + prefix + body + "\n"


def render_rule(source_root: Path, filename: str) -> str:
    body = (source_root / ".agents/rules" / filename).read_text(encoding="utf-8").strip()
    return (
        "<!-- Gerado de .agents/rules/" + filename + "; mantenha o arquivo portátil como fonte de verdade. -->\n\n"
        + body
        + "\n"
    )


def render_settings(runtime_script: str) -> str:
    command = f'python "${{CLAUDE_PROJECT_DIR}}/{runtime_script}"'
    payload = {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": command + ' session-start --root "${CLAUDE_PROJECT_DIR}"',
                        }
                    ]
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash|Write|Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command + ' pre-tool --root "${CLAUDE_PROJECT_DIR}"',
                        }
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Write|Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": command + ' post-edit --root "${CLAUDE_PROJECT_DIR}"',
                        }
                    ],
                }
            ],
        }
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def native_files(source_root: Path, installed: bool = False) -> dict[Path, str]:
    runtime_script = (
        ".verificar-mudancas/scripts/claude_hook_bridge.py"
        if installed
        else "scripts/claude_hook_bridge.py"
    )
    files: dict[Path, str] = {
        Path("CLAUDE.md"): CLAUDE_MD,
        Path(".claude/settings.json"): render_settings(runtime_script),
        Path(".claude/skills/verificar-mudancas/SKILL.md"): render_skill(source_root, "verificar-mudancas"),
    }
    for name in COMMANDS:
        files[Path(".claude/skills") / name / "SKILL.md"] = render_skill(source_root, name)
    for name in AGENTS:
        files[Path(".claude/agents") / f"{name}.md"] = render_agent(source_root, name)
    for filename in RULES:
        files[Path(".claude/rules") / filename] = render_rule(source_root, filename)
    return files


def install_native(
    source_root: Path,
    target: Path,
    *,
    mode: str,
    force: bool,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    files = native_files(source_root, installed=True)
    allowed_prefixes = {Path(".claude/skills/verificar-mudancas/SKILL.md")}
    for relative, content in files.items():
        if mode != "full" and relative not in allowed_prefixes:
            continue
        destination = target / relative
        if destination.exists() and not force:
            operations.append({"path": str(destination), "status": "skipped-existing"})
            continue
        operations.append({"path": str(destination), "status": "planned" if dry_run else "written"})
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for relative, content in native_files(root, installed=False).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(path)
