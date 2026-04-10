# Skill Wishlist

Ideas and vague executions for skills not yet built. Anyone can pick these up.
Add your own ideas — no implementation required to add to this list.

---

## Platform Engineering

**`/onboard-service`**
Given a service name and type (e.g. "payments-api, nodejs"), scaffold everything needed to run it on the platform: Helm chart, GHA workflow, ADR stub, namespace, basic dashboards. The "golden path" in a single command.

**`/cost-estimate`**
Analyze a `terraform plan` and estimate the monthly AWS cost delta. Flag expensive surprises (NAT gateways, data transfer, oversized RDS).

**`/migrate-terraform`**
Help migrate between Terraform versions or provider versions. Reads current state, identifies breaking changes, suggests `moved` blocks and updated syntax.

**`/gen-github-action`**
Describe a CI workflow in plain English, get a production-grade `.github/workflows/` YAML with caching, OIDC auth, and sane defaults.

---

## Kubernetes

**`/k8s-debug`**
Interactive pod debugging assistant. Runs `kubectl describe`, `logs`, and `events` in sequence, interprets the output, and suggests next steps. Like a rubber duck that knows Kubernetes.

**`/compliance-check`**
Check K8s manifests against CIS Kubernetes Benchmark controls. Returns a prioritized list of violations with remediation snippets.

**`/capacity-plan`**
Given current resource requests/limits and growth projections, recommend node pool sizing and Karpenter configuration.

**`/network-policy-gen`**
Given a description of a service and its dependencies, generate a `NetworkPolicy` that enforces least-privilege traffic rules.

---

## Observability

**`/gen-dashboard`**
Generate a Grafana dashboard JSON from a service description. Includes RED metrics (Rate, Errors, Duration) and K8s resource panels.

**`/alert-rules`**
Generate Prometheus alerting rules for a given service type. Includes severity levels, annotations, and runbook links.

**`/log-query`**
Describe what you're looking for in plain English, get a LogQL query for Loki.

---

## Security

**`/security-scan`**
Run `checkov` and `tfsec` against current Terraform, interpret the findings, prioritize by severity, and suggest fixes.

**`/iam-audit`**
Analyze an IAM policy or role and flag overly permissive statements. Suggest least-privilege replacements.

**`/secret-rotation-plan`**
Given a secret name and service, generate a zero-downtime rotation runbook.

---

## Incident Response

**`/post-mortem`**
Generate a blameless post-mortem template pre-populated from an incident description. Includes timeline, contributing factors, and action items sections.

**`/blast-radius`**
Given a proposed change (Terraform plan, Helm upgrade, config change), reason about the potential blast radius and rollback strategy.

---

## Developer Experience

**`/changelog`**
Generate a `CHANGELOG.md` entry from `git log` since the last tag. Categorizes commits into features, fixes, and breaking changes.

**`/review-pr`**
Review an open PR for a platform engineering lens — security, cost, reliability, and operability concerns beyond just code correctness.

**`/doc-module`**
Generate a README for a Terraform module from its `variables.tf` and `outputs.tf`.
