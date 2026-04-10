# platform-engineer-skills

A collection of [Claude Code skills](https://code.claude.com/docs/en/skills) purpose-built for platform engineers. Two layers: slash commands as the UX, Claude API agents as the engine for complex workflows.

## What's Inside

| Skill | Command | Description |
|---|---|---|
| Terraform Reviewer | `/review-terraform` | Injects live `terraform plan` output, reviews for security issues, cost gotchas, and missing tags |
| ADR Writer | `/write-adr` | Interviews you, then writes a fully populated Architecture Decision Record to `docs/adr/` |
| K8s Error Explainer | `/explain-k8s-error` | Paste a Kubernetes error, get root cause + fix |
| Helm Chart Generator | `/gen-helm-chart` | Scaffolds a production-grade Helm chart from a plain-English description |
| Incident Runbook | `/incident-runbook` | Generates a runbook from an alert or incident description — symptoms, causes, steps, escalation |
| PR Description | `/pr-description` | Reads your live `git diff` and writes the PR body for you |

## Architecture

```
.claude/skills/          ← Claude Code slash commands (UX layer)
    review-terraform/
    write-adr/
    explain-k8s-error/
    gen-helm-chart/
    incident-runbook/
    pr-description/

agents/                  ← Claude API agents (engine for complex skills)
    terraform_reviewer.py
    adr_writer.py
    runbook_generator.py
```

**Simple skills** use live shell injection (`` !`command` ``) and `$ARGUMENTS` — no dependencies, just Claude.

**Complex skills** shell out to `agents/` Python scripts that call the Claude API directly for structured, multi-step output.

## Installation

### All skills (recommended)

```bash
git clone https://github.com/your-username/platform-engineer-skills
cd platform-engineer-skills

# Install skills globally (available in all projects)
cp -r .claude/skills/* ~/.claude/skills/
```

### Single skill

```bash
cp -r .claude/skills/write-adr ~/.claude/skills/
```

### Agent dependencies (for complex skills)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
```

## Usage

Once installed, invoke any skill from within Claude Code:

```
/write-adr "why we chose Karpenter over Cluster Autoscaler"
/review-terraform
/explain-k8s-error "OOMKilled on pod payments-7d9f"
/gen-helm-chart "a nodejs api with HPA, PDB, and external secret"
/incident-runbook "payments service p99 latency spike at 3pm"
/pr-description
```

## Skill Reference

See [`docs/`](docs/) for detailed documentation on each skill, including example output and configuration options.

## Contributing

Ideas for new skills go in [`WISHLIST.md`](WISHLIST.md). PRs welcome.
