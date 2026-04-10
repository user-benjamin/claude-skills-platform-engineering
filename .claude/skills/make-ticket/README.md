# make-ticket

Generates a structured Jira ticket from a plain-English description.

## Usage

```
/make-ticket the payments service is throwing 503s during peak traffic, we think it's the connection pool
```

Claude will produce a fully populated ticket with inferred priority, summary,
desired outcome, acceptance criteria, testing methodology, rollout plan, and
incidental notes.

## Phase 1 (current)

Generates ticket content as markdown. Copy/paste into Jira manually.

## Phase 2 (planned): Jira API Integration

Automatically creates the ticket in Jira via the REST API.

### Setup

1. Generate a Jira API token at `https://id.atlassian.com/manage-profile/security/api-tokens`
2. Add to your environment:
   ```bash
   export JIRA_BASE_URL=https://your-org.atlassian.net
   export JIRA_USER=your@email.com
   export JIRA_API_TOKEN=your-token
   export JIRA_PROJECT_KEY=PLAT   # default project key
   ```
3. Install dependencies:
   ```bash
   pip install anthropic requests
   ```

Phase 2 will use `agents/jira_creator.py` to POST the generated ticket directly
to the Jira API, then return the ticket URL as a PR comment or terminal output.
