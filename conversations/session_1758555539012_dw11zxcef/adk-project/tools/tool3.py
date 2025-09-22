import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="find_available_employees", permission=ToolPermission.ADMIN)
def find_available_employees(shift_details: str) -> list:
    """
    Finds employees who are available to cover an open shift based on today's schedule.

    Args:
        shift_details (str): A description of the shift that needs coverage (e.g., '2 PM shift today'). This argument provides context but the tool currently checks for general availability today.

    Returns:
        list: A list of dictionaries, where each dictionary represents an available employee.
    """
    try:
        with open('data/schedules.json', 'r') as f:
            schedules = json.load(f)
        
        available_staff = [
            emp for emp in schedules if emp.get('is_available_today')
        ]
        return available_staff
    except FileNotFoundError:
        return [{"error": "Schedule data file not found."}]