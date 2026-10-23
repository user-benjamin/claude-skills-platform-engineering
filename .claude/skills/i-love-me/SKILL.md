---
name: i-love-me
description: A digital "I love me" binder for the user's work. Once a month it crawls whichever work systems the user has connected (issue tracker, docs and wiki, chat, code hosting, incident tools, cloud cost, Claude memory notes) for what they contributed to their team and company since the last run, and files evidence-backed entries of what they did, what it measurably changed, and who else contributed. At review time it assembles the binder into a self-assessment draft. Use this whenever the user wants to update their binder or brag doc, record recent wins, run the monthly binder update, prepare for a performance review or self-assessment, gather evidence for a promotion or compensation conversation, or capture their work record before their access to work systems changes, even if they don't name the skill.
argument-hint: "<optional: since YYYY-MM-DD | review | archive | setup>"
---

# i-love-me

i-love-me collects the user's contributions to their team and company, month by month, for performance reviews. Every entry records what they did, what it measurably changed, and the ticket, PR, page or message that shows it.

Most of that evidence lives in work systems that are only reachable from the user's work machine. The binder lives on that machine in full detail. Optionally, a sanitized copy goes to a private repo the user owns, so the record survives a laptop swap or a role change.

Arguments: $ARGUMENTS.

| Argument | What it does |
|---|---|
| (none) | Monthly update, from the day after `last_crawled` through today. Runs setup first if there is no config. |
| `since YYYY-MM-DD` | Update from that date |
| `review` | Assemble the binder into a self-assessment draft (see "Review mode") |
| `archive` | Complete capture of everything not yet in the binder, plus final values for open items, while access is current |
| `setup` | Rerun setup to change sources, leak-check terms or the off-machine copy |

## Ground rules

These exist because the first version of this binder overclaimed in about 15 places, and sensitive detail nearly left the laptop.

- **Read-only, everywhere.** Use only the search and read tools of any connector or CLI. Never create, edit, comment on, transition, react to, send or schedule anything. In local repos use read-only git commands only; the user's terminal may share those checkouts.
- **Never copy secrets** (keys, tokens, passwords, invite links), even when a source contains them.
- **The user is the actor, and contribution is stated precisely.** "Helped build" is not "built". "Member of the group that drove it" is not "drove". Following a procedure is not designing it. When others did part of the work, name their part; specifying work that a teammate builds is leadership evidence, so keep it.
- **Measured results only.** Use the final, corrected figure, never an estimate presented as a measurement. Label modeled numbers as modeled. If there is no number, write "no metric found".
- **Only sanitized content leaves the machine.** Account IDs, ARNs, hostnames, IPs, internal URLs, customer names, and anything describing a security weakness that is still open stay in the local file. Facts the company has published itself, such as case studies, are fine.
- **Employer policy comes first.** Some employers don't allow work records outside company systems, even sanitized ones. The off-machine copy is optional; if policy rules it out, run local-only.
- **The user approves before anything leaves the machine.** Show them the sanitized entries first.

## Paths

