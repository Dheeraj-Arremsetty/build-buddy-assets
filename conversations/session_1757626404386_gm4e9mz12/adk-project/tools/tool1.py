import json
from typing import List, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define paths to our mock data files
TEACHERS_FILE = 'data/teachers.json'
SCHEDULE_FILE = 'data/schedule.json'

def _load_data(file_path: str) -> List[Dict]:
    """Helper function to load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_data(file_path: str, data: List[Dict]):
    """Helper function to save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

@tool(name="find_class_details", permission=ToolPermission.ADMIN)
def find_class_details(teacher_name: str, class_time: str, studio_location: str) -> Optional[Dict]:
    """
    Finds specific details for a class based on the original teacher, time, and location.

    This tool is essential for initiating the substitute process. It retrieves the unique class ID and required certification format, which are necessary inputs for finding a suitable substitute and updating the schedule.

    Args:
        teacher_name (str): The first name of the teacher who needs a substitute (e.g., "Sarah").
        class_time (str): The start time of the class in ISO format (e.g., "2024-09-25T18:00:00Z").
        studio_location (str): The location of the studio (e.g., "LoDo").

    Returns:
        Optional[Dict]: A dictionary containing class details ('class_id', 'class_name', 'assigned_teacher_id') or None if not found.
    """
    schedule = _load_data(SCHEDULE_FILE)
    teachers = _load_data(TEACHERS_FILE)
    
    teacher_id = None
    for teacher in teachers:
        if teacher_name.lower() in teacher['name'].lower():
            teacher_id = teacher['teacher_id']
            break
            
    if not teacher_id:
        return None

    for class_info in schedule:
        if (class_info['assigned_teacher_id'] == teacher_id and
            class_info['start_time'] == class_time and
            class_info['studio_location'].lower() == studio_location.lower()):
            return class_info
            
    return None

@tool(name="find_available_subs", permission=ToolPermission.ADMIN)
def find_available_subs(class_name: str, original_teacher_id: str) -> List[Dict]:
    """
    Finds available and certified substitute teachers for a specific class format.

    This tool automates the most critical step: intelligent matching. It filters the entire teacher roster to find instructors who hold the correct certification for the class (e.g., "Yoga Sculpt") and are marked as available, ensuring class quality is maintained.

    Args:
        class_name (str): The name/format of the class needing a sub (e.g., "C2", "Yoga Sculpt").
        original_teacher_id (str): The ID of the teacher who cannot teach the class, to exclude them from the search.

    Returns:
        List[Dict]: A list of teacher objects who are available and certified, excluding the original teacher.
    """
    teachers = _load_data(TEACHERS_FILE)
    available_subs = []
    
    for teacher in teachers:
        if (teacher['is_available_for_subbing'] and
            class_name in teacher['certifications'] and
            teacher['teacher_id'] != original_teacher_id):
            available_subs.append({
                "teacher_id": teacher["teacher_id"],
                "name": teacher["name"],
                "phone_number": teacher["phone_number"]
            })
            
    return available_subs

@tool(name="update_class_schedule", permission=ToolPermission.ADMIN)
def update_class_schedule(class_id: str, new_teacher_id: str) -> Dict:
    """
    Updates the assigned teacher for a specific class in the master schedule.

    This tool closes the loop on the workflow. Once a substitute is confirmed, this function updates the system of record (our mock schedule.json), ensuring that all studio systems are synchronized and accurate. This prevents confusion and ensures a smooth class experience.

    Args:
        class_id (str): The unique identifier of the class to update.
        new_teacher_id (str): The unique identifier of the new substitute teacher.

    Returns:
        Dict: A confirmation message indicating success or failure.
    """
    schedule = _load_data(SCHEDULE_FILE)
    class_found = False
    for class_info in schedule:
        if class_info['class_id'] == class_id:
            class_info['assigned_teacher_id'] = new_teacher_id
            class_found = True
            break
            
    if class_found:
        _save_data(SCHEDULE_FILE, schedule)
        return {"status": "Success", "message": f"Class {class_id} has been updated with new teacher {new_teacher_id}."}
    else:
        return {"status": "Error", "message": f"Class with ID {class_id} not found."}