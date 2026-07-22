---
name: gen-dashboard
description: Generates a Grafana dashboard JSON for a service (RED metrics — Rate, Errors, Duration — plus Kubernetes resource panels), then opens it in your browser as a final check and tunes it with you against the live render. Uses your logged-in Grafana session, so it works with SSO and picks up your real datasources.
argument-hint: <optional: service name and/or type, e.g. "payments-api nodejs">
allowed-tools: mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__tabs_create_mcp
---

The user wants a Grafana dashboard for a service. Their context (if provided): $ARGUMENTS

This skill has two halves: **generate** the dashboard JSON, then **look at it in the
browser** and tune it against what actually renders. See
`docs/browser-driven-skills.md` for the browser dependency and safety model.

## Safety rule — read this first

The browser phase is **read-only by default**: navigating, reading the page, and
screenshots are always fine. The following change state in Grafana and require an
**explicit "yes" from the user before you do them** — describe exactly what will
happen, then wait:

- Importing / saving a dashboard
- Overwriting an existing dashboard
- Deleting the scratch dashboard afterward

Never enter Grafana credentials yourself — the skill rides the session the user is
already logged into. On any cookie/consent banner, choose the privacy-preserving
option.

---

## Phase 1: Understand what to build

Read $ARGUMENTS for a service name and type. If either is missing or vague, ask
before generating anything:

> **What service is this dashboard for, and what does it run?**
> Give me the service name and roughly what it is — e.g. "payments-api, a Node.js
> HTTP service", "que-worker, a background job consumer", "checkout, a Go gRPC
> service". Also: does it expose Prometheus metrics already, and through what —
> a ServiceMonitor, an annotation-based scrape, or something else?

Then scan the repo for context — these are read-only:

!`find . -name "Chart.yaml" -o -name "values*.yaml" -o -name "servicemonitor*.yaml" -o -name "*dashboard*.json" 2>/dev/null | head -20`

Read anything found to infer: the service's `app`/`job` label, namespace, container
name, exposed ports, and whether an existing dashboard or naming convention already
exists to match. State what you found and what you're assuming:

> "I can see this deploys to namespace `payments` with label `app=payments-api` and
> a ServiceMonitor scraping `/metrics` on port `http`. I'll build panels keyed on
> `job=\"payments-api\"` / `namespace=\"payments\"`. Say if that's wrong."

Confirm the metric shape before generating. RED panels assume standard instrumentation
(e.g. `http_requests_total`, `http_request_duration_seconds_bucket`). If the service
uses different metric names, ask for them or adapt.

---

## Phase 2: Generate the dashboard JSON

Produce a **valid, importable** Grafana dashboard model and write it to disk
(default: `./<service>-dashboard.json` — confirm the path). Requirements:

- **RED method**, one row:
  - **Rate** — requests/sec, e.g. `sum(rate(http_requests_total{job="$service"}[5m]))`
  - **Errors** — error ratio, e.g.
    `sum(rate(http_requests_total{job="$service",status=~"5.."}[5m])) / sum(rate(http_requests_total{job="$service"}[5m]))`, unit `percentunit`
  - **Duration** — p50/p95/p99 from the histogram, e.g.
    `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="$service"}[5m])) by (le))`, unit `s`
- **Kubernetes resource** row: CPU usage vs requests/limits, memory working set vs
  limits, pod restarts (`kube_pod_container_status_restarts_total`), and ready replica
  count. Key these on the inferred namespace/label.
- **Datasource as an input**, so import lets the user pick their Prometheus. Include
  an `__inputs` entry of type `datasource` (e.g. `DS_PROMETHEUS`) and reference it as
  `"datasource": "${DS_PROMETHEUS}"` in every panel target. Do **not** hardcode a
  datasource UID.
- A `$service` (or `job`) **template variable** so the board is reusable, defaulted to
  the service you're building for.
