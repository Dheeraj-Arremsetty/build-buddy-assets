# hr_tools.py
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_hr_profile(full_name: str, role: str, department: str, manager: str, start_date: str) -> str:
    """
    Creates a new employee profile in the core HR system (e.g., Workday).

    This tool is the first critical step in the onboarding process. It generates a unique employee ID
    and officially records the new hire's information, enabling downstream processes like payroll and benefits enrollment.

    Args:
        full_name (str): The full legal name of the new hire.
        role (str): The official job title of the new hire.
        department (str): The department the new hire will be joining.
        manager (str): The name of the new hire's direct manager.
        start_date (str): The official start date for the new hire (e.g., 'YYYY-MM-DD').

    Returns:
        str: A JSON string containing a confirmation message and the newly created employee ID.
    """
    try:
        employee_id = f"EMP{random.randint(90000, 99999)}"
        confirmation = {
            "status": "Success",
            "message": f"HR profile created for {full_name}.",
            "employee_id": employee_id,
            "details": {
                "role": role,
                "department": department,
                "manager": manager,
                "start_date": start_date
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(confirmation)
    except Exception as e:
        return json.dumps({"status": "Error", "message": str(e)})

@tool(permission=ToolPermission.ADMIN)
def send_welcome_packet(employee_id: str, full_name: str) -> str:
    """
    Sends the official digital welcome packet to the new hire.

    This tool triggers the sending of essential first-day information, company policies, and benefits
    enrollment forms. It helps create a positive first impression and ensures the new hire is well-prepared.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The full name of the new hire to personalize the communication.

    Returns:
        str: A JSON string confirming that the welcome packet has been sent.
    """
    confirmation = {
        "status": "Success",
        "message": f"Digital welcome packet sent to {full_name} (ID: {employee_id}).",
        "timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(confirmation)