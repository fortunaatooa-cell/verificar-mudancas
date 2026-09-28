#!/usr/bin/env python3
"""Sanitized local engineering memory store."""

import argparse
import json
import re
import shutil
from pathlib import Path

KINDS = {"lesson": "lessons", "pattern": "patterns", "incident": "incidents"}
SECRET_VALUE_PATTERNS = [re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")]
SENSITIVE_KEYS = {"password", "passwd", "token", "secret", "api_key", "apikey", "access_key", "private_key"}


def _walk(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{path}.{key}" if path else str(key)
            yield current, key, child
            yield from _walk(child, current)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from _walk(child, f"{path}[{i}]")


def privacy_errors(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["documento deve ser objeto JSON"]
    if not isinstance(doc.get("id"), str) or not doc["id"].strip():
        errors.append("id textual obrigatório")
    kind = doc.get("kind")
    if kind not in KINDS:
        errors.append("kind deve ser lesson, pattern ou incident")
    privacy = doc.get("privacy")
    if not isinstance(privacy, dict) or privacy.get("sanitized") is not True:
        errors.append("privacy.sanitized=true é obrigatório")
    for path, key, value in _walk(doc):
        key_norm = str(key).lower().replace("-", "_")
        if key_norm in SENSITIVE_KEYS and value not in (None, "", "REDACTED", "<redacted>"):
            errors.append(f"campo sensível não redigido: {path}")
        if isinstance(value, str):
            for pattern in SECRET_VALUE_PATTERNS:
                if pattern.search(value):
                    errors.append(f"possível segredo detectado em {path}")
    return errors


def _memory_files(root):
    memory = root / "memory"
    for folder in KINDS.values():
        directory = memory / folder
        if directory.is_dir():
            yield from sorted(p for p in directory.glob("*.json") if p.is_file())


def reindex(root):
    entries = []
    for path in _memory_files(root):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        entries.append({"id": doc.get("id"), "kind": doc.get("kind"), "path": str(path.relative_to(root)).replace("\\", "/"), "title": doc.get("title") or doc.get("symptom") or doc.get("id")})
    index = {"version": 1, "entries": entries}
    index_path = root / "memory/index/index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def add(root, source, force=False):
    doc = json.loads(Path(source).read_text(encoding="utf-8"))
    errors = privacy_errors(doc)
    if errors:
        raise ValueError("; ".join(errors))
    folder = root / "memory" / KINDS[doc["kind"]]
    folder.mkdir(parents=True, exist_ok=True)
    safe_id = re.sub(r"[^A-Za-z0-9._-]+", "-", doc["id"]).strip("-.")
    if not safe_id:
        raise ValueError("id não gera nome de arquivo seguro")
    destination = folder / f"{safe_id}.json"
    if destination.exists() and not force:
        raise FileExistsError(f"memória já existe: {destination}")
    shutil.copyfile(source, destination)
    reindex(root)
    return destination


def search(root, query, limit=10):
    terms = {t for t in re.findall(r"[A-Za-zÀ-ÿ0-9_-]+", query.lower()) if len(t) > 2}
    scored = []
    for path in _memory_files(root):
        try:
            text = path.read_text(encoding="utf-8")
            doc = json.loads(text)
        except (OSError, ValueError):
            continue
        haystack = text.lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score, doc, path))
    scored.sort(key=lambda item: (-item[0], str(item[2])))
    return [{"score": score, "id": doc.get("id"), "kind": doc.get("kind"), "path": str(path.relative_to(root)).replace("\\", "/"), "summary": doc.get("title") or doc.get("symptom") or doc.get("generalizable_learning")} for score, doc, path in scored[:limit]]


def validate(root):
    errors = []
    seen = set()
    for path in _memory_files(root):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        current = privacy_errors(doc)
        errors.extend(f"{path}: {item}" for item in current)
        identifier = doc.get("id")
        if identifier in seen:
            errors.append(f"id duplicado: {identifier}")
        seen.add(identifier)
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    add_p = sub.add_parser("add")
    add_p.add_argument("file")
    add_p.add_argument("--force", action="store_true")
    search_p = sub.add_parser("search")
    search_p.add_argument("query")
    search_p.add_argument("--limit", type=int, default=10)
    sub.add_parser("reindex")
    sub.add_parser("validate")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "add":
        try:
            path = add(root, args.file, args.force)
            print(path)
        except (OSError, ValueError) as exc:
            print(f"ERRO: {exc}")
            raise SystemExit(1)
    elif args.command == "search":
        print(json.dumps(search(root, args.query, args.limit), ensure_ascii=False, indent=2))
    elif args.command == "reindex":
        print(json.dumps(reindex(root), ensure_ascii=False, indent=2))
    else:
        errors = validate(root)
        if errors:
            for error in errors:
                print(f"ERRO: {error}")
            raise SystemExit(1)
        print("Memória válida e sanitizada.")


if __name__ == "__main__":
    main()
