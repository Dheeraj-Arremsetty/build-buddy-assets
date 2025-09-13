import requests
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define the base URL for the mock API
BASE_URL = "http://127.0.0.1:5001"

@tool(permission=ToolPermission.ADMIN)
def fetch_market_news(query: str) -> str:
    """
    Gathers the latest news articles and press releases related to a specific market event or company.

    Args:
        query (str): The search term for the news, such as a company name or event description (e.g., 'QuantumLeap Inc.', 'trade tariffs').

    Returns:
        str: A JSON string containing a list of relevant news articles or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/news", params={"q": query})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})