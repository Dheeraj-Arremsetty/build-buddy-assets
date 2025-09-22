# /tools/it_support_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# In-memory dictionary to simulate a database of created tickets
# This allows the demo to maintain state between tool calls
MOCK_TICKET_DB = {}

@tool(name="create_service_now_incident", permission=ToolPermission.ADMIN)
def create_service_now_incident(short_description: str) -> str:
    """
    Creates a new incident ticket in the IT Service Management system (e.g., ServiceNow).
    This tool is used when an employee reports a new IT issue that requires tracking.

    Args:
        short_description (str): A brief, one-sentence summary of the user's IT issue.

    Returns:
        str: A JSON string containing a confirmation message and details of the created ticket.
    """
    # Business Value: This tool automates the creation of L1 support tickets, reducing manual
    # entry for both employees and the IT help desk. It ensures that all issues are logged
    # consistently and immediately, accelerating the time to resolution and providing a clear
    # audit trail for every reported problem.
    #
    # Technical Implementation: This function simulates a POST request to an ITSM API. It generates a
    # unique ticket number and a realistic data structure for the new incident, including metadata like
    # timestamps, priority, and category. The ticket is stored in a mock in-memory database to allow
    # for follow-up status checks within the same demo session.
    try:
        ticket_number = f"INC{random.randint(1000000, 9999999)}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        new_ticket = {
            "ticket_number": ticket_number,
            "status": "New",
            "short_description": short_description,
            "category": "Hardware",
            "priority": "3 - Medium",
            "assignment_group": "IT Help Desk",
            "caller_id": "employee@example.com", # Mocked user
            "created_at": timestamp,
            "updated_at": timestamp
        }

        MOCK_TICKET_DB[ticket_number] = new_ticket

        response = {
            "message": f"Successfully created IT support ticket {ticket_number}.",
            "ticket_details": new_ticket
        }
        return json.dumps(response, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to create ticket: {str(e)}"})


@tool(name="get_incident_status_by_number", permission=ToolPermission.ADMIN)
def get_incident_status_by_number(ticket_number: str) -> str:
    """
    Retrieves the current status and details of an existing IT incident ticket by its number.
    Use this tool when an employee asks for an update on a ticket they have already created.

    Args:
        ticket_number (str): The unique identifier of the incident ticket (e.g., "INC1234567").

    Returns:
        str: A JSON string containing the details of the ticket or an error message if not found.
    """
    # Business Value: This tool provides employees with self-service access to the status of their
    # IT tickets, 24/7. This reduces follow-up calls and emails to the help desk, freeing up
    # IT staff to focus on resolving issues rather than providing routine status updates, thus
    # improving overall IT department efficiency and employee satisfaction.
    #
    # Technical Implementation: This function simulates a GET request to an ITSM API endpoint.
    # It looks up the provided ticket_number in our mock in-memory database. If found, it realistically
    # simulates a potential status update (e.g., moving from 'New' to 'In Progress') and returns
    # the ticket's full data structure. Otherwise, it returns a clear "not found" error.
    if ticket_number in MOCK_TICKET_DB:
        ticket_details = MOCK_TICKET_DB[ticket_number]
        
        # Simulate a potential status update for demo purposes
        if ticket_details["status"] == "New" and random.random() > 0.5:
             ticket_details["status"] = "In Progress"
             ticket_details["assignment_group"] = "Network Support Team"
             ticket_details["updated_at"] = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
             MOCK_TICKET_DB[ticket_number] = ticket_details

        return json.dumps(ticket_details, indent=2)
    else:
        return json.dumps({"error": f"Ticket {ticket_number} not found."}, indent=2)