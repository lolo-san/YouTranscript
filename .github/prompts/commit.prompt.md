---
description: Propose a commit message from staged & unstaged changes, then wait for approval
agent: agent
model: GPT-5 mini
---

Check the current Git changes in this workspace (both staged and unstaged).

Allowed commands for inspection:
- `git status --porcelain`  → to list staged and unstaged changes
- `git diff`               → to show unstaged diffs
- `git diff --staged`      → to show staged diffs

Rules:
- Only use these commands exactly as written.
- Do not add flags like `--name-only`, `--no-pager`, or any others.
- Do not run any other commands.
- Do not summarize diffs in detail; only extract enough to draft a commit message.
- Propose a **Conventional Commits** style commit message:
  - Format: `type(scope): short summary`
  - ≤ 70 characters for the title
  - Optional body if there are many files/changes (≤ 72 chars per line, each line starts with `-`)
- Do not suggest follow-up steps, risks, or recommendations.
- Do not reference files in the commit message.
- Wait for explicit approval before committing.

When I reply with **"proceed"**, then run:

```bash
git add -A
git commit -m "<commit title>
<commit body line 1>
<commit body line 2>
..."
```

Formatting rules for the commit command:
- The entire commit message (title + body) must be passed as one single string to git commit -m.
- Use \n newlines inside the quoted string to separate the title from body lines.
- Do not use multiple -m flags.
- Do not auto-commit without explicit approval.
- Do not invent a new message at commit time; reuse the one you proposed.
