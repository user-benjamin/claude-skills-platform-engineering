# claude-skills-platform-engineering

A collection of [Claude Code skills](https://code.claude.com/docs/en/skills) purpose-built for platform engineers. Every skill today is a slash command driven by live shell injection — no dependencies, just Claude. A Claude API agent layer for complex multi-step workflows is planned; see [Roadmap](#roadmap).

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
| Dashboard Generator | `/gen-dashboard` | Generates a Grafana dashboard (RED metrics + K8s resource panels) for a service, then opens it in your logged-in Grafana and tunes it against the live render. First browser-driven skill — needs the Claude in Chrome MCP for the visual check. |

## Architecture

```
.claude/skills/          ← Claude Code slash commands (UX layer)
    review-terraform/
    write-adr/
    explain-k8s-error/
    gen-chart/
    write-runbook/
    make-ticket/
    pr-description/
    project-proposal/
    make-presentation/

templates/               ← shared output templates, referenced by skills
    adr.md
    jira-ticket.md
    project-proposal.md
    pull-request.md
    runbook.md
    presentation.md
```

Every skill uses live shell injection (`` !`command` ``) and `$ARGUMENTS` — no dependencies, just Claude. Skills that produce structured output pull their format from a shared file in `templates/` via `` !`cat ~/.claude/templates/<name>.md` ``, keeping templates centralized and independently editable.

**Browser-driven skills** drive a real Chrome tab (via the Claude in Chrome MCP) so Claude can *see* a rendered UI and tune it with you — e.g. `gen-dashboard` checking a Grafana render. These need the browser extension + MCP connected and declare their tools in `allowed-tools`. See [`docs/browser-driven-skills.md`](docs/browser-driven-skills.md).

## Installation

### All skills (recommended)

```bash
git clone git@github.com:user-benjamin/claude-skills-platform-engineering.git
cd claude-skills-platform-engineering 

# Install skills and shared templates globally
mkdir -p ~/.claude/skills ~/.claude/templates
cp -r .claude/skills/* ~/.claude/skills/
cp -r templates/* ~/.claude/templates/
```

> **Note:** copy the *contents* of `templates/` (`templates/*`) into `~/.claude/templates/`, not the directory itself. `cp -r templates ~/.claude/templates/` nests it as `~/.claude/templates/templates/` when the destination already exists, and the skills' `` !`cat ~/.claude/templates/<name>.md` `` lookups will silently come back empty.

### Single skill

```bash
cp -r .claude/skills/write-adr ~/.claude/skills/
# plus any template that skill references, e.g.:
cp templates/adr.md ~/.claude/templates/
```

## Usage

Once installed, invoke any skill from within Claude Code:

```
/write-adr "why we chose Karpenter over Cluster Autoscaler"
/review-terraform
/explain-k8s-error "OOMKilled on pod payments-7d9f"
/gen-chart "a nodejs api with HPA, PDB, and external secret"
/write-runbook "payments service p99 latency spike at 3pm"
/pr-description
/make-presentation "infra prio and planning — k8s, waf status, neo migration, roadmap"
```

## Skill Reference

Each skill has a `README.md` in its own directory (`.claude/skills/<skill>/README.md`) covering what it does, an example invocation, and example output.

## Roadmap

A planned `agents/` layer would let complex skills shell out to Python scripts that call the Claude API directly for structured, multi-step output, rather than relying on shell injection alone:

```
agents/                  ← Claude API agents (planned — not yet implemented)
    terraform_reviewer.py
    adr_writer.py
    runbook_generator.py
```

This would add a dependency (`pip install anthropic` and an `ANTHROPIC_API_KEY`) for the skills that use it. Not yet built — proposals welcome in [`WISHLIST.md`](WISHLIST.md).

## Contributing

Ideas for new skills go in [`WISHLIST.md`](WISHLIST.md). PRs welcome.
