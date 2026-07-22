# Browser-driven skills

A third category of skill, alongside the two in the root README:

- **Simple skills** — shell injection (`` !`command` ``) + `$ARGUMENTS`. No dependencies, just Claude and your shell.
- **Complex skills** — shell out to a Python agent in `agents/` that calls the Claude API.
- **Browser-driven skills** *(this doc)* — drive a real Chrome tab so Claude can *see* a rendered UI and iterate on it visually.

Some platform work can't be verified from a terminal. You can generate a Grafana
dashboard's JSON, a rendered runbook, or a deployed web page's markup blind — but
you can't tell whether the panels actually plot data, whether the layout is sane,
or whether a query returns "No data" until something *renders* it. Browser-driven
skills close that loop: Claude opens the thing in your browser, looks at it, and
tunes it with you.

## The dependency (read this before authoring one)

Every other skill in this repo needs nothing beyond your shell. Browser-driven
skills need the **Claude in Chrome** MCP server, which drives Chrome through the
browser extension. That means, at runtime:

1. The Claude in Chrome extension is installed and signed in with the same account
   as your Claude Code / Cowork session
   (<https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn>).
2. The MCP server is registered with your session, so its tools are available.

If either is missing, the browser tools simply aren't there. A browser-driven
skill must detect that and degrade gracefully (see *Preflight* below) rather than
dying halfway through and losing the user's work.

### Why a browser and not an API/token

- **Rides your authenticated session.** It sees Grafana (or any SSO-gated console)
  exactly as you're already logged in — no separate service account, API token, or
  datasource credential to provision. This is the whole reason the approach works
  where a token-based generator can't.
- **Sees what a human sees.** Rendered panels, real values, error states — not just
  the JSON model you *hope* renders correctly.

Trade-offs: it's interactive and slower than a one-shot generator, and it needs a
live browser session. Use it for the *verification / tuning* phase, not for
bulk generation.

## Tool declaration convention

Declare the browser tools the skill uses in the `allowed-tools` frontmatter field.
This makes the skill's surface explicit and lets it fail closed if the tools
aren't granted, instead of reaching for capabilities the user didn't expect.

```markdown
---
name: your-browser-skill
description: One-line trigger description.
argument-hint: <what the user passes>
allowed-tools: mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__tabs_create_mcp
---
```

The exact prefix depends on the name the MCP server is registered under. The
default is `claude-in-chrome`, giving tools named `mcp__claude-in-chrome__<tool>`.
If you registered the server under a different name, adjust the prefix to match.

### Core tools

| Tool | Use |
|---|---|
| `tabs_context_mcp` | List the session's tabs / create the group. **Call first** — it's also the preflight probe. |
| `tabs_create_mcp` | Open a fresh tab for the task (don't reuse the user's tabs). |
| `navigate` | Go to a URL, or `back`/`forward`. |
| `get_page_text` | Extract readable text — good for articles, JSON, plain pages. |
| `read_page` | Accessibility tree with element refs — use to locate inputs/buttons. |
| `find` | Natural-language element lookup, returns refs. |
| `form_input` | Set a value in an input/textarea by ref. |
| `computer` | Screenshot, click, type, scroll — for anything visual or not addressable by ref. |

## Preflight and graceful degradation (required)

Before the skill needs the browser, probe for it and handle absence:

```
1. Call tabs_context_mcp (createIfEmpty: true).
2. If it errors / the tools aren't available:
     - Do NOT abort the whole skill.
     - Deliver any non-browser artifact already produced (e.g. the generated JSON).
     - Tell the user exactly how to enable the browser step:
         • install + sign into the Claude in Chrome extension (same account), and
         • ensure the claude-in-chrome MCP server is connected to this session,
       then re-run the skill (or just the verification phase).
3. If it succeeds: proceed with the browser phase.
```

The rule: the browser is an *enhancement* to the deliverable, never a single point
of failure that discards work already done.

## Safety

- **Reading is safe.** `navigate`, `get_page_text`, `read_page`, `find`, and
  screenshots are read-only — do them freely.
- **State changes need an explicit yes.** Anything that mutates the target system —
  saving/importing a dashboard, clicking Submit / Save / Delete / Confirm, accepting
  a consent banner, granting OAuth — is a per-action confirmation. Describe exactly
  what will happen and wait for a clear "yes" before doing it. Mirror the
  `explain-k8s-error` pattern: keep the loop read-only, and surface any mutating
  action for the user to approve.
- **Privacy.** Prefer the privacy-preserving option on cookie/consent popups. Never
  enter credentials, tokens, or card details on the user's behalf — that's always
  the user's to do.

## Authoring checklist

- [ ] `allowed-tools` lists exactly the browser tools the skill uses
- [ ] Preflight probe (`tabs_context_mcp`) runs before the browser is needed
- [ ] Graceful degradation path delivers the non-browser artifact if tools are absent
- [ ] Every state-changing action stops for explicit user confirmation
- [ ] The final deliverable is a durable artifact (file / committed JSON), not just
      the on-screen result
