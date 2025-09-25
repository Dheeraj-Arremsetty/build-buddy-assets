# tools/communications_tools.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def send_slack_message(channel: str, message: str) -> str:
    """
    Sends a message to a specified Slack channel.

    This tool provides the mechanism for delivering real-time, technical updates to the
    incident response team in their dedicated Slack channel. It is essential for keeping
    engineers and technical stakeholders informed of the latest findings, actions taken,
    and next steps, ensuring the entire response team is aligned.

    Args:
        channel (str): The Slack channel to send the message to (e.g., "incident-inc0012345").
        message (str): The message content to be sent.

    Returns:
        str: A JSON string confirming the message was sent successfully.
    """
    print(f"Sending Slack message to #{channel}:\n---\n{message}\n---")
    return json.dumps({"status": "Message sent", "channel": channel})

@tool(permission=ToolPermission.ADMIN)
def send_email_update(recipient_list: str, subject: str, body: str) -> str:
    """
    Sends an email update to a list of recipients.

    This tool is used to send high-level, business-impact-focused communications to leadership
    and non-technical stakeholders. By using a separate channel (email) and tailoring the
    message, it ensures that executives receive the information they need—business impact,
    customer impact, and ETA for resolution—without being overwhelmed by technical jargon.

    Args:
        recipient_list (str): A comma-separated list of recipient email addresses.
        subject (str): The subject line of the email.
        body (str): The HTML or plain text body of the email.

    Returns:
        str: A JSON string confirming the email was sent successfully.
    """
    print(f"Sending Email to [{recipient_list}] with subject '{subject}':\n---\n{body}\n---")
    return json.dumps({"status": "Email sent", "recipients": recipient_list.split(',')})