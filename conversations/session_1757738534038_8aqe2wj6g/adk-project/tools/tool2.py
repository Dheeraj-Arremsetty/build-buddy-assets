import requests
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define the base URL for the mock API
BASE_URL = "http://127.0.0.1:5001"

@tool(permission=ToolPermission.ADMIN)
def get_company_financials(company_ticker: str) -> str:
    """
    Retrieves key financial data for a given company ticker from the internal S&P mock database.
    This includes market cap, P/E ratio, EPS, and analyst ratings.

    Args:
        company_ticker (str): The stock ticker symbol for the company (e.g., 'QLI').

    Returns:
        str: A JSON string containing the company's financial data or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/financials/{company_ticker}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})

@tool(permission=ToolPermission.ADMIN)
def get_sector_performance(sector_name: str) -> str:
    """
    Retrieves performance data for a specific market sector from the internal S&P mock database.
    This includes YTD performance, daily change, key drivers, and outlook.

    Args:
        sector_name (str): The name of the market sector to query (e.g., 'Semiconductors', 'Automotive').

    Returns:
        str: A JSON string containing the sector's performance data or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/sector/{sector_name}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})