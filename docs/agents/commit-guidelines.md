# Commit guidelines

## Cadence

- Commit each coherent milestone after its focused checks pass. Prefer a sequence of small, independently understandable commits over one large end-of-task commit.
- Keep each commit focused on one purpose. Split changes with different purposes into separate commits when practical; avoid commits that only divide trivial edits.
- Before staging, inspect `git status` and the diff. Stage only changes made for the task; preserve unrelated or user-owned changes and never include them in a commit.
- If a milestone cannot be validated, do not present it as verified; explain the limitation before committing it.

## Message format

Every commit message MUST follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- Use `feat` for a new feature and `fix` for a bug fix. Other accurate types such as `docs`, `test`, `refactor`, `build`, and `chore` are allowed.
- Use a concise, lowercase type; add a lowercase scope in parentheses when it usefully identifies the affected area.
- Write a short, specific description after the colon. Use the imperative mood, for example, `fix(grid): reject empty dimensions`.
- Add a body only when it clarifies context or reasoning not apparent from the description. Separate it from the description with a blank line.
- Mark a breaking change with `!` immediately before the colon, and describe the change in the description or with a `BREAKING CHANGE: <description>` footer. A breaking-change footer may also be used without `!`.
- Put footers after a blank line. Use the Conventional Commits footer syntax, such as `Refs: #123`.

Examples:

```text
feat(recipe): preserve declared operation order
fix(grid): reject empty dimensions
docs(agents): define commit guidelines
refactor!: remove the legacy recipe format

BREAKING CHANGE: recipe declarations must use the ordered format.
```
