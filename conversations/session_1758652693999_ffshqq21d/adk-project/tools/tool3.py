# tools/lms_tools.py
import json
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def enroll_in_onboarding_training(employee_name: str, department: str) -> str:
    """
    Enrolls a new employee in the standard set of onboarding training courses based on their department.

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.

    Returns:
        str: A JSON string confirming the courses the employee has been enrolled in.
    """
    base_courses = [
        {"course_id": "SEC101", "course_name": "New Hire Security Awareness Training"},
        {"course_id": "CND101", "course_name": "Corporate Code of Conduct"}
    ]
    department_courses = {
        "Engineering": [{"course_id": "ENG201", "course_name": "Introduction to Engineering Practices"}],
        "Sales": [{"course_id": "SLS201", "course_name": "CRM Best Practices and Usage"}]
    }
    enrollments = base_courses + department_courses.get(department, [])
    
    response = {
        "status": "success",
        "message": f"{employee_name} has been enrolled in {len(enrollments)} required onboarding courses.",
        "enrolled_courses": enrollments
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def check_training_completion(employee_name: str) -> str:
    """
    Checks the completion status of required training for a specific employee.

    Args:
        employee_name (str): The full name of the employee.

    Returns:
        str: A JSON string detailing the status of each required training course for the employee.
    """
    courses = [
        {"course_name": "New Hire Security Awareness Training", "status": random.choice(["Completed", "In Progress", "Not Started"]), "due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')},
        {"course_name": "Corporate Code of Conduct", "status": random.choice(["Completed", "In Progress"]), "due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')},
        {"course_name": "Introduction to Engineering Practices", "status": "Not Started", "due_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}
    ]
    response = {
        "employee_name": employee_name,
        "training_status_summary": f"Found {len(courses)} assigned courses.",
        "training_status": courses
    }
    return json.dumps(response)