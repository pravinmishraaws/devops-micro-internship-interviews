# Contributing

Thanks for helping build this community resource! Every improvement helps future learners.

> **Goal:** create high-quality, searchable, and reviewable interview Q&A—organized by week—so students can practice effectively and reviewers can maintain consistency at scale.

---

## Checklist (Do These)

* [ ] **One question per file** in `weeks/<week>/questions/`. 
  *Why:* Keeps reviews small and searchable.
* [ ] File name: **`Q####-kebab-title.md`** (e.g., `Q0401-iam-role-vs-user.md`). 
  *Why:* Consistent IDs make indexing and linking reliable.
* [ ] Include **frontmatter** fields: `id, title, difficulty, week, topics, tags, author, reviewed`. 
  *Why:* Metadata powers validation, search, and dashboards.
* [ ] Run validators before committing: 

  ```bash
  python scripts/validate_frontmatter.py && python scripts/build_index.py
  ```

  *Why:* CI will fail otherwise—faster feedback locally.
* [ ] Add/update references; **avoid plagiarism** (cite sources). 
  *Why:* This is a learning resource—be fair and accurate.
* [ ] Answer layout: **Short Answer** → **Deep Dive** → **Pitfalls** → **References**. 
  *Why:* Mimics interview flow: quick reply, then depth and nuance.

---

## Difficulty Levels

Use one of: `entry | easy | medium | hard | expert`
*Why:* Helps learners choose the right challenge level.

---

## Frontmatter Template (Copy This)

```yaml
---
id: Q0001
title: OSI vs TCP/IP — what’s the practical difference?
difficulty: entry
week: 00
topics: [networking, models]
tags: [networking, osi, tcpip]
author: pravinmishraaws
reviewed: false
---

## Question
Compare OSI and TCP/IP models and explain how they map to real-world troubleshooting.

## Short Answer
- OSI is a teaching model (7 layers); TCP/IP is pragmatic (4–5 layers) used on the Internet.
- Map examples: DNS (app), TCP/UDP (transport), IP (network), Ethernet/Wi‑Fi (link).
- Troubleshoot top→down or bottom→up; verify each layer (DNS, TCP handshake, routing, link).

## Deep Dive
- Mapping table, typical tools: `ping`, `traceroute`, `dig`, `curl`, `tcpdump`.

## Pitfalls
- Confusing DNS failures (app) with network reachability (IP/route).

## References
- https://datatracker.ietf.org/doc/html/rfc1122

---
```

> **Tip:** `id` must match the file name’s number (e.g., `Q0401` ↔ `Q0401-...md`).

---

## Recommended Answer Structure

```markdown
## Short Answer
Concise, interviewer-ready definition in 2–4 sentences.

## Deep Dive
- Explain the concept with context and trade-offs.
- Add examples, diagrams (if useful), and edge cases.

## Pitfalls / Gotchas
- Common mistakes and how to avoid them.

## References
- Official docs
- High-quality blogs or whitepapers
```

*Why:* Consistent structure makes contributions skimmable and reviewable.

---

## Local Development

### macOS / Linux

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/validate_frontmatter.py
python scripts/build_index.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r scripts\requirements.txt
python scripts\validate_frontmatter.py
python scripts\build_index.py
```

*Why:* Running validators locally saves CI cycles and reviewer time.

---

## Governance & Reviews

* **CODEOWNERS** approval is required for the **week(s)** your change touches.
  *Why:* Ensures subject-matter review.
* **CI** enforces formatting and metadata.
  *Why:* Keeps the repo tidy and searchable.
* Use **Discussions** for clarifications. The best responses graduate to `reviewed: true`.
  *Why:* Promotes consensus before code.

---

## Step 1 — Fork & Authenticate

1. **Fork** the repo to your account:
   [https://github.com/pravinmishraaws/devops-micro-internship-interviews](https://github.com/pravinmishraaws/devops-micro-internship-interviews)
   *Why:* You can’t push to the original; forks are the standard workflow.

2. **Authenticate Git** so pushes work from your terminal.

### SSH (Recommended)

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Copy the contents of `~/.ssh/id_ed25519.pub` into GitHub → **Settings → SSH and GPG keys**.

Force Git to use SSH (avoids https prompts):

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### HTTPS (Alternative)

```bash
git config --global credential.helper cache
```

### Test Authentication

```bash
git ls-remote git@github.com:yourusername/devops-micro-internship-interviews.git
```

✅ **Expected:** You have a fork and your terminal can talk to GitHub.

---

## Step 2 — Clone Your Fork Locally

```bash
git clone git@github.com:yourusername/devops-micro-internship-interviews.git
cd devops-micro-internship-interviews
git remote -v
```

* `origin` → your fork

Add `upstream` (the original):

```bash
git remote add upstream https://github.com/pravinmishraaws/devops-micro-internship-interviews.git
```

✅ **Expected:** You have **origin** (your fork) and **upstream** (original).
*Why:* Keeps your fork fresh and conflict-free.

---

## Step 3 — Create a Feature Branch & Make a Change

Create a new branch:

```bash
git checkout -b Q####-kebab-title
```

Add or edit your question file:

* Go to: `weeks/<week>/questions/`
* Create (or copy) `Q####-kebab-title.md`
* Edit the content following the template

