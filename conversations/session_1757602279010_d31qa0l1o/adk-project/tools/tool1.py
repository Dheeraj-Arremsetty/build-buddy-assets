# tools/corepower_tools.py

import json
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_class_schedule", permission=ToolPermission.ADMIN)
def get_class_schedule(studio_location: str, day: str) -> list[dict]:
    """
    Retrieves the class schedule for a specific CorePower studio location and a given day.

    Args:
        studio_location (str): The CorePower studio location to search for (e.g., "Downtown", "Northside").
        day (str): The desired day for the schedule. Can be "today" or "tomorrow".

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a class with its name, instructor, and start time. Returns an empty list if no classes are found.
    """
    try:
        with open('mock_data/class_schedule.json', 'r') as f:
            all_classes = json.load(f)

        # Simple filter logic based on studio and day
        # In a real scenario, this would involve more complex date handling
        filtered_classes = [
            cls for cls in all_classes
            if cls['studio'].lower() == studio_location.lower() and cls['day'].lower() == day.lower()
        ]
        
        if not filtered_classes:
            return [{"status": "No classes found for the specified criteria."}]
            
        return filtered_classes
    except FileNotFoundError:
        return [{"error": "Schedule data file not found."}]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {str(e)}"}]


@tool(name="get_member_details", permission=ToolPermission.ADMIN)
def get_member_details(member_id: str) -> dict:
    """
    Retrieves detailed information for a specific member using their unique member ID.

    Args:
        member_id (str): The unique identifier for the member (e.g., "CP7890").

    Returns:
        dict: A dictionary containing the member's details, including name, membership level, and join date. Returns an error message if the member is not found.
    """
    try:
        with open('mock_data/member_profiles.json', 'r') as f:
            all_members = json.load(f)

        member_details = next((member for member in all_members if member['member_id'] == member_id), None)

        if member_details:
            return member_details
        else:
            return {"error": f"Member with ID '{member_id}' not found."}
    except FileNotFoundError:
        return {"error": "Member profiles data file not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}