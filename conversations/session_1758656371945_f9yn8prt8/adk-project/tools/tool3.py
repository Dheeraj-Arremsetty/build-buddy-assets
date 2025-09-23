# ld_tools.py
import json
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def enroll_in_training(employee_id: str, role: str) -> str:
    """
    Enrolls a new hire in mandatory company and role-specific training courses.

    This tool automates a key compliance and development step. It checks the new hire's role and
    assigns them to the correct learning paths, such as 'Compliance 101' and 'Intro to Engineering Practices'.

    Args:
        employee_id (str): The unique ID of the new employee.
        role (str): The job title of the new hire to determine relevant training.

    Returns:
        str: A JSON string confirming the list of enrolled courses.
    """
    courses = ["Company Onboarding", "IT Security Awareness", "Code of Conduct"]
    if "developer" in role.lower() or "engineer" in role.lower():
        courses.append("Secure Coding Practices")
    
    confirmation = {
        "status": "Success",
        "employee_id": employee_id,
        "enrolled_courses": courses
    }
    return json.dumps(confirmation)

@tool(permission=ToolPermission.ADMIN)
def schedule_intro_meetings(employee_id: str, full_name: str, manager: str) -> str:
    """
    Schedules introductory meetings for the new hire with key team members.

    This tool facilitates team integration by automatically setting up crucial initial meetings. It simulates
    checking calendar availability to schedule a 'Welcome Lunch' and a '1-on-1 with Manager'.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The name of the new hire.
        manager (str): The name of the direct manager.

    Returns:
        str: A JSON string confirming the scheduled meetings.
    """
    today = datetime.utcnow()
    meetings = [
        {
            "title": f"Welcome Meeting: {full_name} & Team",
            "attendees": [full_name, manager, "Team DL"],
            "time": (today + timedelta(days=2)).strftime('%Y-%m-%d %H:%M UTC')
        },
        {
            "title": f"1-on-1: {full_name} & {manager}",
            "attendees": [full_name, manager],
            "time": (today + timedelta(days=3)).strftime('%Y-%m-%d %H:%M UTC')
        }
    ]
    confirmation = {
        "status": "Success",
        "employee_id": employee_id,
        "scheduled_meetings": meetings
    }
    return json.dumps(confirmation)