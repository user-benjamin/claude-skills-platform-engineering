---
name: make-ticket
description: Generate a structured Jira ticket from a plain-English description. Produces a fully populated ticket with priority, summary, desired outcome, acceptance criteria, testing methodology, rollout plan, and incidental notes.
argument-hint: <describe the problem or feature in plain English>
---

The user wants to create a Jira ticket. Their input is: $ARGUMENTS

Generate a complete, production-quality Jira ticket using the template below.

## Instructions

**Priority:** Infer from the user's description using these guidelines:
- **Critical** — production is down or at risk, data loss possible, security vulnerability
- **High** — significant user or platform impact, no workaround, blocking other work
- **Medium** — meaningful impact but a workaround exists, planned improvement
- **Low** — nice to have, minor polish, non-urgent tech debt

**Summary:** Describe the problem or need clearly and specifically. If the user's input is vague, make reasonable inferences but note any assumptions you've made.

**Desired Outcome:** Paint the end-state picture. Focus on what changes for the better — for users, for the platform, for the team operating it.

**Acceptance Criteria:** Write 3–5 specific, binary, testable items in Given/When/Then format where applicable. These should be things a reviewer can check without asking the author.

**Testing Methodology:** Write step-by-step instructions a separate engineer can follow to validate the change. Include commands where you can infer them from context.

**Rollout Plan:** Infer the safest rollout strategy from the nature of the change:
- Infrastructure changes → canary or blue/green
- Config changes → direct with rollback steps
- New features → feature-flagged where possible
Always include a rollback procedure.

**Incidental:** Note any obvious dependencies, related concerns, or follow-up work that the user's description implies — even if they didn't mention it explicitly.

## Template

Use this exact template structure:

!`cat ~/.claude/templates/jira-ticket.md`

## Output

Write the completed ticket as a markdown code block so it can be copied directly into Jira. After the ticket, add a brief **Notes** section with any assumptions you made or clarifying questions the user should answer before filing.
