import json
from typing import Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="send_sms_notification", permission=ToolPermission.ADMIN)
def send_sms_notification(teacher_name: str, phone_number: str, class_details: str) -> Dict:
    """
    Sends a simulated SMS notification to a teacher to ask if they can sub for a class.

    This tool acts as the bridge to external communication systems (like Twilio). It automates the outreach process, saving managers from having to manually text or call potential substitutes. The tool simulates a confirmation, allowing the automated workflow to proceed to the final step.

    Args:
        teacher_name (str): The name of the teacher to contact.
        phone_number (str): The phone number of the teacher.
        class_details (str): A summary of the class details (e.g., "6 PM C2 class at LoDo tomorrow").

    Returns:
        Dict: A dictionary indicating the status of the notification and a simulated confirmation.
    """
    # In a real-world scenario, this would integrate with an SMS API like Twilio.
    # For this demo, we print to the console and return a success message.
    print(f"\n--- SIMULATING SMS ---")
    print(f"To: {teacher_name} ({phone_number})")
    print(f"Message: Hi {teacher_name}, can you sub the {class_details}? Reply 'CONFIRM' if yes.")
    print(f"--- SIMULATION END ---\n")
    
    # We simulate an immediate positive response for the "happy path" demo.
    return {
        "status": "Notification Sent",
        "confirmation_received": True,
        "message": f"Successfully sent sub request to {teacher_name} and received confirmation."
    }