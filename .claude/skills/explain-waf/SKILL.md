---
name: explain-waf
description: Live WAF/ALB triage assistant. Determines whether a blocked request was stopped by the WAF or the app, pulls the exact terminating rule and matched pattern from WAF logs, and checks whether the block is specific to that one request or reproducible for anyone hitting the same path. Read-only — never modifies WAF, ALB, or any AWS resource.
argument-hint: <optional: IP address and time window, e.g. "76.234.106.156 around 11:30-12:30 EST on 2026-07-31" — if omitted, Claude will ask what you're investigating>
---

## Safety rule — read this first

This skill is diagnose-only. You may ONLY run read-only AWS CLI calls:
`sts get-caller-identity`, `elbv2 describe-load-balancers`, `elbv2 describe-load-balancer-attributes`,
`wafv2 list-web-acls`, `wafv2 get-web-acl`, `wafv2 get-logging-configuration`, `s3 ls`, and `s3 sync`/`s3 cp`
reading *from* the log buckets into local scratch.

You must NEVER:
- Modify a WebACL, a rule, or an `override_action` (`aws wafv2 update-web-acl`, or any Terraform apply)
- Modify ALB, target group, or any other resource config
- Write to any S3 bucket other than local scratch
- Leave synced logs on disk after the investigation — ALB/WAF logs contain cookies, auth headers, and
  request bodies that can carry PII. Delete the local copies before finishing.
- Paste raw log lines (headers, cookies, full request bodies) into Slack/Confluence/tickets unsanitized

If the investigation concludes a WAF rule genuinely needs to change (an exemption, a scope-down statement,
or an `override_action` flip), stop and output it under a **Proposed Change (requires Terraform)** block:
what to change, why, and the blast radius. The user decides whether to open a PR — this skill does not
touch Terraform state or apply anything itself.

---

## Step 1: Ask the opening question

The user's context (if provided): $ARGUMENTS

If $ARGUMENTS is empty or vague, open with exactly this question before doing anything else:

