# tools/ingestion_tools.py
import pandas as pd
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a CSV file from the given path and returns its content as a list of records.

    Args:
        file_path (str): The full path to the CSV file to be read.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a row from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        # Convert NaN to None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        return df.to_dict('records')
    except FileNotFoundError:
        return [{"error": f"File not found at path: {file_path}"}]
    except Exception as e:
        return [{"error": f"An error occurred while reading the file: {str(e)}"}]

@tool(permission=ToolPermission.ADMIN)
def fetch_from_api(endpoint_url: str) -> List[Dict[str, Any]]:
    """
    Fetches customer data from a mock API endpoint.

    Args:
        endpoint_url (str): The URL of the API endpoint to fetch data from.

    Returns:
        List[Dict[str, Any]]: A list of customer records retrieved from the API.
    """
    # This is a mock implementation. In a real scenario, you would use the 'requests' library.
    print(f"Fetching data from mock API: {endpoint_url}")
    mock_api_data = [
        {"CustomerID": "API-101", "FirstName": "Alice", "LastName": "Johnson", "Email": "alice.j@email.com", "PhoneNumber": "(777) 111-2222", "State": "GA"},
        {"CustomerID": "API-102", "FirstName": "Bob", "LastName": "Williams", "Email": "bob.w@email.com", "PhoneNumber": "(888) 333-4444", "State": "WA"}
    ]
    return mock_api_data