import csv
import json
import os
from typing import List
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

# --- Pydantic Models for Structured Output ---
class ToolError(BaseModel):
    error: str = Field(description="Description of the error that occurred.")

class FeedbackEntry(BaseModel):
    date: str
    rating: int
    comment: str

# --- Tool Implementation ---
FEEDBACK_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'mock_data', 'feedback.csv')

@tool(name="get_customer_feedback", description="Retrieves recent customer feedback from the store's feedback system.")
def get_customer_feedback() -> List[FeedbackEntry] | ToolError:
    """
    Fetches raw customer feedback entries from the past week.

    Returns:
        List[FeedbackEntry] | ToolError: A list of structured feedback objects or an error.
    """
    feedback_list = []
    try:
        with open(FEEDBACK_DATA_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure rating is an integer
                row['rating'] = int(row['rating'])
                feedback_list.append(FeedbackEntry(**row))
        return feedback_list
    except FileNotFoundError:
        return ToolError(error="Customer feedback file not found.")
    except Exception as e:
        return ToolError(error=f"Failed to process feedback file: {e}")