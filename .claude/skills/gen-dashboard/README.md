# gen-dashboard

Generate a Grafana dashboard for a service, then **look at it in the browser and tune
it** — instead of shipping dashboard JSON blind and hoping the panels render.

The first half is a generator: from a service name and type it writes an importable
dashboard model with RED panels (Rate, Errors, Duration) and Kubernetes resource
panels, keyed on labels it infers from your repo. The second half is the point of the
skill — it opens the dashboard in your logged-in Grafana, screenshots the render, and
iterates with you on anything that comes back wrong (a `No data` panel, a bad unit, a
label mismatch). That render-and-tune loop is only possible because of the browser
tooling; see [`docs/browser-driven-skills.md`](../../../docs/browser-driven-skills.md).

## Requirements

This is a **browser-driven skill**. The generate half works with just a shell, but the
final visual check needs:

- the Claude in Chrome extension installed and signed in with the same account, and
- the `claude-in-chrome` MCP server connected to your session.

If those aren't present the skill still writes the JSON and tells you how to enable the
check — it never throws away the generated dashboard. It uses your existing Grafana
session, so SSO-gated Grafana works and no datasource token or service account is
needed.

## Example invocation

```
/gen-dashboard "payments-api, a Node.js HTTP service"
/gen-dashboard          # will ask what the service is
```

## Example flow

1. **Asks / infers** — service name, type, metric source; scans the repo for the
   `app`/`job` label, namespace, and any existing dashboard to match.
2. **Generates** `payments-api-dashboard.json` — RED row on top, K8s resource row
   below, Prometheus as a selectable `${DS_PROMETHEUS}` input, a `$service` template
   variable, thresholds and units set.
3. **Asks for your Grafana URL**, opens it in a tab you're logged into.
4. **Asks before importing**, drops it in a scratch folder, then screenshots the
   render:
   > "The p95 latency panel shows `No data` — the histogram metric is
   > `http_server_duration_seconds_bucket`, not `http_request_duration_seconds_bucket`.
   > Fixing the query and re-importing."
5. **Iterates** until it renders cleanly, offers to delete the scratch dashboard, and
   leaves you the tuned JSON in the repo.

## Safety

Reading and screenshotting are read-only. Anything that changes Grafana — importing,
overwriting, or deleting a dashboard — stops for an explicit yes first. The skill never
enters your credentials.

## Phase 2 ideas

- Provision the finished dashboard as a ConfigMap/JSON for the Grafana sidecar (GitOps),
  not just a repo file.
- Support Loki log panels and alert-rule stubs alongside the metrics panels.
- Pull the service's actual metric names from a live `/metrics` scrape to key queries
  off real instrumentation instead of assumed names.
