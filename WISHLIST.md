# Skill Wishlist

Ideas and vague executions for skills not yet built. Anyone can pick these up.
Add your own ideas — no implementation required to add to this list.

---

## External Skills and Integrations

These are useful external projects and integration ideas to evaluate or adapt into
native Claude Code skills. Prefer read-only workflows and explicit approval before
allowing any agent to mutate AWS, Kubernetes, or GitHub state.

### AWS and EKS

**AWS Agent Toolkit for AWS** — <https://github.com/aws/agent-toolkit-for-aws>

AWS-maintained skills, plugins, and MCP servers covering service selection, CDK,
CloudFormation, containers, EKS, IAM, observability, billing, and AWS
Documentation. Evaluate the AWS-specific guidance and identify reusable patterns
for `/aws-review`, `/eks-triage`, and `/aws-docs`.

**AWS APEX Skills** — <https://github.com/aws-samples/sample-apex-skills>

Platform-engineering workflows for EKS, golden paths, Backstage, GitOps,
progressive delivery, multi-tenancy, ACK/KRO, AI/ML platform paths, and DORA
metrics. Strong candidate for a `/design-platform` or `/eks-platform-plan` skill.

**Amazon EKS MCP Server** — <https://github.com/awslabs/mcp/tree/main/src/eks-mcp-server>

Provides live EKS and Kubernetes context for resource inspection, logs, events,
deployment troubleshooting, manifest generation, and cluster workflows. Evaluate
as an optional read-only integration for `/explain-k8s-error` and `/k8s-debug`.

**AWS MCP collection** — <https://github.com/awslabs/mcp>

Includes AWS API and AWS Documentation MCP servers plus integrations for EKS,
ECS, ECR/Finch, and other services. Investigate a guarded `/aws-investigate`
workflow with account, region, and mutation boundaries.

### Kubernetes

**kubectl-ai** — <https://github.com/GoogleCloudPlatform/kubectl-ai/>

Natural-language Kubernetes assistance with support for Bedrock, hosted models,
and local models. Evaluate command-generation and evidence-gathering patterns,
without granting autonomous destructive access.

**kubectl MCP Server** — <https://github.com/rohitg00/kubectl-mcp-server/>

Kubernetes MCP tools and packaged skills for core resources, networking, storage,
deployments, operations, security, Helm, and troubleshooting. Compare its
workflows with the existing `/explain-k8s-error` skill.

**kagent** — <https://kagent.dev/>

Kubernetes-native runtime for governed agents using CRDs, GitOps, RBAC, MCP,
A2A, OpenTelemetry, and human-in-the-loop approvals. Consider a future skill for
designing or reviewing an in-cluster agent platform.

### Platform Engineering

**Platform Skills** — <https://github.com/nitinjain999/platform-skills>

A broad platform-engineering handbook covering Kubernetes, AWS, Terraform, Helm,
Argo CD, Flux, GitHub Actions, OPA/Rego, Karpenter, KEDA, supply-chain security,
Falco, and observability. Review its preflight, platform-review, incident-debug,
and deployment-hardening workflows for ideas to add here.

### GitHub

**Official GitHub MCP Server** — <https://github.com/github/github-mcp-server/>

GitHub-maintained integration for repository contents, code search, issues, pull
requests, reviews, and Actions metadata. Potential uses include `/review-pr`,
`/environment-drift`, `/github-actions-audit`, and `/onboard-service`.

### Suggested Build Order

1. Add a read-only `/eks-investigate` mode to the existing Kubernetes triage flow.
2. Add `/review-platform-change` for Terraform, Helm, Kubernetes, and GitHub Actions.
3. Add `/environment-drift` to compare Git, AWS, and cluster state without mutation.
4. Add `/onboard-service` with an EKS golden path, GitHub Actions, Helm, GitOps,
   IAM/OIDC, observability, and rollback artifacts.
5. Add approval-gated mutation only after dry-run, audit, and rollback behavior is
   well-defined.

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

> `/gen-dashboard` — ✅ built (see the root README). Generates the dashboard *and*
> renders it in your browser to tune against live data.

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
