# i-love-me

Collects your contributions to your team and company, month by month, so that at performance review
time you argue from evidence instead of memory. Each run crawls the work systems you've connected for
what you did since the last run, and files evidence-backed entries: what you did, what it measurably
changed, who it helped, and the ticket, PR, page or message that shows it. At review time it assembles
the binder into a self-assessment draft.

## Requirements

- At least one work source Claude can read: connectors such as Jira, Confluence, Slack, Linear, Notion
  or GitHub, or CLIs such as `gh`, `glab`, `aws`, `gcloud` or `az`. Use whatever you have; setup finds
  what's connected.
- Python 3 for the leak check (stdlib only).
- Optional: a **private** repo for an off-machine copy of the sanitized binder.

## Usage

```
/i-love-me                    # monthly update; runs setup the first time
/i-love-me since 2026-09-01   # update from a specific date
/i-love-me review             # self-assessment draft for a performance review
/i-love-me archive            # complete capture before your access to work systems changes
/i-love-me setup              # change sources, leak-check terms or the off-machine copy
```

## What it does

1. **Sets up once.** Finds the connectors and CLIs available in your session, asks which to use and
   for the identifiers each needs (orgs, cloud profile), your employer's domains for the leak check,
   and whether you want an off-machine copy. Saves this to `~/Documents/i-love-me/config.json`, which
   never leaves your machine.
2. **Crawls the window** since the last run: tickets, docs, PRs and reviews, chat, incidents, Claude
   memory notes, and cloud cost once a month has closed. It looks specifically for the work that
   doesn't close tickets (code reviews, unblocking teammates, onboarding, on-call), because that is
   most of what "contribution to the team" means in a review.
3. **Writes full entries locally**, grouped by initiative, with exact figures, ticket keys and notes on
   what's sensitive.
4. **Writes a sanitized copy** if you configured one, and runs `scripts/check_sanitized.py` over it
   until it comes back clean (account IDs, ARNs, tokens, IPs, internal URLs, emails, your denylist).
5. **Asks before saving.** Shows you the window, what was skipped, the strongest entries, and anything
   where your contribution or a figure needs your confirmation.

## Example output

A monthly run ends with a summary like this:

```
Window: 2026-09-01 to 2026-09-30 (Slack skipped: login expired)
3 new entries, 2 updates, 1 recognition quote.
Strongest: CI build time (-62%, cross-team); on-call handbook rewrite.
Needs your call: "Led the Postgres 16 upgrade". The cutover ticket is assigned to Sam.
  Led, or co-led with Sam?
```

And each entry looks like this (fictional):

```
### Cut CI build time for the monorepo
- **When:** 2026-08 to 2026-09
- **What I did:** Profiled the slowest CI jobs, moved dependency installs into a cached base image,
  and split the test suite into four parallel shards. Sam wrote the shard-balancing script.
- **Measured result:** median pipeline time 31m 40s to 12m 05s, 30 days of runs before and after
  (CI analytics). Measured.
- **Scope:** Cross-team
- **Evidence:** ENG-412, ENG-430, PR #1187, PR #1203, Slack #engineering, 2026-09-18
- **Tech:** GitHub Actions, Docker, pytest-xdist
- **Themes:** Delivery, Practices
- **Status:** VERIFIED
- **Summary sentence:** Cut median CI pipeline time 62% (32 to 12 minutes) for every team in the
  monorepo by caching dependencies and parallelizing tests.
```

The summary sentence is written to stand on its own, so it drops straight into a review form (or a
resume). The full entry format is in [`references/entry-format.md`](references/entry-format.md).

## Safety

- **Read-only in every source.** It never creates, edits, comments on, transitions or sends anything.
- **Honest by design.** Contribution is stated precisely ("helped build" is not "built"), results are
  measured or labeled as modeled, and "no metric found" is a valid answer.
- **Full detail stays on your machine.** The off-machine copy is optional, sanitized, leak-checked,
  pushed only to a repo confirmed private before every push, and only after you approve it.
- **Check your employer's policy** on keeping work records outside company systems before you turn on
  the off-machine copy. Local-only is a fully supported mode.

## Files

| Path | What it holds |
|---|---|
| `~/Documents/i-love-me/config.json` | Your sources, leak-check terms and off-machine copy settings |
| `~/Documents/i-love-me/STATE.json` | Last crawled date and a log of runs |
| `~/Documents/i-love-me/entries-<date>.md` | Full entries for each run |
| `~/Documents/i-love-me/denylist.txt` | Optional internal names for the leak check, one per line |
| `~/Documents/i-love-me/self-assessment-<date>.md` | Review mode output |
