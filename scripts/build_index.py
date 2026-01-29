import os, re, sys, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_frontmatter(md_path):
    t = md_path.read_text(encoding="utf-8")
    if not t.strip().startswith('---'):
        return None
    fm_text = t.split('---', 2)[1]
    return yaml.safe_load(fm_text) or {}

def replace_index(readme_path, table_md):
    t = readme_path.read_text(encoding="utf-8")
    start_marker = "## Index"
    if start_marker not in t:
        # append
        t = t.rstrip() + "\n\n" + table_md + "\n"
    else:
        pre, _, rest = t.partition(start_marker)
        # Keep header line; replace whole section until the next '## ' or EOF
        post = rest
        m = re.search(r"\n##\s", rest)
        if m:
            post = rest[m.start():]
            t = pre + table_md + "\n" + post
        else:
            t = pre + table_md + "\n"
    readme_path.write_text(t, encoding="utf-8")

for week_dir in sorted(ROOT.glob("weeks/week-*")):
    qdir = week_dir/"questions"
    if not qdir.exists():
        continue
    rows = []
    for q in sorted(qdir.glob("*.md")):
        fm = load_frontmatter(q)
        if not fm: 
            continue
        rows.append({
            "id": fm.get("id"),
            "title": fm.get("title"),
            "difficulty": fm.get("difficulty"),
            "tags": ", ".join(fm.get("tags", [])),
            "link": f"questions/{q.name}"
        })
    # Build table
    header = f"## Index\n| ID | Title | Difficulty | Tags | Link |\n|---|---|---|---|---|\n"
    body = "\n".join([f"| {r['id']} | {r['title']} | {r['difficulty']} | {r['tags']} | [Open]({r['link']}) |" for r in rows])
    table_md = header + body if rows else header + "| - | - | - | - | - |"
    replace_index(week_dir/"README.md", table_md)
