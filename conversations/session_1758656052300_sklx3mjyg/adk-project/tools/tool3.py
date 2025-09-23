import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def get_role_based_training_plan(role: str) -> str:
    """
    Retrieves the mandatory training plan for a specific job role.

    Args:
        role (str): The job role of the new hire.

    Returns:
        str: A JSON string listing the required courses for the role.
    """
    # Mock data for training plans
    plans = {
        "software engineer": [
            {"course_id": "SEC101", "course_name": "Secure Software Development Lifecycle", "duration_hours": 8},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "GIT300", "course_name": "Advanced Git Workflow", "duration_hours": 4}
        ],
        "sales associate": [
            {"course_id": "CRM100", "course_name": "Introduction to Salesforce", "duration_hours": 16},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "SALES210", "course_name": "Consultative Selling Techniques", "duration_hours": 8}
        ],
        "default": [
            {"course_id": "HR001", "course_name": "New Hire Orientation", "duration_hours": 2},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "ITSEC099", "course_name": "Cybersecurity Awareness", "duration_hours": 1.5}
        ]
    }
    
    training_plan = plans.get(role.lower(), plans["default"])
    response = {
        "role": role,
        "training_plan": training_plan
    }
    return json.dumps(response, indent=2)


@tool(permission=ToolPermission.ADMIN)
def enroll_in_course(employee_name: str, course_id: str, course_name: str) -> str:
    """
    Enrolls a new hire into a specific training course in the LMS.

    Args:
        employee_name (str): The full name of the new hire.
        course_id (str): The unique ID of the course.
        course_name (str): The name of the course.

    Returns:
        str: A JSON string confirming the enrollment.
    """
    enrollment_id = f"ENRL-{''.join(random.choices('0123456789', k=9))}"
    response = {
        "status": "Success",
        "message": f"{employee_name} has been successfully enrolled in '{course_name}'.",
        "enrollment_id": enrollment_id,
        "course_id": course_id,
        "enrollment_timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(response, indent=2)