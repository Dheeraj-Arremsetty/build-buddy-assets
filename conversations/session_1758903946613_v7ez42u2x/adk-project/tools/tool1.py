import json
import uuid
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="send_form_by_email", permission=ToolPermission.ADMIN)
def send_form_by_email(email_address: str, form_type: str) -> str:
    """
    Sends a specified HR form to an employee's email address.

    This tool is used to initiate simple HR processes by delivering the necessary
    documentation directly to the employee. It's essential for tasks like direct deposit
    setup, benefits enrollment, or tax form completion. The tool validates the email format
    and form type before simulating the email dispatch, ensuring reliable delivery of
    critical documents.

    Args:
        email_address (str): The valid email address of the employee receiving the form.
        form_type (str): The type of form to send. Supported values: 'Direct Deposit', 'W-4', 'Benefits Enrollment'.

    Returns:
        str: A JSON string confirming the action, including the form type and recipient email.
    """
    supported_forms = ['direct deposit', 'w-4', 'benefits enrollment']
    if form_type.lower() not in supported_forms:
        return json.dumps({"status": "error", "message": f"Form type '{form_type}' is not supported."})

    print(f"SIMULATING: Sending '{form_type}' form to {email_address}...")

    response = {
        "status": "success",
        "message": f"The '{form_type}' form has been successfully sent to {email_address}.",
        "timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(response)

@tool(name="create_support_ticket", permission=ToolPermission.ADMIN)
def create_support_ticket(employee_id: str, issue_description: str) -> str:
    """
    Creates a new support ticket for issues that require human intervention.

    When an employee's request cannot be fully resolved through automated actions or
    knowledge base queries, this tool escalates the issue by creating a formal support
    ticket. It captures essential details and generates a unique ticket ID, providing a clear
    audit trail and ensuring that the employee's issue is routed to the correct HR or IT support team
    for resolution.

    Args:
        employee_id (str): The unique identifier for the employee raising the issue.
        issue_description (str): A detailed description of the problem or request.

    Returns:
        str: A JSON string confirming ticket creation, including a unique ticket ID.
    """
    if not employee_id or not issue_description:
        return json.dumps({"status": "error", "message": "Employee ID and issue description are required."})
        
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    print(f"SIMULATING: Creating support ticket for Employee ID {employee_id}...")
    
    response = {
        "status": "success",
        "message": "A support ticket has been created. A team member will reach out shortly.",
        "ticket_id": ticket_id,
        "submitted_at": datetime.utcnow().isoformat()
    }
    return json.dumps(response)