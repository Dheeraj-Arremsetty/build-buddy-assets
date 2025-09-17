import json
import random
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="create_user_account", description="Creates system user accounts for a new employee.")
def create_user_account(full_name: str, employee_id: str, title: str) -> str:
    """
    Creates standard user accounts (e.g., Active Directory, email, VPN) for a new employee.

    Args:
        full_name (str): The new employee's full name.
        employee_id (str): The unique employee ID from the HR system.
        title (str): The employee's job title, used to determine access groups.

    Returns:
        str: A JSON string confirming account creation and providing the new username.
    """
    try:
        # Simulate preparing a payload for the Identity Management API
        payload = {"employeeId": employee_id, "fullName": full_name, "title": title}
        
        # Generate a standard username and mock a successful API response
        parts = full_name.lower().split()
        username = parts[0][0] + parts[-1]
        mock_api_response = {
            "status": "success",
            "message": f"Core system accounts provisioned for {employee_id}.",
            "username": f"{username}@xerox.com",
            "systems_provisioned": ["Active Directory", "Microsoft 365", "VPN Access"]
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Identity API Error: {str(e)}"}, indent=2)

@tool(name="provision_hardware", description="Orders standard hardware for a new employee.")
def provision_hardware(employee_id: str, shipping_address: str) -> str:
    """
    Opens a ticket in the IT service management system to order and ship standard hardware (laptop, monitor).

    Args:
        employee_id (str): The new employee's unique ID for tracking.
        shipping_address (str): The address to ship the hardware to.

    Returns:
        str: A JSON string with the IT service ticket number and the asset tag of the provisioned hardware.
    """
    try:
        # Simulate creating a ServiceNow API request payload
        payload = {
            "requested_for_id": employee_id,
            "category": "Hardware",
            "short_description": f"New Hire Standard Hardware Kit for {employee_id}",
            "shipping_details": { "address": shipping_address }
        }
        
        # Generate mock ticket and asset IDs for the response
        ticket_id = f"IT-REQ-{random.randint(100000, 999999)}"
        asset_tag = f"XEROX-LT-{random.randint(10000, 99999)}"

        mock_api_response = {
            "status": "success",
            "message": "Hardware provisioning request submitted.",
            "ticket_id": ticket_id,
            "asset_tag": asset_tag,
            "items_ordered": ["Standard Laptop", "Docking Station", "24-inch Monitor"],
            "shipping_to": shipping_address
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"ServiceNow API Error: {str(e)}"}, indent=2)