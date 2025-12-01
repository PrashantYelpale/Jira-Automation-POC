# Jira Automation POC

Complete automated daily POC for Jira ticket management.

## What It Does Daily

1. Completes 3-5 tickets per developer (simulates work completion)
2. Adds 5 new tickets to backlog (with random task names from Excel)
3. Assigns unassigned tickets using intelligent algorithm
4. Handles priority override (if requester sets wrong priority)

## Setup

### 1. Add GitHub Secrets

Go to Settings → Secrets → Actions, add:

- `JIRA_API_TOKEN` - Your Jira API token
- `JIRA_EMAIL` - prashantyelpale63@gmail.com
- `JIRA_SERVER` - https://prashantyelpale63.atlassian.net
- `JIRA_PROJECT_KEY` - SCRUM

### 2. Enable GitHub Actions

Go to Actions tab → Enable workflows

### 3. Done!

Automation runs daily at 9 AM CET automatically.

## Manual Run

Actions tab → Daily Jira Automation POC → Run workflow

## Team Members

- Person 1: prashantyelpale63@gmail.com
- Person 2: prashantyelpale01@gmail.com  
- Person 3: prashantyelpale7@gmail.com (Rohit Kumar)

## Assignment Algorithm

```
Score = (Readiness × 10) + Availability Bonus - Workload Penalty

Where:
- Readiness: Developer skill level (0-10)
- Availability: Based on workload
  - ≤3 tickets: +20
  - 4-6 tickets: -10
  - >6 tickets: -100
- Workload Penalty: Prevents overloading
  - >5 tickets: -(workload-5) × 15
  - <2 tickets: +10
```

## Monitoring

- Actions tab: See all runs
- Jira board: See assignments
- Logs: Download from workflow artifacts

## Cost

FREE! GitHub Actions provides 2,000 minutes/month free.

## POC Success Criteria

After 1 week:
- Tickets completed daily
- New tickets added daily
- Assignments balanced
- Priority overrides working
