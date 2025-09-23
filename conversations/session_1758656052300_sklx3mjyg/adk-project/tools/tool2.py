import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def setup_payroll(employee_name: str, employee_id: str, start_date: str) -> str:
    """
    Sets up the new hire in the payroll system.

    Args:
        employee_name (str): The full name of the new hire.
        employee_id (str): The unique employee ID number.
        start_date (str): The official start date of the new hire (YYYY-MM-DD).

    Returns:
        str: A JSON string confirming payroll setup and next steps.
    """
    confirmation_id = f"PAY-{''.join(random.choices('0123456789', k=8))}"
    response = {
        "status": "Success",
        "message": f"Payroll profile for {employee_name} (ID: {employee_id}) has been created.",
        "confirmation_id": confirmation_id,
        "start_date_registered": start_date,
        "next_steps": "New hire will receive an email to complete direct deposit and tax withholding forms."
    }
    return json.dumps(response, indent=2)

@tool(permission=ToolPermission.ADMIN)
def send_benefits_enrollment_package(employee_name: str, email: str) -> str:
    """
    Sends the benefits enrollment package and instructions to the new hire's email.

    Args:
        employee_name (str): The full name of the new hire.
        email (str): The new hire's company email address.

    Returns:
        str: A JSON string confirming that the package was sent.
    """
    tracking_id = f"BEN-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))}"
    response = {
        "status": "Success",
        "message": f"Benefits enrollment package sent to {employee_name} at {email}.",
        "tracking_id": tracking_id,
        "sent_timestamp": datetime.utcnow().isoformat(),
        "enrollment_deadline_notice": "The new hire has 30 days from their start date to complete enrollment."
    }
    return json.dumps(response, indent=2)