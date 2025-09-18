import random
import logging
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@tool(name="create_it_ticket", description="Creates an IT support ticket for hardware or software issues.")
def create_it_ticket(issue_description: str) -> str:
    """Creates an IT support ticket in the internal tracking system.
    Use this for any issues related to logging in, cash register (POS) problems,
    or broken equipment.

    Args:
        issue_description (str): A clear and concise description of the IT problem the user is facing.

    Returns:
        str: A confirmation message including the newly created ticket number.
    """
    if not issue_description or not isinstance(issue_description, str):
        return "Error: A description of the issue is required to create a ticket."

    # Simulate API call to a ticketing system and generate a ticket number
    ticket_id = f"SBX-{random.randint(70000, 99999)}"
    
    # Use logging for server-side traceability instead of print()
    logging.info(f"Generated IT Ticket: {ticket_id} for issue: '{issue_description}'")

    return f"Success! I've created an IT support ticket for you. The reference number is #{ticket_id}. A technician will be in touch shortly."