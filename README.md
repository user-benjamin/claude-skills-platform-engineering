# platform-engineer-skills

A collection of [Claude Code skills](https://code.claude.com/docs/en/skills) purpose-built for platform engineers. Two layers: slash commands as the UX, Claude API agents as the engine for complex workflows.

## What's Inside

| Skill | Command | Description |
|---|---|---|
| Terraform Reviewer | `/review-terraform` | Reviews a terraform plan — categorizes changes as routine, worth reviewing, or destructive surprises (changes Terraform shows as updates but that actually destroy resources). Uses web search to verify provider-specific ForceNew behavior. |
| ADR Writer | `/write-adr` | Interviews you, then writes a fully populated Architecture Decision Record to `docs/adr/` |
| K8s Triage | `/explain-k8s-error` | Live cluster investigation — reads local Helm values, runs non-destructive kubectl commands, explains every finding with reasoning and docs links. Never takes destructive actions autonomously. |
| Chart Generator | `/gen-chart` | Generates a production-grade Helm chart or Kustomize manifests. Scans repo for context, asks before assuming, walks through component selection with caveats, then writes files to disk. |
| Runbook Writer | `/write-runbook` | Reviews the current debugging/incident session and distills it into a reusable runbook |
| PR Description | `/pr-description` | Combines live `git diff` with conversation context to write a PR description. Uses repo template if one exists, otherwise falls back to standard summary/problem/acceptance criteria/testing structure. |
| Project Proposal | `/project-proposal` | Generates a structured project proposal with executive summary, goals, metrics, timeline, risks, and stakeholders |
| Presentation Maker | `/make-presentation` | Creates a complete Slidev presentation from a topic outline — slides, speaker script, diagrams, real code examples — ready to `npm run dev` |

## Architecture

```
.claude/skills/          ← Claude Code slash commands (UX layer)
    review-terraform/
    write-adr/
    explain-k8s-error/
    gen-helm-chart/
    incident-runbook/
    pr-description/
    make-presentation/

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
git clone git@github.com:user-benjamin/claude-skills-platform-engineering.git
cd claude-skills-platform-engineering 

# Install skills and shared templates globally
cp -r .claude/skills/* ~/.claude/skills/
cp -r templates ~/.claude/templates/
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
/make-presentation "infra prio and planning — k8s, waf status, neo migration, roadmap"
```

## Skill Reference

See [`docs/`](docs/) for detailed documentation on each skill, including example output and configuration options.

## Contributing

Ideas for new skills go in [`WISHLIST.md`](WISHLIST.md). PRs welcome.