- Sane `gridPos` layout (RED across the top, resources below), `title`, `tags`
  (include the service name), thresholds on the error and latency panels, and correct
  units. Sensible default time range (`now-6h`) and refresh (`30s`).

Show the user a short summary of the panels and their queries before moving on — not
the raw JSON dump.

---

## Phase 3: Final check in the browser

This is the point of the skill: verify the dashboard *renders* correctly rather than
shipping JSON blind.

### 3a. Preflight the browser

Call `tabs_context_mcp` (createIfEmpty: true). **If the browser tools are unavailable
or it errors:** do not abort. Tell the user the JSON is already written at its path,
and that the visual check needs the Claude in Chrome extension installed + signed in
(same account) and the `claude-in-chrome` MCP server connected to this session — then
they can re-run to do the check. Stop here in that case; the deliverable still stands.

### 3b. Get the target Grafana

Ask for the Grafana base URL if not already known:

> **What's your Grafana URL?** (e.g. `https://grafana.example.com`) I'll open it in
> the tab you're logged into — I won't enter any credentials.

Open a fresh tab (`tabs_create_mcp`) and `navigate` to it. Confirm you're logged in by
reading the page; if it shows a login screen, ask the user to sign in in that tab,
then continue.

### 3c. Import the dashboard (state change — confirm first)

Importing creates a dashboard in Grafana, so **ask before doing it**:

> "To render it I'll import this into Grafana — I'll drop it in a scratch folder
> (or one you name) so it's easy to clean up, select your Prometheus datasource when
> prompted, and I'll offer to delete it when we're done. OK to import?"

On a clear yes: navigate to `<grafana>/dashboard/import`, paste the JSON model into the
import textarea (locate it with `find` / `read_page`, set it with `form_input`), click
**Load**, pick the Prometheus datasource for the `DS_PROMETHEUS` input, choose the
folder, and confirm the import.

### 3d. Look at it and critique

Screenshot the rendered dashboard (`computer` → screenshot) and read the panels. Judge
against intent, and call out specifically:

- Any panel showing **"No data"** or a **query error** (usually a label/metric-name
  mismatch — the most common failure, and exactly what blind generation misses).
- Whether **units** render sensibly (percent, seconds, bytes) and axes aren't absurd.
- Whether **thresholds** on error/latency panels are placed usefully.
- **Titles, layout, and overlap** — does it read cleanly at a glance?

Report what you see plainly, tied to the render — "the p95 latency panel is `No data`;
the histogram metric is `http_server_duration_seconds_bucket`, not
`http_request_duration_seconds_bucket` — I'll fix the query."

### 3e. Tune together, iterate

Adjust the JSON on disk for each issue found, re-import (or re-upload the updated
model) and refresh, and re-screenshot until it's right. Keep the user in the loop on
each change. This is the "build better dashboards because Claude can actually look at
the thing" loop — expect a few passes.

### 3f. Clean up (state change — confirm first)

When done, offer to remove the scratch dashboard:

> "Want me to delete the scratch dashboard from Grafana? The finished JSON stays in
> your repo either way."

Only delete on an explicit yes.

---

## Phase 4: Deliver

- Confirm the final JSON path and that it's the tuned version that rendered cleanly.
- Summarize the panels, the datasource input, and the template variable.
- Note anything left for the user: metrics that weren't available to verify, queries
  assuming instrumentation you couldn't confirm, or panels that need real traffic to
  populate.
- The committed JSON is the deliverable — it should import cleanly into any Grafana
  with a matching Prometheus, not just the one you tested against.

---

## Tone and style

- Assume the user knows their service but not every Grafana/PromQL detail; explain
  query choices in a sentence when non-obvious.
- Tie every critique to what actually rendered, not generic dashboard theory.
- Be direct about uncertainty: "this panel needs real traffic to show anything — I
  can't verify it's correct from an idle service, only that the query is valid."
- Read-only until the user says yes to import/delete. Never assume approval.
