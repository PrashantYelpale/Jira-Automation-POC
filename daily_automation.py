"""
Complete Daily Automation for Jira POC
- Completes 3-5 tickets per developer
- Adds 5 new tickets to backlog
- Assigns new tickets automatically
- Handles priority override
"""
import os
from jira import JIRA
from datetime import datetime, timedelta
import random
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
JIRA_SERVER = os.getenv('JIRA_SERVER', 'https://prashantyelpale63.atlassian.net')
JIRA_EMAIL = os.getenv('JIRA_EMAIL', 'prashantyelpale63@gmail.com')
JIRA_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'SCRUM')

# Team members (3 developers)
TEAM_EMAILS = [
    'prashantyelpale63@gmail.com',  # Person 1
    'prashantyelpale01@gmail.com',  # Person 2
    'prashantyelpale7@gmail.com'    # Person 3 (Rohit)
]

# Task templates from Excel
TASK_TEMPLATES = [
    {'name': 'Drupal Salesforce Mapping (WER)', 'complexity': 'Simple', 'priority': 'P1', 'readiness': {'p1': 10, 'p2': 8, 'p3': 6}},
    {'name': 'Drupal Salesforce Mapping (WER + DOI)', 'complexity': 'Complex', 'priority': 'P2', 'readiness': {'p1': 8, 'p2': 10, 'p3': 7}},
    {'name': 'FormMan Integration (Regular)', 'complexity': 'Complex', 'priority': 'P2', 'readiness': {'p1': 10, 'p2': 8, 'p3': 9}},
    {'name': 'FormMan Integration (Standard)', 'complexity': 'Medium', 'priority': 'P3', 'readiness': {'p1': 10, 'p2': 9, 'p3': 7}},
    {'name': 'Meta Form Integration', 'complexity': 'Complex', 'priority': 'P2', 'readiness': {'p1': 9, 'p2': 8, 'p3': 10}},
    {'name': 'Drupal SMFC Config', 'complexity': 'Complex', 'priority': 'P2', 'readiness': {'p1': 9, 'p2': 10, 'p3': 7}},
    {'name': 'Website Case Drupal (SF Mapping)', 'complexity': 'Complex', 'priority': 'P2', 'readiness': {'p1': 8, 'p2': 9, 'p3': 10}},
    {'name': 'FormMan Integration (Event Form)', 'complexity': 'Medium', 'priority': 'P3', 'readiness': {'p1': 10, 'p2': 8, 'p3': 10}},
    {'name': 'VEV Integration (FormMan)', 'complexity': 'Medium', 'priority': 'P3', 'readiness': {'p1': 8, 'p2': 1, 'p3': 10}},
    {'name': 'Drupal Event Form Mapping', 'complexity': 'Medium', 'priority': 'P2', 'readiness': {'p1': 10, 'p2': 9, 'p3': 8}},
]

