import json
import random
import string
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_user_account(full_name: str, role: str, department: str) -> str:
    """
    Creates a new user account in the company's directory (e.g., Active Directory).

    Args:
        full_name (str): The full name of the new hire.
        role (str): The job role of the new hire (e.g., 'Software Engineer').
        department (str): The department the new hire belongs to.

    Returns:
        str: A JSON string confirming the account creation with details.
    """
    try:
        name_parts = full_name.lower().split()
        username = name_parts[0][0] + name_parts[-1]
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        email = f"{username}@example-client-corp.com"
        
        response = {
            "status": "Success",
            "message": f"Account for {full_name} created successfully.",
            "username": username,
            "email": email,
            "temp_password_notice": "A temporary password has been securely sent to the hiring manager.",
            "creation_timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"status": "Error", "message": f"Failed to create user account: {str(e)}"})

@tool(permission=ToolPermission.ADMIN)
def order_hardware(employee_name: str, role: str) -> str:
    """
    Orders standard hardware (laptop, monitor) based on the new hire's role.

    Args:
        employee_name (str): The full name of the new hire.
        role (str): The job role, which determines the hardware kit.

    Returns:
        str: A JSON string with the order confirmation and tracking details.
    """
    # Mock logic to determine hardware based on role
    if "engineer" in role.lower() or "developer" in role.lower():
        kit = "High-Performance Laptop (16GB RAM, 512GB SSD), Dual 24-inch Monitors"
    elif "sales" in role.lower():
        kit = "Business Laptop (16GB RAM, 256GB SSD), Single 27-inch Monitor"
    else:
        kit = "Standard Business Laptop (8GB RAM, 256GB SSD), Single 24-inch Monitor"
        
    order_id = f"HW-{''.join(random.choices(string.digits, k=7))}"
    tracking_number = f"1Z{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}"
    delivery_date = (datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    response = {
        "status": "Success",
        "message": f"Hardware order placed for {employee_name}.",
        "order_id": order_id,
        "hardware_kit": kit,
        "tracking_number": tracking_number,
        "estimated_delivery": delivery_date
    }
    return json.dumps(response, indent=2)

@tool(permission=ToolPermission.ADMIN)
def assign_software_licenses(employee_name: str, role: str) -> str:
    """
    Assigns software licenses from a predefined list based on the new hire's role.

    Args:
        employee_name (str): The full name of the new hire.
        role (str): The job role, which determines the software bundle.

    Returns:
        str: A JSON string confirming which licenses were assigned.
    """
    base_licenses = ["Microsoft 365 E5", "Slack", "Zoom Pro"]
    role_specific = {
        "software engineer": ["JetBrains Ultimate Pack", "Docker Desktop", "Postman Pro"],
        "sales associate": ["Salesforce Enterprise", "LinkedIn Sales Navigator", "DocuSign"],
        "hr specialist": ["Workday HCM", "Greenhouse Recruiting"]
    }
    
    assigned_licenses = base_licenses + role_specific.get(role.lower(), ["Jira Standard"])
    
    response = {
        "status": "Success",
        "message": f"Software licenses assigned to {employee_name} for the role of {role}.",
        "assigned_licenses": assigned_licenses,
        "assignment_date": datetime.utcnow().isoformat()
    }
    return json.dumps(response, indent=2)