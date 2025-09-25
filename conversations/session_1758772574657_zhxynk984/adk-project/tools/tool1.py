# tools/triage_tools.py
import json
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock CMDB data source
MOCK_CMDB_DATA = {
    "prod-db-01": {
        "business_service": "Customer Billing Platform",
        "application_owner": "finance-app-owners@example.com",
        "service_tier": "Tier 1",
        "on_call_engineer": "jane.doe@example.com",
        "dependencies": ["prod-app-01", "prod-web-01"],
        "last_change_id": "CHG003456"
    },
    "prod-app-01": {
        "business_service": "Customer Billing Platform",
        "application_owner": "finance-app-owners@example.com",
        "service_tier": "Tier 1",
        "on_call_engineer": "john.smith@example.com",
        "dependencies": ["prod-db-01"],
        "last_change_id": "CHG003451"
    }
}

@tool(permission=ToolPermission.ADMIN)
def get_cmdb_details(hostname: str) -> str:
    """
    Retrieves critical business context for a given hostname from the CMDB.

    This tool queries the Configuration Management Database (CMDB) to enrich a technical alert
    with essential business information, such as the affected business service, the application
    owner, and service tier. This context is vital for assessing business impact and engaging
    the correct stakeholders during a major incident.

    Args:
        hostname (str): The hostname of the affected server (e.g., "prod-db-01").

    Returns:
        str: A JSON string containing the CMDB details for the specified hostname.
             Returns an error message if the hostname is not found.
    """
    print(f"Querying CMDB for hostname: {hostname}")
    details = MOCK_CMDB_DATA.get(hostname)
    if details:
        return json.dumps(details)
    else:
        return json.dumps({"error": f"Hostname '{hostname}' not found in CMDB."})