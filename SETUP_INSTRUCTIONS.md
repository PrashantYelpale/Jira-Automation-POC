SETUP INSTRUCTIONS FOR GITHUB POC

Step 1: Push Code to GitHub (5 minutes)

1. Open terminal in GitHub-POC-Automation folder
2. Run these commands:

   git init
   git add .
   git commit -m "Initial commit - Jira Automation POC"
   git remote add origin https://github.com/PrashantYelpale/Jira-Automation-POC.git
   git branch -M main
   git push -u origin main

Step 2: Add GitHub Secrets (3 minutes)

1. Go to: https://github.com/PrashantYelpale/Jira-Automation-POC
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these 4 secrets:

   Secret 1:
   Name: JIRA_API_TOKEN
   Value: ATATT3xFfGF0KMkxmIyB7nhkwfiui2WPxjL6hwydeLkwQjQjoaE0m3PnvnNIEzhN_wQvYXzBxhnQLxFdaWNCcG71AwBbbTTrgNihvipqEfPT00dU2Dj7ECol2yNZnA_8SzJ2JvgkXpAEtT-_UhoBzQ2l38dcC3TlAtRLjAoxNEKIz4JYJYZf-lw=880FD2F2

   Secret 2:
   Name: JIRA_EMAIL
   Value: prashantyelpale63@gmail.com

   Secret 3:
   Name: JIRA_SERVER
   Value: https://prashantyelpale63.atlassian.net

   Secret 4:
   Name: JIRA_PROJECT_KEY
   Value: SCRUM

Step 3: Enable GitHub Actions (1 minute)

1. Go to Actions tab
2. Click "I understand my workflows, go ahead and enable them"

Step 4: Test Manual Run (2 minutes)

1. Actions tab → Daily Jira Automation POC
2. Click "Run workflow" → Run workflow
3. Wait 1-2 minutes
4. Check if green checkmark appears

Step 5: Verify in Jira (1 minute)

1. Go to: https://prashantyelpale63.atlassian.net/jira/software/projects/SCRUM/boards/1
2. Check if:
   - Some tickets completed
   - New tickets added
   - Tickets assigned

DONE! Automation will run daily at 9 AM CET automatically.

What Happens Daily:

1. Completes 3-5 tickets per developer
2. Adds 5 new tickets to backlog
3. Assigns unassigned tickets intelligently
4. Handles priority overrides

Monitoring:

- Actions tab: See all runs
- Green checkmark = Success
- Red X = Failed (check logs)

Stop/Pause:

- Actions tab → Daily Jira Automation POC → Disable workflow

Cost:

FREE! GitHub Actions provides 2,000 minutes/month free.
This uses ~2 minutes per day = 60 minutes/month.

Troubleshooting:

Issue: Workflow not running
Fix: Check if secrets are added correctly

Issue: Authentication failed
Fix: Regenerate API token and update secret

Issue: No tickets found
Fix: Check if JIRA_PROJECT_KEY is correct (SCRUM)

Support:

Check logs in Actions tab for detailed error messages.
