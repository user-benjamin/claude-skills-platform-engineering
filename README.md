# platform-engineer-skills

A collection of [Claude Code skills](https://code.claude.com/docs/en/skills) purpose-built for platform engineers. The skills provide reusable workflows for infrastructure review, Kubernetes operations, observability, incident response, and engineering documentation.

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
.claude/skills/              ← Claude Code slash commands
    explain-k8s-error/       ← Kubernetes investigation
    gen-chart/               ← Helm/Kustomize generation
    gen-dashboard/           ← Grafana dashboard generation
    make-presentation/       ← Slidev presentation generation
    make-ticket/             ← Jira ticket generation
    pr-description/          ← Pull request descriptions
    project-proposal/        ← Project proposals
    review-terraform/        ← Terraform plan review
    write-adr/               ← Architecture decision records
    write-runbook/           ← Incident runbooks

templates/                  ← Shared output templates
scripts/lint-skills.py       ← Structural validation
.github/workflows/lint.yml   ← CI validation
```

Skills use Claude Code's `$ARGUMENTS`, live shell injection where needed, and
shared templates for structured output. The repository includes a structural
validator that checks skill metadata, required documentation, and template
references on every pull request.

**Browser-driven skills** drive a real Chrome tab (via the Claude in Chrome MCP)
so Claude can *see* a rendered UI and tune it with you — for example,
`gen-dashboard` checks a Grafana render. These need the browser extension and
MCP connected and declare their tools in `allowed-tools`. See
[`docs/browser-driven-skills.md`](docs/browser-driven-skills.md).

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

### Dependencies

The skills themselves do not require a separate runtime or package installation.
Browser-driven skills additionally require the Claude in Chrome extension and
MCP server; see [`docs/browser-driven-skills.md`](docs/browser-driven-skills.md).

## Usage

Once installed, invoke any skill from within Claude Code:

```
/write-adr "why we chose Karpenter over Cluster Autoscaler"
/review-terraform
/explain-k8s-error "OOMKilled on pod payments-7d9f"
/gen-chart "a nodejs api with HPA, PDB, and external secret"
/write-runbook "payments service p99 latency spike at 3pm"
/pr-description
/project-proposal "centralize platform observability"
/make-ticket "add a PDB to the payments service"
/make-presentation "infra prio and planning — k8s, waf status, neo migration, roadmap"
/gen-dashboard "payments-api nodejs"
```

## Skill Reference

See [`docs/`](docs/) for detailed documentation on each skill, including example output and configuration options.

## Contributing

Ideas for new skills go in [`WISHLIST.md`](WISHLIST.md). PRs welcome.
