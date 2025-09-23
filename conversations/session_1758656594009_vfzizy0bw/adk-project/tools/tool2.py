import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

SOFTWARE_CATALOG_FILE = 'data/software.json'

def _load_software_catalog():
    """Helper function to load software data from the JSON file."""
    try:
        with open(SOFTWARE_CATALOG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@tool(permission=ToolPermission.ADMIN)
def check_license_availability(software_name: str) -> str:
    """
    Checks if there are available licenses for a given piece of software in the catalog.

    Args:
        software_name (str): The name of the software to check (e.g., 'Microsoft Visio').

    Returns:
        str: A message indicating whether licenses are available, not available, or if the software is not found.
    """
    catalog = _load_software_catalog()
    for software in catalog:
        if software['software_name'].lower() == software_name.lower():
            available_licenses = software['total_licenses'] - software['used_licenses']
            if available_licenses > 0:
                return f"Yes, there are {available_licenses} licenses available for {software_name}."
            else:
                return f"No, there are currently no available licenses for {software_name}."
    return f"Software named '{software_name}' was not found in the catalog."

@tool(permission=ToolPermission.ADMIN)
def request_software_install(software_name: str, user_email: str) -> str:
    """
    Submits a request for a software installation after checking for license availability. If a license is available, it simulates creating a service ticket.

    Args:
        software_name (str): The name of the software being requested.
        user_email (str): The email of the user requesting the software.

    Returns:
        str: A confirmation message with a ticket number if the request is successful, or an error message if no licenses are available.
    """
    catalog = _load_software_catalog()
    software_found = False
    for software in catalog:
        if software['software_name'].lower() == software_name.lower():
            software_found = True
            available_licenses = software['total_licenses'] - software['used_licenses']
            if available_licenses > 0:
                # Simulate ticket creation
                ticket_id = f"INC{random.randint(10000, 99999)}"
                # In a real system, we would decrement the license count here.
                # For the demo, we won't modify the file to keep it repeatable.
                return f"Request approved. A support ticket ({ticket_id}) has been created to install {software_name} for {user_email}. The IT team will be in touch shortly."
            else:
                return f"Request denied for {software_name}. No licenses are currently available. Please contact IT for alternatives."
    
    if not software_found:
        return f"Cannot process request. Software '{software_name}' is not in our catalog."