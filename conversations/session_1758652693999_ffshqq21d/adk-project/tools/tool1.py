# tools/it_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_servicenow_ticket(employee_name: str, department: str, request_type: str, short_description: str) -> str:
    """
    Creates a ServiceNow incident ticket for a new employee request.

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.
        request_type (str): The type of request (e.g., 'Onboarding Hardware', 'Offboarding Asset Recovery').
        short_description (str): A brief summary of the request.

    Returns:
        str: A JSON string containing a confirmation message and the new ServiceNow ticket number and details.
    """
    ticket_id = f"INC{random.randint(10000, 99999)}"
    response = {
        "status": "success",
        "message": f"Successfully created ServiceNow ticket {ticket_id} for {employee_name}.",
        "ticket": {
            "id": ticket_id,
            "request_type": request_type,
            "status": "New",
            "assigned_to": "IT Support",
            "created_at": datetime.now().isoformat(),
            "short_description": short_description
        }
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def assign_hardware_package(employee_name: str, role: str) -> str:
    """
    Assigns and orders a standard hardware package based on the employee's role from the catalog.

    Args:
        employee_name (str): The full name of the employee.
        role (str): The job role of the employee (e.g., 'Software Engineer', 'Marketing Manager').

    Returns:
        str: A JSON string confirming the hardware package that has been ordered.
    """
    packages = {
        "Software Engineer": "16-inch MacBook Pro, 32-inch 4K Display, Mechanical Keyboard",
        "Marketing Manager": "13-inch MacBook Air, 27-inch external monitor",
        "Sales Representative": "14-inch Lenovo ThinkPad, Wireless Headset"
    }
    package_details = packages.get(role, "Standard Employee Laptop Package")
    order_id = f"HW-ORD-{random.randint(100000, 999999)}"
    
    response = {
        "status": "success",
        "message": f"Hardware package for {employee_name} ({role}) has been ordered.",
        "order_id": order_id,
        "package_details": package_details,
        "estimated_delivery": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def get_ticket_status(ticket_id: str) -> str:
    """
    Retrieves the current status and details of a given ServiceNow ticket.

    Args:
        ticket_id (str): The unique identifier for the ServiceNow ticket (e.g., 'INC12345').

    Returns:
        str: A JSON string with the ticket's details, current status, and update history.
    """
    statuses = ["New", "In Progress", "On Hold", "Resolved", "Closed"]
    created_date = datetime.now() - timedelta(days=random.randint(1, 5))
    
    response = {
        "ticket_id": ticket_id,
        "status": random.choice(statuses),
        "created_date": created_date.isoformat(),
        "last_updated": datetime.now().isoformat(),
        "short_description": "Employee Onboarding Request",
        "updates": [
            {"timestamp": (created_date + timedelta(hours=1)).isoformat(), "comment": "Ticket assigned to IT Support."},
            {"timestamp": (created_date + timedelta(days=1)).isoformat(), "comment": "Hardware order placed."}
        ]
    }
    return json.dumps(response)