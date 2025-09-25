# empower_demo/tools/customer_care/get_healthcare_benefits.py

from enum import Enum
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool
def get_healthcare_benefits(plan: Plan, in_network: bool = None):
    """Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (str, optional): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
            If not provided, all plans will be returned.
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains benefit details.
    """
    # In a real scenario, this would call a live API. We are using a mock service.
    try:
        resp = requests.get(
            'https://get-benefits-data.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud/',
            params={
                'plan': plan,
                'in_network': in_network
            }
        )
        resp.raise_for_status()
        return resp.json()['benefits']
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve healthcare benefits: {str(e)}"}