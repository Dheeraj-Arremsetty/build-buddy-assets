# tools/it_support_tools.py
import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock database to store ticket information
MOCK_TICKET_DB = {}

@tool(name="create_it_ticket", permission=ToolPermission.ADMIN)
def create_it_ticket(issue_summary: str, employee_id: str) -> str:
    """
    Creates a new IT support ticket in the system for requests like hardware or software.

    Args:
        issue_summary (str): A brief, clear description of the IT issue or request (e.g., 'Request corporate laptop').
        employee_id (str): The unique ID of the employee making the request.

    Returns:
        str: The confirmation message including the new ticket number.
    """
    ticket_number = f"INC{random.randint(10000, 99999)}"
    creation_time = datetime.datetime.now().isoformat()
    
    MOCK_TICKET_DB[ticket_number] = {
        "employee_id": employee_id,
        "summary": issue_summary,
        "status": "New",
        "created_at": creation_time,
        "updated_at": creation_time
    }
    
    print(f"Creating ticket {ticket_number} for {employee_id} with summary: {issue_summary}")
    return f"Successfully created IT ticket {ticket_number} for your request: '{issue_summary}'."

@tool(name="check_ticket_status", permission=ToolPermission.ADMIN)
def check_ticket_status(ticket_number: str) -> str:
    """
    Checks the status of an existing IT support ticket.

    Args:
        ticket_number (str): The unique ticket number to check (e.g., 'INC12345').

    Returns:
        str: A message describing the current status of the ticket, or an error if not found.
    """
    if ticket_number in MOCK_TICKET_DB:
        ticket_data = MOCK_TICKET_DB[ticket_number]
        # Simulate status change for demo purposes
        if random.random() > 0.5 and ticket_data["status"] == "New":
            ticket_data["status"] = "In Progress"
            ticket_data["updated_at"] = datetime.datetime.now().isoformat()

        return f"Ticket {ticket_number} ('{ticket_data['summary']}') is currently in status: '{ticket_data['status']}'. Last updated: {ticket_data['updated_at']}."
    else:
        return f"Error: Ticket {ticket_number} not found in the system."