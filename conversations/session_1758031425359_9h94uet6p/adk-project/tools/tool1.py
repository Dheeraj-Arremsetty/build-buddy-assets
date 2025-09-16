import json
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool(name="get_healthcare_benefits", permission=ToolPermission.ADMIN)
def get_healthcare_benefits(plan: Plan) -> str:
    """
    Retrieves a comprehensive list of health benefits data for a specific plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (str): The plan the user is asking about. Must be one of "HDHP", "HDHP Plus", or "PPO".

    Returns:
        str: A JSON string representing a list of dictionaries with benefit details for the requested plan.
    """
    benefits_data = {
        "HDHP": [
            {"Coverage": "Annual Deductible", "In-Network": "$3,000", "Out-of-Network": "$6,000"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$6,000", "Out-of-Network": "$12,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "100% after deductible", "Out-of-Network": "70% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "90% after deductible", "Out-of-Network": "60% after deductible"},
        ],
        "HDHP Plus": [
            {"Coverage": "Annual Deductible", "In-Network": "$2,000", "Out-of-Network": "$4,000"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$5,000", "Out-of-Network": "$10,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "$40 Copay", "Out-of-Network": "70% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "$60 Copay", "Out-of-Network": "60% after deductible"},
        ],
        "PPO": [
            {"Coverage": "Annual Deductible", "In-Network": "$1,000", "Out-of-Network": "$2,500"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$4,000", "Out-of-Network": "$8,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "$25 Copay", "Out-of-Network": "80% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "$50 Copay", "Out-of-Network": "70% after deductible"},
        ]
    }
    
    result = benefits_data.get(plan, [])
    return json.dumps(result)