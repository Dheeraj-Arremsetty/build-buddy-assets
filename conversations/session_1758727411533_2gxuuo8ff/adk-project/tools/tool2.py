import requests
import json
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# --- Tool 1: Check Part Inventory ---

@tool
def check_part_inventory(part_number: str) -> dict:
    """
    Checks the inventory level and location for a given aircraft part number by calling the inventory API.

    Args:
        part_number (str): The unique identifier for the aircraft part, for example, 'HG-455B'.

    Returns:
        dict: The inventory details including quantity, location, and description, or an error message if not found.
    """
    api_url = f"http://127.0.0.1:5000/inventory/{part_number}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": f"Part number '{part_number}' not found in inventory."}
        else:
            return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"API connection error: {req_err}"}

# --- Tool 2: Log Maintenance Task ---

@tool
def log_maintenance_task(aircraft_id: str, task_description: str) -> dict:
    """
    Logs a completed maintenance task for a specific aircraft into the maintenance record system.

    Args:
        aircraft_id (str): The tail number or unique identifier of the aircraft, e.g., 'N505DN'.
        task_description (str): A clear and concise description of the maintenance task performed.

    Returns:
        dict: A confirmation message with a log ID and timestamp.
    """
    # In a real system, this would write to a database or a secure log file.
    # For this demo, we simulate the log entry and return a confirmation.
    log_entry = {
        "log_id": f"LOG-{int(datetime.now().timestamp())}",
        "timestamp": datetime.now().isoformat(),
        "aircraft_id": aircraft_id,
        "task_description": task_description,
        "status": "LOGGED_SUCCESSFULLY"
    }
    
    # Simulate logging by printing to the console
    print(f"MAINTENANCE LOG: {json.dumps(log_entry)}")
    
    return log_entry