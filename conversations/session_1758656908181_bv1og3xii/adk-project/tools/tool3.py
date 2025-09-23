# tools/scheduling_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import List, Dict
import datetime

@tool
def get_interviewer_availability(interviewer_name: str) -> List[Dict]:
    """
    Checks the calendar for an interviewer's availability for the upcoming week.

    Args:
        interviewer_name (str): The name of the interviewer (e.g., 'Sarah Jenkins').

    Returns:
        List[Dict]: A list of available time slots.
    """
    print(f"Checking calendar availability for {interviewer_name}...")
    # Mock data simulating calendar API response for the next 5 business days
    today = datetime.date.today()
    availability = []
    for i in range(1, 6):
        day = today + datetime.timedelta(days=i)
        if day.weekday() < 5: # Monday to Friday
            availability.append({"date": day.strftime('%Y-%m-%d'), "time": "10:00 AM", "duration_minutes": 60})
            availability.append({"date": day.strftime('%Y-%m-%d'), "time": "02:30 PM", "duration_minutes": 45})
    return availability

@tool
def send_interview_invite(candidate_name: str, interviewer_name: str, date: str, time: str, duration: int) -> Dict:
    """
    Sends a calendar invitation for an interview.

    Args:
        candidate_name (str): The name of the candidate.
        interviewer_name (str): The name of the interviewer.
        date (str): The date of the interview (YYYY-MM-DD).
        time (str): The time of the interview (e.g., '10:00 AM').
        duration (int): The duration of the interview in minutes.

    Returns:
        Dict: A confirmation message indicating the interview was scheduled.
    """
    print(f"Sending interview invite to {candidate_name} with {interviewer_name}...")
    return {
        "status": "Success",
        "message": f"Interview scheduled for {candidate_name} with {interviewer_name} on {date} at {time} for {duration} minutes. Invitation sent."
    }