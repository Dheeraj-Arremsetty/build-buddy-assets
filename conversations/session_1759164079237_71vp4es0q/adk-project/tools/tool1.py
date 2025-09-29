# empower-demo/tools/customer_care/get_healthcare_benefits.py
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool(permission=ToolPermission.ADMIN)
def get_healthcare_benefits(plan: Plan, in_network: bool = None):
    """Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (Plan): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains details on coverage.
    """
    # In a real scenario, this would make an API call. Here, we generate synthetic data.
    all_benefits = [
        {'Coverage': 'Annual Deductible', 'HDHP (In-Network)': '$3,000', 'HDHP (Out-of-Network)': '$6,000', 'PPO (In-Network)': '$1,000'},
        {'Coverage': 'Out-of-Pocket Max', 'HDHP (In-Network)': '$7,000', 'HDHP (Out-of-Network)': '$14,000', 'PPO (In-Network)': '$5,000'},
        {'Coverage': 'Primary Care Visit', 'HDHP (In-Network)': '100% after deductible', 'HDHP (Out-of-Network)': '80% after deductible', 'PPO (In-Network)': '$30 co-pay'},
        {'Coverage': 'Specialist Visit', 'HDHP (In-Network)': '100% after deductible', 'HDHP (Out-of-Network)': '80% after deductible', 'PPO (In-Network)': '$50 co-pay'},
        {'Coverage': 'Emergency Room', 'HDHP (In-Network)': '$500 co-pay then 100%', 'HDHP (Out-of-Network)': '$500 co-pay then 80%', 'PPO (In-Network)': '$250 co-pay'}
    ]
    
    # Simple filtering logic based on input
    if plan == Plan.HDHP:
        return [b for b in all_benefits if 'HDHP' in ' '.join(b.keys())]
    elif plan == Plan.PPO:
        return [b for b in all_benefits if 'PPO' in ' '.join(b.keys())]
    else:
        return all_benefits