"""Mechanical leak check for a sanitized binder entry file.

Usage: check_sanitized.py FILE [--domain DOMAIN ...] [--allow-email EMAIL ...] [--deny DENYLIST]
Prints each finding as LINE:KIND:MATCH and exits 1, or prints CLEAN and exits 0.
--domain adds an employer domain (e.g. example.com) to the internal-URL check;
repeat it per domain. Every email address is flagged unless passed with
--allow-email. The denylist is a local text file, one case-insensitive term per
line (internal hostnames, customer names); keep it off the repo since the list
itself is sensitive.
"""
import argparse
import re
import sys

ALLOWED_EMAILS = {"noreply@anthropic.com"}
# Work-tool hosts whose URLs always point inside someone's workspace.
INTERNAL_HOSTS = [
    "slack.com", "atlassian.net", "notion.so", "linear.app", "docs.google.com",
    "drive.google.com", "pagerduty.com", "incident.io", "teams.microsoft.com", "sharepoint.com",
]

PATTERNS = [
    ("aws-account-id", re.compile(r"(?<![\d.])\d{12}(?![\d.])")),
    ("arn", re.compile(r"\barn:aws[a-z-]*:", re.I)),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]+")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("ipv4", re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")),
    ("aws-hostname", re.compile(r"[a-z0-9.-]+\.amazonaws\.com", re.I)),
    ("slack-id", re.compile(r"\b[CDGU](?=[A-Z0-9]*\d)[A-Z0-9]{8,11}\b")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
]


def internal_url(domains):
    hosts = "|".join(re.escape(h) for h in INTERNAL_HOSTS + domains)
    return re.compile(rf"https?://[^\s)]*(?:{hosts})[^\s)]*", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--domain", action="append", default=[], help="employer domain, repeatable")
    ap.add_argument("--allow-email", action="append", default=[], help="email allowed in the file, repeatable")
    ap.add_argument("--deny", help="local denylist, one term per line")
    args = ap.parse_args()

    patterns = PATTERNS + [("internal-url", internal_url(args.domain))]
    allowed = ALLOWED_EMAILS | {e.lower() for e in args.allow_email}

    deny = []
    if args.deny:
        with open(args.deny, encoding="utf-8") as fh:
            deny = [t.strip() for t in fh if t.strip() and not t.startswith("#")]

    findings = []
    with open(args.file, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            for kind, pat in patterns:
                for m in pat.finditer(line):
                    if kind == "email" and m.group(0).lower() in allowed:
                        continue
                    findings.append((n, kind, m.group(0)))
            low = line.lower()
            for term in deny:
                if term.lower() in low:
                    findings.append((n, "denylist", term))
            if "—" in line:
                findings.append((n, "em-dash", "—"))

    if findings:
        for n, kind, match in findings:
            print(f"{n}:{kind}:{match}")
        sys.exit(1)
    print("CLEAN")


if __name__ == "__main__":
    main()
