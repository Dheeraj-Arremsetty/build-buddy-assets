# tools/incident_commander_tools.py
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_servicenow_ticket(description: str, business_service: str, severity: int = 1) -> str:
    """
    Creates a new major incident ticket in ServiceNow.

    This tool automates the first critical step of the formal incident response process:
    logging the incident in the system of record. Automating ticket creation ensures that all
    incidents are tracked, assigned, and have an auditable timeline from the very beginning,
    reducing administrative burden on the incident commander.

    Args:
        description (str): A detailed description of the incident.
        business_service (str): The primary business service impacted.
        severity (int): The severity level of the incident (e.g., 1 for Critical).

    Returns:
        str: A JSON string containing the new ServiceNow incident ticket number (e.g., "INC0012345").
    """
    ticket_number = f"INC{random.randint(10000, 99999)}"
    print(f"Creating ServiceNow ticket '{ticket_number}' for service '{business_service}' with description: {description}")
    return json.dumps({"ticket_id": ticket_number, "status": "New"})

@tool(permission=ToolPermission.ADMIN)
def create_slack_channel(incident_id: str) -> str:
    """
    Creates a dedicated Slack channel for a major incident.

    This tool automates the setup of a collaboration space for the incident response team.
    By creating a unique "war room" channel, it ensures all communications, data, and findings
    related to the incident are centralized. This improves coordination and prevents information
    silos, allowing the team to work more effectively towards resolution.

    Args:
        incident_id (str): The incident ticket number (e.g., "INC0012345") to name the channel.

    Returns:
        str: A JSON string with the name of the created Slack channel.
    """
    channel_name = f"incident-{incident_id.lower()}"
    print(f"Creating Slack channel: #{channel_name}")
    return json.dumps({"channel_name": channel_name, "status": "Created"})

@tool(permission=ToolPermission.ADMIN)
def generate_pir_draft(incident_id: str, root_cause: str, resolution_steps: str, timeline: str) -> str:
    """
    Generates a draft Post-Incident Report (PIR).

    This tool automates the often tedious process of compiling a PIR. By synthesizing key
    information gathered during the incident—such as the root cause, timeline, and resolution
    steps—it creates a structured draft report. This accelerates the post-incident learning
    process and ensures that valuable insights are captured consistently.

    Args:
        incident_id (str): The incident ticket number.
        root_cause (str): A summary of the identified root cause.
        resolution_steps (str): A summary of the steps taken to resolve the incident.
        timeline (str): A summary of the incident timeline.

    Returns:
        str: A formatted string containing the draft PIR.
    """
    pir_content = f"""
# Post-Incident Report (DRAFT)

**Incident ID:** {incident_id}
**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}

## 1. Executive Summary
A major incident was declared impacting the Customer Billing Platform. The root cause was identified and resolved, restoring service.

## 2. Incident Timeline
{timeline}

## 3. Root Cause Analysis
{root_cause}

## 4. Resolution Steps
{resolution_steps}

## 5. Next Steps
- [ ] Schedule post-mortem review.
- [ ] Identify and assign preventative action items.
"""
    return pir_content