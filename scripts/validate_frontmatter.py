import os, re, sys, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUESTIONS = ROOT.glob("weeks/**/questions/*.md")

ALLOWED_DIFFICULTY = {"entry","easy","medium","hard","expert"}

def error(msg):
    print(f"::error::{msg}")
    return 1

rc = 0
for qpath in QUESTIONS:
    text = qpath.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        rc |= error(f"{qpath}: missing YAML frontmatter '---' block at top")
        continue
    try:
        fm_text = text.split('---', 2)[1]
        fm = yaml.safe_load(fm_text) or {}
    except Exception as e:
        rc |= error(f"{qpath}: YAML parse error: {e}")
        continue

    # Required fields
    required = ["id","title","difficulty","week","topics","tags","author","reviewed"]
    missing = [k for k in required if k not in fm]
    if missing:
        rc |= error(f"{qpath}: missing fields: {missing}")

    # ID + filename
    fname = qpath.name
    m = re.match(r"(Q\d{4})-", fname)
    if not m:
        rc |= error(f"{qpath}: filename must start with Q####-")
        continue
    if fm.get("id") != m.group(1):
        rc |= error(f"{qpath}: frontmatter id '{fm.get('id')}' != filename id '{m.group(1)}'")

    # Week folder match
    parts = qpath.parts
    for i, p in enumerate(parts):
        if p.startswith("week-"):
            week_folder = p.split("-")[1]
            break
    else:
        rc |= error(f"{qpath}: not inside a week-* folder")
        continue

    if str(fm.get("week")).zfill(2) != week_folder:
        rc |= error(f"{qpath}: frontmatter week {fm.get('week')} != folder week {week_folder}")

    # Difficulty
    if fm.get("difficulty") not in ALLOWED_DIFFICULTY:
        rc |= error(f"{qpath}: invalid difficulty '{fm.get('difficulty')}'. Allowed: {sorted(ALLOWED_DIFFICULTY)}")

sys.exit(rc)
