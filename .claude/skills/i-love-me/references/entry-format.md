# Binder entry format

Group entries by **initiative**, not by ticket. Tickets, PRs and pages are the evidence for an initiative. When an entry continues an earlier one, say so in the title. Smaller contributions that don't belong to an initiative (a review that caught a bug, an afternoon unblocking a teammate) go together in one "Team support" entry for the month, so they're recorded without flooding the binder.

## Full entry (local file only)

```
### <Initiative title>  [continues: <earlier entry title>, if any]
- **When:** YYYY-MM to YYYY-MM | ongoing
- **What I did:** 1-3 sentences of concrete actions. Name others' parts.
- **Measured result:** exact numbers with units and source, or "no metric found". Mark modeled vs measured.
- **Scope:** Team | Cross-team | Company (the widest the evidence supports)
- **Evidence:** ticket keys, PR numbers, doc page IDs or titles, chat channel and date, queries used
- **Tech:** comma-separated list
- **Themes:** Delivery | Reliability | Security | Cost | Leadership | Practices (pick all that apply)
- **Status:** VERIFIED | IN PROGRESS | UNVERIFIED
- **Sensitivity:** what must not leave this machine (open weaknesses, IDs, hostnames, customer names), or "clean"
- **Summary sentence:** one sentence, written to the conventions in SKILL.md
```

Scope means who the work helped. Team is the user's own team. Cross-team is other teams in engineering or the wider org. Company is customers, revenue, cost, or compliance at the company level.

## Sanitized entry (off-machine copy)

Same as the full entry, with these changes:
- **Drop** the Sensitivity field. Its contents are the sensitive part.
- **Evidence** keeps ticket keys, PR numbers and doc page IDs, but no URLs: "Slack #engineering, 2026-10-16", not a permalink.
- **Remove** anything the Sensitivity note flagged. If that guts the entry, keep a one-line generic version, or leave the entry local-only.
