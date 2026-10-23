# explain-waf

A live WAF/ALB triage assistant. Given a client IP and a time window, it works out whether a blocked
request was stopped by the WAF or by the application, pulls the exact terminating rule and matched
pattern out of the WAF logs, and checks whether the block is specific to that one request or reproducible
for anyone hitting the same path. Read-only — it never modifies WAF, ALB, or any other AWS resource.

## Usage

```
/explain-waf
```

Claude will ask what you're investigating, then take it from there.

Or give it a head start:

```
/explain-waf 76.234.106.156 around 11:30-12:30 EST on 2026-07-31
/explain-waf someone got a 403 on the admin panel around lunch today, prod
/explain-waf check both envs for 403s from 203.0.113.9 in the last hour
```

## What it does

1. **Verifies AWS access first** — checks the SSO session for the relevant profile(s) before syncing
   anything, so an expired token fails fast instead of mid-investigation.

2. **Discovers infrastructure live, never hardcoded** — finds the WAF-fronted ALB, its access-log bucket,
   and the attached WebACL's logging destination via `describe-load-balancers` /
   `describe-load-balancer-attributes` / `wafv2 get-logging-configuration`. Also reads the WebACL's actual
   rule actions rather than trusting its `Description` field, which is known to go stale.

3. **Syncs only the relevant hour(s)** of ALB access logs and WAF logs to local scratch — never a full
   day — after converting the given local time window to UTC (DST-aware).

4. **Classifies WAF vs. app** — the ALB access log's `target_status_code` and `actions_executed` fields
   tell you definitively whether the WAF terminated the request before any backend saw it, or whether the
   app itself returned the status code. If it's app-side, the skill stops and redirects you to
   application logs instead of chasing a WAF explanation that doesn't exist.

5. **Pulls the exact terminating rule** from the WAF JSON logs — the managed rule group, the specific
   sub-rule, and the literal matched string/location — not just "the WAF blocked it."

6. **Checks the blast radius** — compares against every other client hitting the same path in the same
   window. This is the difference between "this one request's content tripped a rule" (no WAF change
   needed) and "this rule blocks anyone on this legitimate path" (a real false positive needing a scoped
   exemption).

7. **Cleans up after itself** — always deletes the synced log copies before ending the investigation. ALB
   and WAF logs carry cookies, auth headers, and potentially PII; they don't get left on disk or pasted
   anywhere unsanitized.

## Safety

This skill only runs read-only AWS CLI calls (`describe-*`, `get-*`, `list-*`, `s3 ls`/`sync` reading from
log buckets). It never runs `wafv2 update-web-acl`, never touches Terraform state, and never applies a
change. If the investigation concludes a rule genuinely needs to change, that's surfaced as a **Proposed
Change (requires Terraform)** block — what to change and why — for the user to act on separately. The
skill diagnoses; it does not remediate.

## Audience

Built for infrastructure/platform engineers who own the WAF and ALB layer but not the application code —
someone who can read a WAF log and reason about a rule match, but who wants the cross-referencing (ALB
log vs. WAF log vs. other clients on the same path) done for them instead of by hand each time.
