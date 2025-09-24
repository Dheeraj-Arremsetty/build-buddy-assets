# maintenance_tools.py
import random
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Priority(str, Enum):
    """Enumeration for maintenance issue priority levels."""
    P1 = 'Priority 1 (Critical - AOG)'
    P2 = 'Priority 2 (High)'
    P3 = 'Priority 3 (Medium)'
    P4 = 'Priority 4 (Low)'

@tool(name="log_maintenance_issue", permission=ToolPermission.ADMIN)
def log_maintenance_issue(description: str, priority: Priority, aircraft_tail_number: str) -> str:
    """
    Creates a new maintenance issue ticket in the central tracking system.

    Args:
        description (str): A detailed description of the maintenance issue observed.
        priority (Priority): The priority level of the issue, e.g., 'Priority 1 (Critical - AOG)'.
        aircraft_tail_number (str): The tail number of the aircraft requiring maintenance, e.g., 'N301DN'.

    Returns:
        str: A confirmation message with the newly created ticket number.
    """
    # In a real-world scenario, this function would make an API call to a system like ServiceNow or JIRA.
    # For this demo, we simulate the API call and generate a mock ticket number.
    print(f"Connecting to maintenance backend...")
    ticket_id = f"MX-{random.randint(10000, 99999)}"
    print(f"Creating ticket {ticket_id} for aircraft {aircraft_tail_number} with priority {priority.value} and description: '{description}'")
    
    # Return a user-friendly confirmation message
    return f"Successfully created maintenance ticket {ticket_id} for aircraft {aircraft_tail_number}."