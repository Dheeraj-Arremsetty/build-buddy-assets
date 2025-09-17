import json
import random
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="create_employee_record", description="Creates a new employee record in the HR system.")
def create_employee_record(full_name: str, title: str, start_date: str, manager: str) -> str:
    """
    Creates a new employee record in the core HR system with essential details.
    This is the first step in the official onboarding process.

    Args:
        full_name (str): The new employee's full legal name.
        title (str): The new employee's official job title.
        start_date (str): The employee's first day of work (e.g., '2024-10-01').
        manager (str): The name of the hiring manager.

    Returns:
        str: A JSON string containing a confirmation message and the newly generated unique employee ID.
    """
    try:
        # Simulate preparing a payload for an internal HRIS API
        payload = {
            "fullName": full_name,
            "jobTitle": title,
            "startDate": start_date,
            "managerName": manager,
            "action": "CREATE_PROFILE"
        }
        
        # Simulate making a POST request to the API endpoint
        # In a real scenario: response = requests.post(api_url, json=payload, headers=headers)
        
        # Generate a mock successful response from the API
        employee_id = f"XEROX-{random.randint(10000, 99999)}"
        mock_api_response = {
            "status": "success",
            "message": f"Employee record created for {full_name}.",
            "employee_id": employee_id,
            "details": payload
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        # Simulate an API error response
        error_response = {
            "status": "error",
            "message": "Failed to connect to HRIS API.",
            "details": str(e)
        }
        return json.dumps(error_response, indent=2)