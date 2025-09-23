# it_tools.py
import json
import random
import requests
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# This dictionary simulates a response from a mock API endpoint
MOCK_API_RESPONSES = {
    "order_equipment": lambda pkg: {"ticket_id": f"SNOW-TKT{random.randint(700, 999)}", "package": pkg, "status": "Pending Shipment"},
    "create_accounts": lambda name: {"request_id": f"JIRA-USR{random.randint(1000, 2000)}", "username": f"{name.lower().replace(' ','.')}", "status": "Accounts Provisioning"}
}


@tool(permission=ToolPermission.ADMIN)
def create_user_accounts(employee_id: str, full_name: str) -> str:
    """
    Creates standard user accounts (Email, Slack, VPN) for a new employee.

    This tool automates the creation of essential communication and access accounts. It reduces manual
    work for the IT team and ensures the new hire can connect with colleagues and systems immediately.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The full name of the new hire, used to generate a username.

    Returns:
        str: A JSON string containing the service desk request ID and the generated username.
    """
    # In a real scenario, this would make an API call. We simulate it here.
    # response = requests.post("http://mock-it-api/create_accounts", json={"id": employee_id, "name": full_name})
    # response.raise_for_status()
    # return json.dumps(response.json())
    
    response_data = MOCK_API_RESPONSES["create_accounts"](full_name)
    return json.dumps(response_data)


@tool(permission=ToolPermission.ADMIN)
def order_equipment(employee_id: str, package_type: str) -> str:
    """
    Orders standard IT equipment (laptop, monitor) for a new employee based on their role.

    This tool streamlines hardware procurement by creating a ticket in the IT service management system (e.g., ServiceNow).
    It ensures equipment is ordered promptly based on pre-defined packages, avoiding configuration errors.

    Args:
        employee_id (str): The unique ID of the new employee.
        package_type (str): The type of equipment package (e.g., 'Standard', 'Developer').

    Returns:
        str: A JSON string with the IT service ticket number for tracking.
    """
    # In a real scenario, this would make an API call. We simulate it here.
    # response = requests.post("http://mock-it-api/order_equipment", json={"id": employee_id, "pkg": package_type})
    # response.raise_for_status()
    # return json.dumps(response.json())

    response_data = MOCK_API_RESPONSES["order_equipment"](package_type)
    return json.dumps(response_data)