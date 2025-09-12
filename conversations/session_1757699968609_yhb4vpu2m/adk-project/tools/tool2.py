# tools/maintenance_tools.py
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

class TicketResponse(BaseModel):
    status: str = Field(description="The status of the ticket creation, e.g., 'success'.")
    ticket_id: str = Field(description="The unique identifier for the created maintenance ticket.")
    message: str = Field(description="A confirmation message for the user.")

@tool
def report_equipment_issue(equipment_name: str, issue_description: str) -> TicketResponse:
    """
    Creates a maintenance ticket for broken or malfunctioning equipment.

    Args:
        equipment_name (str): The name of the equipment that is broken (e.g., 'main grinder', 'espresso machine').
        issue_description (str): A detailed description of the problem.

    Returns:
        TicketResponse: An object containing the status and ID of the newly created ticket.
    """
    print(f"SIMULATING API CALL: Creating ticket for '{equipment_name}' with issue: '{issue_description}'")
    
    # Generate a random, realistic-looking ticket ID
    ticket_id = f"INC{random.randint(1000000, 9999999)}"
    
    confirmation_message = f"Maintenance ticket {ticket_id} has been successfully logged for the {equipment_name}."
    
    return TicketResponse(
        status="success", 
        ticket_id=ticket_id, 
        message=confirmation_message
    )