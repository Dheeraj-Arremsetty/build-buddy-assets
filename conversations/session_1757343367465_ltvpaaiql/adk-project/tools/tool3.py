# support_ticket_creator.py
import json
import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="support_ticket_creator", description="Creates support tickets", permission=ToolPermission.ADMIN)
def support_ticket_creator(issue_description: str) -> str:
    """Creates a support ticket from the provided issue description.

    Args:
        issue_description (str): The description of the customer's issue.

    Returns:
        str: The confirmation of the ticket creation.
    """
    ticket_id = f"TICKET-{random.randint(1000, 9999)}"
    timestamp = datetime.datetime.now().isoformat()
    return json.dumps({"ticket_id": ticket_id, "created_at": timestamp, "description": issue_description})