```markdown
# (Your question title)

## Short Answer
...

## Deep Dive
...

## Pitfalls / Gotchas
...

## References
- ...
```

Stage & commit:

```bash
git add weeks/<week>/questions/Q####-kebab-title.md
git commit -m "question(Q####): add IAM role vs user with pitfalls and refs"
```

*Why:* Small, focused branches are easier to review and iterate.

---

## Step 4 — Sync With Upstream & Push to Your Fork

Keep `main` up to date:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

Rebase your branch (recommended for a clean history):

```bash
git checkout Q####-kebab-title
git rebase main
```

Push:

```bash
git push -u origin Q####-kebab-title
```

✅ **Expected:** Your feature branch appears on your fork.
*Why:* Rebasing reduces merge commits and review noise.

---

## Step 5 — Open a Pull Request

1. Go to your fork on GitHub.

2. Click **Compare & pull request**.

3. Base: `pravinmishraaws/devops-micro-internship-interviews:main`
   Compare: `yourusername:Q####-kebab-title`

4. **Title** (use Conventional Commits where possible):

   ```
   question(Q0401): add IAM role vs user with pitfalls and references
   ```

5. **Description** (be clear and specific):

   ```
   Adds Q0401 under week 4 with Short Answer, Deep Dive, Pitfalls, and References.
   Includes frontmatter and passes metadata validation.
   ```

6. Submit the PR.

*Why:* Clear titles/descriptions speed up reviews and indexing.

---

## Commit Message Guidance (Conventional Commits)

Use a type + scope when possible:

```
question(Q0401): add IAM role vs user
docs: update contributing examples
chore: fix build index script path
```

*Why:* Predictable history helps future auditing and automation.

---

## Quality Bar (What Reviewers Look For)

* **Accuracy:** No factual errors; trade-offs mentioned where relevant.
* **Clarity:** Short Answer is crisp; Deep Dive adds real value.
* **Citations:** Official docs or reputable sources in **References**.
* **Consistency:** Naming, `id`, and frontmatter fields match conventions.
* **Validation:** Scripts pass locally and in CI.

---

## Common Pitfalls & Quick Fixes

* **Mismatch:** `id` in frontmatter ≠ file name number → *Fix both to match.*
* **Missing fields:** Validation script fails → *Copy the template frontmatter.*
* **Long walls of text:** No Short Answer/Pitfalls → *Refactor into sections.*
* **No references:** Add **at least one** official doc link.

---

## Code of Conduct

Be respectful, constructive, and kind. Disagreements are fine—disrespect isn’t.
*Why:* This is a learning space; we optimize for safety and growth.

---

## FAQ

**Q: Can I add multiple questions in one PR?**
A: Prefer **one question per PR**. Easier to review and revert if needed.

**Q: Can I update an existing answer?**
A: Yes. Explain **what** changed and **why** in your PR description.

**Q: My CI failed—what now?**
A: Run the local validators, fix frontmatter or structure, and push again.

---

## Maintainers’ Notes (for transparency)

* PRs touching certain weeks require **CODEOWNERS** approvals.
* CI checks formatting and schema; failing PRs will be blocked until fixed.
* High-quality answers will be marked `reviewed: true` after consensus.

---

### Thank you!

Your contributions help hundreds of learners prepare with confidence. 🙌


If you want, I can also create a **PR template** (`.github/pull_request_template.md`) and a **contribution issue template** to guide first-timers.