| What | Where |
|---|---|
| Local binder (full detail, stays on this machine) | `~/Documents/i-love-me/` |
| Config (local only; it names the employer's systems) | `~/Documents/i-love-me/config.json` |
| State | `~/Documents/i-love-me/STATE.json` |
| Local full entries | `~/Documents/i-love-me/entries-<run-date>.md` |
| Optional denylist of internal names | `~/Documents/i-love-me/denylist.txt` |
| Entry format | `references/entry-format.md` in this skill |
| Leak check | `scripts/check_sanitized.py` in this skill |
| Off-machine copy (optional) | Configured repo and branch, cloned fresh each run into the session scratchpad. Sanitized entries at `binder/entries/<run-date>.md`, state at `binder/STATE.json` |

## Setup (first run, or `setup`)

Run this when `config.json` is missing or the argument is `setup`. Ask one group at a time, and never guess a value.

1. **Identity.** The user's name as it appears in work systems, and their start date in their current role (the earliest date `archive` will crawl).
2. **Sources.** Find out what is reachable before asking about it:
   - Connectors: use ToolSearch to look for common work tools (for example `jira`, `confluence`, `linear`, `notion`, `slack`, `teams`, `github`, `gitlab`, `pagerduty`, `google drive`). Only note what exists; don't call anything yet.
   - CLIs: `command -v gh glab aws gcloud az`.

   Show what was found, grouped by the categories in step 2 of the update, and ask which to include. Get the identifiers each one needs: code-hosting orgs or groups, a cloud profile for cost, and the Claude memory path if it isn't the default. A tool that isn't listed here is fine if it has a read or search tool; ask what to pull from it.
3. **Leak-check terms.** The employer's domains (URLs on them get flagged), any email addresses allowed in the sanitized copy (every other address gets flagged), and optionally internal names for `denylist.txt` (customers, internal hostnames, codenames). The denylist stays local, because the list itself is sensitive.
4. **Off-machine copy.** Ask whether the user wants one. If they do, get the repo and branch, and confirm the repo is private: for GitHub, `gh repo view <owner/repo> --json visibility -q .visibility` must print `PRIVATE`; for any other host, ask the user. Never configure a public repo.
5. Write `config.json`, show it to the user, and confirm.

Example:

```json
{
  "name": "Alex Doe",
  "role_start": "2025-01-06",
  "sources": {
    "tracker": "jira",
    "docs": "confluence",
    "chat": "slack",
    "code": { "tool": "gh", "orgs": ["example-org"] },
    "incidents": null,
    "cost": { "tool": "aws", "profile": "billing-readonly" },
    "memory": "~/.claude/projects/*/memory/"
  },
  "leak_check": {
    "domains": ["example.com"],
    "allowed_emails": ["alex.doe@example.net"]
  },
  "offsite_copy": { "repo": "alexdoe/notes", "branch": "binder" }
}
```

## Update mode (default)

### 1. Get ready
1. Read `config.json`; run setup first if it's missing.
2. Check each configured source is reachable (`gh auth status`, or one cheap read call per connector). Note any that fail and carry on; one expired login doesn't stop the run.
3. If an off-machine copy is configured, clone only its branch into the scratchpad: `git clone --branch <branch> --single-branch <repo-url> <scratchpad>/binder-repo`. If the branch doesn't exist yet, clone the default branch and create it.
4. Read `STATE.json`. If it's missing locally but exists in the clone (a new machine), use that one. If there is no state anywhere, ask where to start, defaulting to the first day of the last full month. Tell the user the window in one line.
5. Skim the last two or three local entry files, so new entries continue existing threads instead of duplicating them.

### 2. Crawl the window
Pull from every configured source. Where a tool below matches, use its query, because these are known to work. For any other tool, read its search tool's description or `--help` before building a query, instead of guessing flags.

| Category | What to pull | Known-good queries |
|---|---|---|
| Issue tracker | Tickets resolved, created, or moved forward in the window. Read closing comments for measured results. | Jira: `(assignee = currentUser() OR reporter = currentUser()) AND updated >= "<start>"` |
| Docs and wiki | New pages and substantive updates: postmortems, ADRs, proposals, cost reviews, runbooks | Confluence: `contributor = currentUser() AND lastmodified >= "<start>"` |
| Code hosting | PRs merged, PRs opened, reviews given. Read PR bodies only where they carry the result. | GitHub: `gh search prs --author=@me --owner=<org> --merged-at=">=<start>"` (`--merged` is a yes/no flag and rejects dates), `--created=">=<start>"` for open work, and `--reviewed-by=@me --updated=">=<start>"` for reviews |
| Chat | The user's announcements, change notices and incident work. Recognition from others, as short verbatim quotes with author and date. Ignore bot and support-ticket channels. | Slack: the search tool's description states the logged-in user's ID; use it as `<ME>`. `from:<@ME> after:<start-1>` for the user's messages. For recognition, search `thanks` or `shoutout` with `with:<@ME>` (DMs and group DMs), plus a keyword search for the user's name with thanks in channels. Putting the mention in `filters` doesn't filter, so don't rely on it. |
| Incidents | Incidents the user responded to or led, and their write-ups | |
| Cloud cost | Only when a calendar month has closed since the last run, and only if cost is part of the user's role: monthly spend against prior months | AWS: Cost Explorer with the configured profile. It bills per API request, so stay under ~10 calls. If SSO has expired, ask the user to run `! aws sso login --profile <profile>` instead of retrying. |
| Claude memory notes | Notes modified in the window. They record corrected figures and outcomes. | Files under the configured memory path |

**Look for the work that doesn't close tickets.** Code reviews, unblocking someone in a thread, onboarding a new hire, interviews, on-call, a doc the team now relies on. That is most of what "contribution to the team" means in a review, and none of it shows up in a ticket count.

Scale the effort to the window. For about two weeks or less, crawl inline. For longer windows, or `archive`, fork one agent per source group (for example: tracker and docs; code and chat; incidents, cost and memory). Give each agent `references/entry-format.md` and the ground rules.

### 3. Write the local full entries
Write `~/Documents/i-love-me/entries-<run-date>.md` using the full format, with exact figures, ticket keys and sensitivity notes. This is the evidence trail. It stays on this machine.

### 4. Write the sanitized entries (off-machine copy only)
Skip this step and step 5 if no off-machine copy is configured. Otherwise write `binder/entries/<run-date>.md` in the clone, with these sections:
1. **Window and sources.** Dates, and which sources were crawled or skipped (and why).
2. **New entries.** Sanitized format, each with a one-sentence summary written to the conventions below.
3. **Updates to earlier entries.** Refreshed figures, status changes (in progress to done), new evidence.
4. **Recognition.** Quotes from others, with author role and date.
5. **Feedback and follow-through.** Feedback the user received in the window, and anything they did about earlier feedback.
6. **Nothing to report.** Say so plainly if the window was quiet. An empty run is a valid result.

Summary-sentence conventions: no em dashes; percentages to whole numbers; dollars rounded to the hundred or written as ~$X.XK. Write each sentence so it stands on its own outside the binder, on a review form or a resume. Keep exact figures in the evidence lines.

### 5. Check the sanitized file
Run `python3 -I <this skill>/scripts/check_sanitized.py <clone>/binder/entries/<run-date>.md`, adding `--domain <d>` for each configured domain, `--allow-email <e>` for each allowed email, and `--deny ~/Documents/i-love-me/denylist.txt` if that file exists. Fix every finding and rerun until it prints `CLEAN`. The script catches mechanical leaks (IDs, ARNs, tokens, IPs, internal URLs). Judgment leaks, like an open weakness described in plain words, are still on you, so reread the file once with that in mind.

### 6. Review with the user, then save
Show the user a short summary: the window, sources skipped, how many new entries and updates, the strongest two or three, and anything that needs their confirmation (actor, figures, framing). Ask whether to save, and push if an off-machine copy is configured. On approval:
1. Update `STATE.json`: set `last_crawled` to the window end and append a run record `{date, window, sources, new_entries, updates, pushed}`.
2. If an off-machine copy is configured: recheck that the repo is still private (as in setup), copy `STATE.json` to `binder/STATE.json`, commit only `binder/` with a message like `Binder: <start> to <end>`, ending with the attribution trailer the session specifies, and push the branch.
3. Verify with `git ls-remote --heads origin <branch>` and tell the user the commit.

If the user declines or wants changes, edit and recheck. Don't advance `last_crawled` for a window the user didn't approve.

## Review mode (`review`)
Run this when a performance review or self-assessment is due.
1. Ask the user for the review period, and for the review template or competency list if there is one. Otherwise use the structure of their last review if they share it, or: summary, strengths, areas for improvement and what they did about them, key accomplishments, goals.
2. Run an update first if `last_crawled` is more than a week old, so the binder is current.
3. Read every local full entry in the period (`~/Documents/i-love-me/entries-*.md`). They have exact figures, and this draft stays on the work machine, so detail is fine here.
4. Write `~/Documents/i-love-me/self-assessment-<date>.md`:
   - accomplishments grouped by competency, each with its measured result, its scope (team, cross-team, company) and an evidence link
   - recognition quotes
   - feedback received and the concrete change made in response
   - a short list of goals for the next period that the evidence supports
5. Apply the same honesty rules: precise contribution, measured results only, no overclaiming. A self-assessment that overstates gets caught by the manager who was there.

## Archive mode (`archive`)
Run this when access is about to change: a reorg, a role change, a laptop swap.
- Crawl from `last_crawled`, or from `role_start` if the binder was neglected, using agents.
- Also capture the latest performance review and written feedback (summary only) if the user can share them, and final values for everything still in progress.
- If a calendar month has closed, capture the last full month of cost data.
- Save through the normal review-and-approve step.
