---
name: commit-push
description: Commit all changes and push directly to the main branch. Use when user wants to save work, publish changes, update the site, or sync changes to the remote repository. Triggers on: "commit and push", "save my changes", "publish changes", "update site", "sync to main", "push to main".
---

# Commit & Push to Main

Inspects changes, auto-generates a commit message, commits, and pushes directly to the main branch.

## Workflow

### Step 1: Inspect Changes

Run `git status` to see what files have changed.

### Step 2: Review the Diff

Run `git diff --stat` to show a summary of changes. Present this to the user if there are many files or large changes.

### Step 3: Generate Commit Message

Run `git log --oneline -5` to understand the project's commit message style.

Auto-generate a conventional commit message based on the diff:
- New content files (posts, pages): `feat(content): add {description}`
- Modified content: `fix(content): update {description}`
- Style/CSS changes: `style: update {description}`
- Config/workflow changes: `chore(config): {description}`
- Mixed changes: `chore: sync changes`

If the user provided a commit message, use theirs instead.

### Step 4: Stage All Changes

```bash
git add -A
```

### Step 5: Commit

```bash
git commit -m "{generated_message}"
```

If the commit fails (nothing to commit), report this and stop.

### Step 6: Push to Main

```bash
git push origin main
```

### Step 7: Report Success

Report:
- Commit hash
- Commit message
- Files changed
- Push confirmation

## Error Handling

- If `git add` fails: report the error and stop
- If commit fails (nothing to commit): tell the user there's nothing to commit and stop
- If push fails (e.g., non-fast-forward): run `git pull origin main` first, then retry push
- If merge conflicts occur during pull: report them to the user and stop

## Safety Checks

- Never use `--force` or `-f` when pushing
- Never skip pre-commit hooks unless explicitly requested by the user
- Warn if committing large binary files (>5MB)
- Always confirm the branch is `main` before pushing
