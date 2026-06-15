# Contributing

Contributions are welcome — new skills, improved templates, bug fixes, or
additions to the wishlist. Here's how to do it well.

## Getting Started

```bash
git clone https://github.com/user-benjamin/claude-skills-platform-engineering
cd claude-skills-platform-engineering
git checkout -b feat/your-skill-name
```

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir -p .claude/skills/your-skill-name
```

### 2. Write SKILL.md

Every skill needs a `SKILL.md` with frontmatter. At minimum:

```markdown
---
name: your-skill-name
description: One-line description — Claude uses this to decide when to load the skill.
argument-hint: <what the user should pass>
---

Instructions for Claude...
```

See [Claude Code skill docs](https://code.claude.com/docs/en/skills) for all
available frontmatter fields (`allowed-tools`, `context: fork`,
`disable-model-invocation`, etc.).

### 3. Use shared templates

If your skill produces structured output, add a template to `templates/` rather
than embedding it inline. Skills reference templates via shell injection:

```markdown
!`cat ~/.claude/templates/your-template.md`
```

This keeps templates centralized and independently editable.

### 4. Add a README.md to the skill directory

Cover: what the skill does, example invocation, example output, and any
Phase 2 plans (e.g. API integration).

### 5. Update the root README

Add your skill to the table in `README.md`.

---

## Skill Quality Bar

Before submitting a PR, check:

- [ ] Skill works end-to-end — test it with `cp -r .claude/skills/your-skill ~/.claude/skills/`
- [ ] Output is immediately usable, not a starting point that needs heavy editing
- [ ] Template (if any) is in `templates/`, not embedded in `SKILL.md`
- [ ] `README.md` includes at least one example invocation
- [ ] Root `README.md` table is updated

## Proposing a New Skill (without building it)

Add it to `WISHLIST.md` with a name, one-line description, and rough notes on
what the output should look like. No implementation required.

## Branch & PR Rules

- Branch off `main`, name your branch `feat/<skill-name>` or `fix/<what>`
- One skill (or related set of changes) per PR
- PRs require at least one approving review before merge
- All checks must pass before merge
- Direct pushes to `main` are not permitted

## Commit Style

Short, imperative subject line. Reference what changed and why:

```
Add /explain-k8s-error skill

Pastes a K8s error and gets root cause + fix. Uses context:fork so
the investigation runs in an isolated subagent.
```
