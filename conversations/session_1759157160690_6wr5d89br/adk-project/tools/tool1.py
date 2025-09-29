# tools/shipment_tools.py
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# --- Synthetic Data Generation ---
def _generate_shipments():
    """Generates a list of realistic synthetic shipment data."""
    statuses = ["In Transit", "Customs Hold", "Delivered", "Delayed", "At Port"]
    shipments = []
    for i in range(1, 11):
        shipment_id = f"SHP-GL-{i:03d}"
        origin = random.choice(["Shanghai, CN", "Rotterdam, NL", "Los Angeles, US", "Singapore, SG"])
        destination = random.choice(["New York, US", "Hamburg, DE", "Dubai, AE", "Santos, BR"])
        # Ensure origin and destination are not the same
        while origin == destination:
            destination = random.choice(["New York, US", "Hamburg, DE", "Dubai, AE", "Santos, BR"])
            
        status = random.choice(statuses)
        details = {
            "SHP-GL-002": "Awaiting updated commercial invoice.",
            "SHP-GL-005": "Weather delay at origin port."
        }.get(shipment_id, "On schedule.")

        shipments.append({
            "shipment_id": shipment_id,
            "origin": origin,
            "destination": destination,
            "current_status": status,
            "status_details": details,
            "estimated_delivery": (datetime.now() + timedelta(days=random.randint(5, 25))).strftime('%Y-%m-%d'),
            "carrier": "Oceanic Freight Masters"
        })
    return shipments

_shipment_database = _generate_shipments()

@tool(permission=ToolPermission.ADMIN)
def get_shipment_details(shipment_id: str) -> str:
    """
    Retrieves detailed information for a specific shipment using its unique shipment ID.

    This tool is essential for getting a real-time snapshot of a shipment's status, location, and other critical details.

    Args:
        shipment_id (str): The unique identifier for the shipment (e.g., 'SHP-GL-001').

    Returns:
        str: A JSON string containing the shipment details, or an error message if not found.
    """
    for shipment in _shipment_database:
        if shipment["shipment_id"] == shipment_id:
            return json.dumps(shipment)
    return json.dumps({"error": f"Shipment with ID '{shipment_id}' not found."})

@tool(permission=ToolPermission.ADMIN)
def get_shipment_history(shipment_id: str) -> str:
    """
    Fetches the complete event history for a given shipment ID.

    This provides a detailed audit trail of a shipment's journey, which is crucial for root cause analysis of delays or issues.

    Args:
        shipment_id (str): The unique identifier for the shipment.

    Returns:
        str: A JSON string containing the list of historical events for the shipment.
    """
    if not any(s['shipment_id'] == shipment_id for s in _shipment_database):
        return json.dumps({"error": f"Shipment with ID '{shipment_id}' not found."})

    history = [
        {"timestamp": (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d %H:%M'), "event": "Shipment Created", "location": "Shanghai, CN"},
        {"timestamp": (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d %H:%M'), "event": "Departed Origin Port", "location": "Shanghai, CN"},
        {"timestamp": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M'), "event": "Arrived at Destination Port", "location": "Los Angeles, US"},
        {"timestamp": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M'), "event": "Held by Customs", "location": "Los Angeles, US", "details": "Missing Commercial Invoice"},
    ]
    return json.dumps(history)

@tool(permission=ToolPermission.ADMIN)
def update_shipment_status(shipment_id: str, new_status: str, details: str) -> str:
    """

    Updates the status and details of a specific shipment.

    This tool allows the agent to take action, such as resolving a hold or updating the status after an issue is fixed.

    Args:
        shipment_id (str): The unique identifier for the shipment to update.
        new_status (str): The new status to set for the shipment (e.g., 'In Transit', 'Customs Cleared').
        details (str): A description of the reason for the status update.

    Returns:
        str: A JSON string confirming the update or returning an error.
    """
    for shipment in _shipment_database:
        if shipment["shipment_id"] == shipment_id:
            shipment["current_status"] = new_status
            shipment["status_details"] = details
            shipment["last_updated"] = datetime.now().isoformat()
            return json.dumps({"success": True, "updated_shipment": shipment})
    return json.dumps({"error": f"Shipment with ID '{shipment_id}' not found."})