class DailyAutomation:
    def __init__(self):
        logger.info("="*80)
        logger.info("DAILY JIRA AUTOMATION - POC")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*80)
        
        self.jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
        logger.info("✅ Connected to Jira")
        
        # Get team account IDs
        self.team = self._get_team_members()
        
    def _get_team_members(self):
        """Get team member account IDs"""
        logger.info("\n📋 Getting team members...")
        team = {}
        
        for email in TEAM_EMAILS:
            try:
                users = self.jira.search_users(query=email)
                if users:
                    user = users[0]
                    key = f'p{len(team)+1}'
                    team[key] = {
                        'name': user.displayName,
                        'email': email,
                        'account_id': user.accountId
                    }
                    logger.info(f"   ✅ {user.displayName}")
            except Exception as e:
                logger.error(f"   ❌ Error getting user {email}: {str(e)}")
        
        return team
    
    def complete_tickets(self):
        """Complete 3-5 tickets per developer"""
        logger.info("\n" + "="*80)
        logger.info("STEP 1: Completing Assigned Tickets")
        logger.info("="*80)
        
        for key, member in self.team.items():
            # Get assigned tickets
            jql = f'project = {PROJECT_KEY} AND assignee = "{member["account_id"]}" AND status IN ("To Do", "In Progress")'
            tickets = self.jira.search_issues(jql, maxResults=5)
            
            # Complete 3-5 tickets randomly
            num_to_complete = random.randint(3, min(5, len(tickets)))
            
            logger.info(f"\n👤 {member['name']}: Completing {num_to_complete} tickets")
            
            for i, ticket in enumerate(tickets[:num_to_complete]):
                try:
                    # Transition to Done
                    transitions = self.jira.transitions(ticket)
                    done_transition = None
                    
                    for t in transitions:
                        if t['name'].lower() in ['done', 'close', 'closed', 'complete']:
                            done_transition = t['id']
                            break
                    
                    if done_transition:
                        self.jira.transition_issue(ticket, done_transition)
                        logger.info(f"   ✅ Completed: {ticket.key}")
                    else:
                        # Just update status field if transition not found
                        logger.info(f"   ⚠️  No Done transition for {ticket.key}, skipping")
                        
                except Exception as e:
                    logger.error(f"   ❌ Error completing {ticket.key}: {str(e)}")
    
    def add_new_tickets(self):
        """Add 5 new tickets to backlog"""
        logger.info("\n" + "="*80)
        logger.info("STEP 2: Adding 5 New Tickets to Backlog")
        logger.info("="*80)
        
        created_tickets = []
        
        for i in range(5):
            # Randomly select a task template
            template = random.choice(TASK_TEMPLATES)
            
            # Randomly decide if requester sets wrong priority (30% chance)
            requested_priority = template['priority']
            if random.random() < 0.3:
                # Requester thinks it's P1 but it's actually P2/P3
                requested_priority = 'P1'
            
            try:
                issue_dict = {
                    'project': {'key': PROJECT_KEY},
                    'summary': f"SR-{datetime.now().strftime('%Y%m%d')}-{i+1}: {template['name']}",
                    'description': f'''Support Request Details

Task: {template['name']}
Complexity: {template['complexity']}
Requested Priority: {requested_priority}
Actual Priority: {template['priority']}

Description:
This is an automated test ticket for POC demonstration.

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---
Automated POC Ticket
                    ''',
                    'issuetype': {'name': 'Task'},
                    'labels': [template['complexity'], 'POC_Auto', 'Unassigned']
                }
                
                issue = self.jira.create_issue(fields=issue_dict)
                created_tickets.append(issue.key)
                
                # Add priority note if override needed
                if requested_priority != template['priority']:
                    comment = f'''⚠️ Priority Override Needed

Requester Priority: {requested_priority}
Actual Priority: {template['priority']}
Reason: Based on task complexity ({template['complexity']})

System will assign with correct priority.
                    '''
                    self.jira.add_comment(issue, comment)
                
                logger.info(f"   ✅ Created: {issue.key} - {template['name']}")
                
            except Exception as e:
                logger.error(f"   ❌ Error creating ticket: {str(e)}")
        
        logger.info(f"\n✅ Created {len(created_tickets)} new tickets")
        return created_tickets
    
    def assign_tickets(self):
        """Assign unassigned tickets using intelligent algorithm"""
        logger.info("\n" + "="*80)
        logger.info("STEP 3: Assigning Unassigned Tickets")
        logger.info("="*80)
        
        # Get unassigned tickets
        jql = f'project = {PROJECT_KEY} AND assignee is EMPTY AND status NOT IN (Done, Closed)'
        unassigned = self.jira.search_issues(jql, maxResults=20)
        
        logger.info(f"\n📋 Found {len(unassigned)} unassigned tickets")
        
        if not unassigned:
            logger.info("   ✅ No unassigned tickets")
            return
        
        # Get current workload
        workloads = {}
        for key, member in self.team.items():
            jql = f'project = {PROJECT_KEY} AND assignee = "{member["account_id"]}" AND status NOT IN (Done, Closed)'
            tickets = self.jira.search_issues(jql)
            workloads[key] = len(tickets)
        
        logger.info(f"\n📊 Current Workload:")
        for key, member in self.team.items():
            logger.info(f"   {member['name']}: {workloads[key]} tickets")
        
        # Assign each ticket
        logger.info(f"\n🤖 Assigning Tickets:")
        
        for issue in unassigned:
            try:
                # Extract task name
                task_name = issue.fields.summary.split(': ', 1)[1] if ': ' in issue.fields.summary else issue.fields.summary
                
                # Find matching template for readiness scores
                template = None
                for t in TASK_TEMPLATES:
                    if t['name'] in task_name:
                        template = t
                        break
                
                if not template:
                    template = random.choice(TASK_TEMPLATES)
                
                # Score each developer
                scores = {}
                for key, member in self.team.items():
                    readiness = template['readiness'].get(key, 5)
                    workload = workloads[key]
                    
                    # Calculate score
                    score = readiness * 10
                    
                    # Availability bonus
                    if workload <= 3:
                        score += 20
                    elif workload <= 6:
                        score -= 10
                    else:
                        score -= 100
                    
                    # Workload penalty
                    if workload > 5:
                        score -= (workload - 5) * 15
                    elif workload < 2:
                        score += 10
                    
                    scores[key] = score
                
                # Find best match
                best_key = max(scores, key=scores.get)
                best_member = self.team[best_key]
                best_score = scores[best_key]
                
                # Assign
                issue.update(fields={'assignee': {'accountId': best_member['account_id']}})
                
                # Add comment
                comment = f'''🤖 Automated Assignment

Assigned to: {best_member['name']}
Assignment Score: {best_score}
Readiness: {template['readiness'].get(best_key, 5)}/10
Current Workload: {workloads[best_key]} tickets

Scoring Details:
'''
                for key, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    member = self.team[key]
                    comment += f"- {member['name']}: {score} (Readiness: {template['readiness'].get(key, 5)}/10, Workload: {workloads[key]})\n"
                
                comment += "\n---\nAutomated by GitHub Actions POC"
                
                self.jira.add_comment(issue, comment)
                
                # Update workload
                workloads[best_key] += 1
                
                logger.info(f"   ✅ {issue.key} → {best_member['name']} (Score: {best_score})")
                
            except Exception as e:
                logger.error(f"   ❌ Error assigning {issue.key}: {str(e)}")
        
        # Show final workload
        logger.info(f"\n📊 Final Workload:")
        for key, member in self.team.items():
            jql = f'project = {PROJECT_KEY} AND assignee = "{member["account_id"]}" AND status NOT IN (Done, Closed)'
            tickets = self.jira.search_issues(jql)
            logger.info(f"   {member['name']}: {len(tickets)} tickets")
    
    def run(self):
        """Run complete daily automation"""
        try:
            # Step 1: Complete tickets
            self.complete_tickets()
            
            # Step 2: Add new tickets
            self.add_new_tickets()
            
            # Step 3: Assign tickets
            self.assign_tickets()
            
            logger.info("\n" + "="*80)
            logger.info("✅ DAILY AUTOMATION COMPLETE!")
            logger.info("="*80)
            logger.info(f"\n📊 Check Jira: {JIRA_SERVER}/jira/software/projects/{PROJECT_KEY}/boards/1")
            
        except Exception as e:
            logger.error(f"\n❌ Automation failed: {str(e)}")
            raise

if __name__ == '__main__':
    automation = DailyAutomation()
    automation.run()
