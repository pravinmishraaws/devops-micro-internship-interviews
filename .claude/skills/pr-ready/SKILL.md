---
name: pr-ready
description: Review staged changes and draft a pull request title, description, and review considerations.
allowed-tools: Bash, Read, Grep
disable-model-invocation: true
---

# PR Ready Check

Review only the staged Git diff. Do not modify files, stage changes, commit, push, or open a pull request.

## Steps
1. Use Bash to inspect the staged diff with `git diff --cached`.
2. Use Read and Grep to examine relevant staged files for secret-like values, debug statements, and potential risks.
3. Report findings with the affected file and line when possible.
4. Clearly distinguish confirmed issues from possible concerns.
5. Draft a concise pull request title and description summarizing the changes.
6. Include review considerations and recommended tests.
7. If no issues are found, state that this is not a guarantee of safety.

Never expose or reproduce a real secret. Do not make changes on the user's behalf.
