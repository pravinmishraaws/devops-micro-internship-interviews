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

## Step 1 — Fork & Authenticate

Login to GitHub and Fork the mini_finance repo into your account.
In your terminal, configure authentication:

#### SSH (Recommended)

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
````
* Copy the contents of `~/.ssh/id_ed25519.pub` into GitHub → **Settings → SSH and GPG keys**

Force Git to use SSH:

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

#### HTTPS (Alternative)

```bash
git config --global credential.helper cache
```

#### Test Authentication

```bash
git ls-remote git@github.com:yourusername/devops-micro-internship-interviews.git
```

✅ **Expected Outcome:** You have forked the repo, and your terminal is authenticated for Git operations.

---

#### Step 2 — Clone Your Fork Locally

```bash
git clone git@github.com:yourusername/devops-micro-internship-interviews.git
cd devops-micro-internship-interviews
git remote -v
```

* `origin` → your fork
* Add an `upstream` remote to the original repo:

```bash
git remote add upstream https://github.com/pravinmishraaws/devops-micro-internship-interviews.git
```

✅ **Expected Outcome:** Local clone has **origin** (your fork) and **upstream** (original repo).

---

## Step 3 — Create a Feature Branch & Make a Change

Create a new branch:

```bash
git checkout -b Q####-kebab-title
```

**Copy and Past existing file** OR **Add/Edit/RNAME** `Q####-kebab-title.md` → add this new section:

```markdown
Addit the file and add your qustion/anwer
```

Stage & commit:

```bash
git add Q####-kebab-title.md
git commit -m "question: added question (good message) note"
```

---

## Step 4 — Pull From Upstream & Push to Origin

Sync changes from upstream:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

Switch back to your feature branch:

```bash
git checkout Q####-kebab-title
git rebase main   # optional but recommended
```

Push your branch:

```bash
git push -u origin Q####-kebab-title
```

✅ **Expected Outcome:** Your branch is available on GitHub under your fork.

---

## Step 5 — Create a Pull Request

1. Go to your fork on GitHub
2. Click **Compare & Pull Request**
3. Target: `pravinmishraaws/devops-micro-internship-interview:main` ← from `yourusername:Q####-kebab-title`
4. Title:

   ```
   docs: update README with assignment note
   ```
5. Description:

   ```
   This PR adds a new section to the README explaining the project's purpose in the context of this GitHub assignment.
   ```
6. Submit the Pull Request.
