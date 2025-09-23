# tools/identity_tools.py
import json
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_user_account(employee_name: str, department: str, role: str) -> str:
    """
    Creates a new user account in the identity management system (Okta).

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.
        role (str): The job role of the employee.

    Returns:
        str: A JSON string with the new user's ID, username, and account status.
    """
    username = f"{employee_name.lower().replace(' ', '.')}"
    user_id = f"okta-{random.randint(1000000, 9999999)}"
    response = {
        "status": "success",
        "message": f"Okta user account created for {employee_name}.",
        "user": {
            "id": user_id,
            "username": username,
            "email": f"{username}@examplecorp.com",
            "department": department,
            "role": role,
            "account_status": "active"
        }
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def assign_app_access(username: str, role: str) -> str:
    """
    Assigns access to a standard set of applications based on the employee's role.

    Args:
        username (str): The user's system username (e.g., 'jane.doe').
        role (str): The job role of the employee.

    Returns:
        str: A JSON string confirming the applications assigned.
    """
    app_sets = {
        "Software Engineer": ["Jira", "GitHub", "Slack", "AWS Console", "Confluence"],
        "Marketing Manager": ["Salesforce", "Marketo", "Slack", "Google Analytics", "Asana"],
        "Sales Representative": ["Salesforce", "Slack", "Outreach.io", "LinkedIn Sales Navigator"]
    }
    apps = app_sets.get(role, ["Slack", "Microsoft 365"])
    response = {
        "status": "success",
        "message": f"Application access assigned to {username} for the {role} role.",
        "username": username,
        "assigned_apps": apps
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def deactivate_user_account(username: str) -> str:
    """
    Deactivates a user's account and revokes all application access for offboarding. This is a critical security action.

    Args:
        username (str): The user's system username to deactivate.

    Returns:
        str: A JSON string confirming the account deactivation and access revocation.
    """
    response = {
        "status": "success",
        "message": f"User account for {username} has been DEACTIVATED. All system access and application tokens have been revoked.",
        "username": username,
        "account_status": "deactivated",
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(response)