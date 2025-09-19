import json
import os
from typing import List, Dict
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

# --- Pydantic Models for Structured Output ---
class ToolError(BaseModel):
    error: str = Field(description="Description of the error that occurred.")

class Employee(BaseModel):
    employee_id: str
    name: str
    role: str
    availability: List[str]

class PeakHoursAnalysis(BaseModel):
    analysis: str = Field(description="A summary of the store's peak business hours based on sales data.")

class WeeklySchedule(BaseModel):
    schedule: Dict[str, Dict[str, List[str]]] = Field(description="The weekly schedule, organized by day and shift (AM/PM).")
    scheduling_notes: str = Field(description="Notes regarding how the schedule was constructed, including any special considerations.")

# --- Tool Implementation ---
EMPLOYEE_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'mock_data', 'employees.json')

@tool(name="get_employee_availability", description="Retrieves the weekly availability for all employees.")
def get_employee_availability() -> List[Employee] | ToolError:
    """
    Fetches the list of all employees and their scheduled availability for the week.

    Returns:
        List[Employee] | ToolError: A list of structured employee objects or an error.
    """
    try:
        with open(EMPLOYEE_DATA_PATH, 'r') as f:
            data = json.load(f)
        return [Employee(**emp) for emp in data]
    except FileNotFoundError:
        return ToolError(error="Employee data file not found.")
    except Exception as e:
        return ToolError(error=f"Failed to parse employee data: {e}")

@tool(name="get_peak_hours", description="Identifies store peak hours based on sales data.")
def get_peak_hours() -> PeakHoursAnalysis:
    """
    Analyzes sales data to determine peak business hours. For this demo, it returns a predefined peak period.

    Returns:
        PeakHoursAnalysis: A structured object with the peak hours analysis.
    """
    return PeakHoursAnalysis(analysis="Peak hours are identified as Weekday Mornings (8am-11am) due to high sales of brewed coffee and espresso drinks.")

@tool(name="draft_schedule", description="Generates a draft weekly schedule based on employee availability and peak hours.")
def draft_schedule(staffing_notes: str) -> WeeklySchedule | ToolError:
    """
    Creates a draft schedule, ensuring extra coverage during peak hours and considering any specific notes.

    Args:
        staffing_notes (str): Specific instructions or context for generating the schedule, such as "add extra staff for morning rush".

    Returns:
        WeeklySchedule | ToolError: A structured schedule object or an error.
    """

    try:
        with open(EMPLOYEE_DATA_PATH, 'r') as f:
            employees = json.load(f)
    except FileNotFoundError:
        return ToolError(error="Employee data file not found.")

    schedule_data = {
        "Monday": {"AM": [], "PM": []}, "Tuesday": {"AM": [], "PM": []},
        "Wednesday": {"AM": [], "PM": []}, "Thursday": {"AM": [], "PM": []},
        "Friday": {"AM": [], "PM": []}, "Saturday": {"AM": [], "PM": []},
        "Sunday": {"AM": [], "PM": []}
    }

    for emp in employees:
        for slot in emp['availability']:
            day, shift = slot.split('-')
            day_map = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
            day_full = day_map.get(day)
            if day_full:
                if shift == "AllDay":
                    schedule_data[day_full]["AM"].append(emp['name'])
                    schedule_data[day_full]["PM"].append(emp['name'])
                else:
                    schedule_data[day_full][shift].append(emp['name'])
    
    notes = f"Draft schedule created. Based on the instruction '{staffing_notes}', an extra barista has been scheduled for Friday morning to cover the anticipated peak rush."
    schedule_data["Friday"]["AM"].append("ADDITIONAL_BARISTA_COVERAGE")

    return WeeklySchedule(schedule=schedule_data, scheduling_notes=notes)