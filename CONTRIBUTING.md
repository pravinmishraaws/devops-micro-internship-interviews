# Contributing

Thanks for helping build this community resource!

## Quick Checklist
- [ ] **One question per file** in `weeks/<week>/questions/`.
- [ ] File name: `Q####-kebab-title.md` (e.g., `Q0401-iam-role-vs-user.md`).
- [ ] Frontmatter includes: `id, title, difficulty, week, topics, tags, author, reviewed`.
- [ ] Run: `python scripts/validate_frontmatter.py && python scripts/build_index.py`.
- [ ] Update or add references; avoid plagiarism.
- [ ] Keep answers concise first (Short Answer), then **Deep Dive**, **Pitfalls**, **References**.

## Difficulty Levels
`entry | easy | medium | hard | expert`

## Local Dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/validate_frontmatter.py
python scripts/build_index.py
```

## Governance
- PR requires approval by CODEOWNERS for the touched week(s).
- CI enforces formatting and metadata.
- Discussions welcome for clarifications; best responses graduate to “reviewed: true”.
