# tools/service_now/get_my_service_now_incidents.py
import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def get_my_service_now_incidents() -> list[dict]:
    """
    Retrieves a list of all open ServiceNow incidents for the current user.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents an open IT incident.
    """
    incidents = [
        {
            "incident_number": f"INC{random.randint(1000000, 9999999)}",
            "status": "In Progress",
            "short_description": "Cannot access shared drive",
            "urgency": "2 - Medium",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
        },
        {
            "incident_number": f"INC{random.randint(1000000, 9999999)}",
            "status": "On Hold",
            "short_description": "New monitor request",
            "urgency": "3 - Low",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat()
        }
    ]
    return incidents