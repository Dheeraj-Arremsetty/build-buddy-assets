from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field
import datetime

# Although not strictly required by Pydantic for this simple tool,
# including all imports is a best practice.
import json

@tool(name="send_risk_report_email", permission=ToolPermission.ADMIN)
def send_risk_report_email(recipient_email: str, report_summary: str) -> str:
    """
    Sends a summarized risk report to a specified email address. This tool is used by the reporting agent to distribute the final analysis.

    Args:
        recipient_email (str): The email address of the recipient (e.g., 'risk-team@example.com').
        report_summary (str): The content of the risk summary report to be included in the email body.

    Returns:
        str: A confirmation message indicating the email was sent successfully or an error occurred.
    """
    print("--- SIMULATING EMAIL DISPATCH ---")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print(f"Recipient: {recipient_email}")
    print(f"Email Body:\n{report_summary}")
    print("---------------------------------")
    
    # Basic validation for the demo
    if not recipient_email or "@" not in recipient_email:
        return f"Error: Invalid recipient email address provided: {recipient_email}."
    if not report_summary:
        return "Error: Report summary is empty. Cannot send email."

    return f"Successfully sent risk report to {recipient_email}."