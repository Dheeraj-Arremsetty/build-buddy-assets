# tools/service_now/create_service_now_incident.py
import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field
from enum import Enum

class Urgency(str, Enum):
    HIGH = '1 - High'
    MEDIUM = '2 - Medium'
    LOW = '3 - Low'

@tool(permission=ToolPermission.ADMIN)
def create_service_now_incident(short_description: str, urgency: Urgency = Urgency.LOW) -> dict:
    """
    Creates a new incident in ServiceNow for IT support.

    Args:
        short_description (str): A brief summary of the user's issue.
        urgency (Urgency, optional): The urgency of the ticket. Can be one of "1 - High", "2 - Medium", or "3 - Low". Defaults to "3 - Low".

    Returns:
        dict: A dictionary containing the details of the newly created incident, including the incident number and status.
    """
    incident_number = f"INC{random.randint(1000000, 9999999)}"
    created_time = datetime.datetime.now().isoformat()

    return {
        "incident_number": incident_number,
        "status": "New",
        "short_description": short_description,
        "urgency": urgency.value,
        "created_at": created_time,
        "confirmation": f"Successfully created incident {incident_number}."
    }