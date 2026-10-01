#!/usr/bin/env python3
"""Builds index.json from recipes/*.txt, the list the Hazel app reads.

  python3 tools/build_index.py           write index.json
  python3 tools/build_index.py --check   fail if index.json is out of date or a recipe breaks a rule

Each entry carries the setting keys the recipe uses, so an app that doesn't know one of them yet can
say the recipe needs a newer version instead of quietly leaving that setting out.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
INDEX = ROOT / "index.json"
# The camera stores the recipe with every photo in a fixed 1024-byte record: the name line plus the
# settings, without the other note lines. Up to 110 of those bytes are the camera's own (photo, time,
# grain seed), which leaves 914. The app refuses a recipe over this, counting the same way.
SIDECAR_BYTES = 1024 - 110
# Film stock names are fine; company names are trademarks and stay out of recipe names.
COMPANY_NAMES = re.compile(r"\b(kodak|fuji|fujifilm|hasselblad|ilford|agfa|polaroid|leica)\b", re.IGNORECASE)
SETTING = re.compile(r"^\s*([a-z_]+)\s*=\s*\S")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def entry(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems = []
    if not lines or not lines[0].startswith("# "):
        return None, [f"{path.name}: the first line must be '# <name>'"]
    name = lines[0][2:].strip()
    notes = [l[1:].strip() for l in lines[1:] if l.startswith("#")]
    keys = sorted({m.group(1) for l in lines if not l.startswith("#") and (m := SETTING.match(l))})
    stored = "".join(l + "\n" for i, l in enumerate(text.split("\n")) if i == 0 or not l.startswith("#"))
    if path.stem != slug(name):
        problems.append(f"{path.name}: file name should be {slug(name)}.txt for '{name}'")
    if COMPANY_NAMES.search(name):
        problems.append(f"{path.name}: '{name}' has a company name in it; say 'Inspired by ...' in a note instead")
    if not notes:
        problems.append(f"{path.name}: needs a description on the second line")
    if len(stored.encode()) > SIDECAR_BYTES:
        problems.append(f"{path.name}: {len(stored.encode())} bytes of settings, the camera keeps {SIDECAR_BYTES}")
    return {
        "name": name,
        "file": f"recipes/{path.name}",
        "description": notes[0] if notes else "",
        "notes": notes[1:],
        "black_and_white": "mono = 1" in text or "film = silver" in text,
        "keys": keys,
        "bytes": len(text.encode()),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
    }, problems


def build():
    entries, problems = [], []
    for path in sorted(RECIPES.glob("*.txt")):
        e, p = entry(path)
        problems += p
        if e:
            entries.append(e)
    names = [e["name"].lower() for e in entries]
    problems += [f"two recipes are called '{n}'" for n in sorted({n for n in names if names.count(n) > 1})]
    return {"version": 1, "recipes": entries}, problems


def main(argv):
    index, problems = build()
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    for p in problems:
        print(p, file=sys.stderr)
    if "--check" in argv:
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != text:
            print("index.json is out of date: run python3 tools/build_index.py", file=sys.stderr)
            return 1
        return 1 if problems else 0
    if problems:
        return 1
    INDEX.write_text(text, encoding="utf-8")
    print(f"index.json: {len(index['recipes'])} recipes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