> **What are you investigating?** Give me the client IP (or another way to identify the request), the
> approximate time window, and which environment(s) — prod, staging, or both. A vague symptom ("someone
> said they got a 403 around lunch") is fine too — I'll ask follow-ups to narrow it down.

Wait for the user's answer before proceeding.

---

## Step 2: Resolve AWS context and verify access

Identify (or ask for) the AWS SSO profile(s) for each environment in scope. Verify the session is live
before doing anything else — an expired SSO token fails loudly mid-investigation otherwise:

!`aws sts get-caller-identity 2>&1`

If it returns "Token has expired" for a profile you need, tell the user to run
`aws sso login --profile <name>` and wait for them before continuing.

If the user hasn't said which environment(s), ask. Default to checking both prod and staging only if
they genuinely don't know which one the traffic hit.

---

## Step 3: Convert the time window to UTC

ALB and WAF log S3 keys are partitioned in UTC. Convert whatever local time the user gave to a UTC hour
range — watch daylight saving (EDT vs EST depends on the date, not just the offset the user says). State
the conversion explicitly so the user can sanity-check it before anything gets synced.

---

## Step 4: Find the WAF-fronted ALB and its log locations

Don't hardcode ARNs, bucket names, or WebACL names — they drift over time. Discover them live, one
environment at a time:

```bash
aws elbv2 describe-load-balancers --profile <profile> --region us-east-1 \
  --query 'LoadBalancers[].{Name:LoadBalancerName,Type:Type,DNS:DNSName,Arn:LoadBalancerArn}' --output table
```

Skip `net` (NLB) entries — WAF only attaches to `app` (ALB) load balancers. If more than one ALB is a
plausible candidate, ask the user which domain/service the traffic hit rather than guessing.

Pull the access-log destination for the chosen ALB:

```bash
aws elbv2 describe-load-balancer-attributes --profile <profile> --region us-east-1 \
  --load-balancer-arn <arn> --query "Attributes[?contains(Key,'access_log')]"
```

Find the attached WebACL and its logging destination:

```bash
aws wafv2 list-web-acls --scope REGIONAL --profile <profile> --region us-east-1
aws wafv2 get-logging-configuration --resource-arn <webacl-arn> --profile <profile> --region us-east-1
```

While you're in there, also pull the WebACL's actual rule actions — don't trust the WebACL `Description`
field, it goes stale:

```bash
aws wafv2 get-web-acl --scope REGIONAL --name <name> --id <id> --profile <profile> --region us-east-1 \
  --query 'WebACL.Rules[].{Priority:Priority,Name:Name,Action:Action,Override:OverrideAction}'
```

---

## Step 5: Sync only the relevant hour(s)

ALB access log filenames embed the timestamp mid-name
(`..._<lb-id>_<TIMESTAMP>Z_<node-ip>_<rand>.log.gz`), so a date-level `s3 ls`/`s3 sync` prefix won't
narrow by hour on its own — filter with `--include`/`--exclude` glob matching on the `T<HH>` fragment.
WAF logs are hour-partitioned in the key path itself (`.../<yyyy>/<mm>/<dd>/<HH>/`).

Sync to a scratch directory (use the session scratchpad if one exists; otherwise a throwaway temp dir —
never the repo), and never sync more than the hour(s) actually needed:

```bash
aws s3 sync "s3://<alb-log-bucket>/AWSLogs/<account>/elasticloadbalancing/<region>/<yyyy>/<mm>/<dd>/" \
  <scratch>/alb/ --profile <profile> --exclude "*" --include "*_<yyyymmdd>T<HH>*"

aws s3 sync "s3://<waf-log-bucket>/AWSLogs/<account>/WAFLogs/<region>/<webacl-name>/<yyyy>/<mm>/<dd>/<HH>/" \
  <scratch>/waf/<HH>/ --profile <profile>
```

Repeat per UTC hour the window spans, and per environment in scope.

---

## Step 6: Classify — WAF or app?

Grep the synced ALB access logs for the client IP. In the ALB access log format (space-delimited, with
quoted fields for the request/user-agent/etc.), the fields that answer this question are:

- `elb_status_code` (field 9) — what the client received
- `target_status_code` (field 10) — what the backend actually returned, or `-` if it was never asked
- `actions_executed` (a later quoted field) — `"waf"` means the WAF terminated the request before any
  target group saw it

**If `target_status_code` is `-` and `actions_executed` is `"waf"`: the WAF blocked it, full stop — the
app never saw the request.** Continue to Step 7.

**If `target_status_code` holds a real value (e.g. `403`): the app itself returned that status.** Stop
here — this isn't a WAF question. Report the target group ARN, response time, and point the user at
application-level logs instead of continuing the WAF investigation.

---

## Step 7: Identify the exact rule and match

Grep the synced WAF JSON logs for the client IP, filter to non-`ALLOW` actions, and pull out per hit:

- `action`
- `terminatingRuleId` and `ruleGroupList[].terminatingRule.ruleId` — the specific rule and sub-rule
  (e.g. managed rule group `AWSManagedRulesCommonRuleSet`, sub-rule `CrossSiteScripting_BODY`)
- `terminatingRuleMatchDetails` — `conditionType`, `location`, and `matchedData`: the literal bytes that
  tripped the rule

Report this plainly to the user: which rule, which sub-rule, and exactly what matched. Don't stop at "the
WAF blocked it" — the specific matched string is almost always the key to whether this is a real threat
or a false positive.

---

## Step 8: Check whether it's IP-specific or content-specific

Before concluding "this IP/user is broken" or "this rule is broken," check the blast radius. Pull every
client IP hitting the *same URI(s)* in the *same window* from the WAF logs and tally ALLOW vs BLOCK per
IP.

- If other clients running the same workflow (same path, similar request size/content-type) are cleanly
  `ALLOW`ed, the block is almost certainly **content-dependent** — something specific in that one
  request's body, headers, or payload — not a problem with the user's account, session, or IP.
- If every client hitting that path gets blocked, the **rule itself** is the problem — a genuine
  false-positive on a legitimate path that warrants a scoped exemption.

This distinction changes the fix entirely: content-dependent blocks usually need no WAF change at all
(the user just needs to know what in their request tripped it); path-wide blocks need a scoped rule
exemption.

---

## Step 9: Synthesize, propose next steps if needed, and clean up

State plainly: WAF or app, which rule/sub-rule, what matched, and whether this is a one-off
(content-specific) or systemic (path-specific block affecting everyone). If this pattern matches a
previously-known false positive (an internal tool's request shape, embedded file metadata, etc.), say so.

If — and only if — the finding points to a genuine rule problem needing a fix, stop and output it under
a **Proposed Change (requires Terraform)** block: what to change (e.g. a scoped Allow rule, a
host/path-scoped exemption, an `override_action` flip), why, and what else that change could affect. Do
not run `aws wafv2 update-web-acl` or any Terraform apply yourself — the user decides whether to act on it.

**Before ending the investigation, always:**

```bash
rm -rf <scratch-dir>
```

Confirm out loud that the local log copies were deleted. They contain cookies, auth headers, and
potentially PII — they must not be left on disk or pasted anywhere unsanitized.
