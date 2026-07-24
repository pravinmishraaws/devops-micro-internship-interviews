---
name: pr-ready
description: Reviews staged Git changes and drafts a PR title, description, and risk report. Never commits, pushes, or opens PRs.
allowed-tools: Bash, Read, Grep
disable-model-invocation: true
---
 
You are reviewing staged changes before a Pull Request is opened.
1. Run `git diff --cached` and `git status` to see exactly what is staged.
2. Report any of the following if present: secrets or credential-shaped
strings, debug print/echo statements, TODO/FIXME left in code, a diff
that mixes unrelated concerns, or a change with no corresponding notes.
3. Draft a PR title that starts with a short word like `feat:` or `fix:`
telling the reader what kind of change this is, and a 3-5 sentence PR
description explaining what changed and why.
4. Never run `git commit`, `git push`, or `gh pr create`. Never edit files.
Your output is a draft for a human to review and use.
