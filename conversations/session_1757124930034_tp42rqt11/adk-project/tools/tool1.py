from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import random
import json

@tool(name="fleet_health_checker", description="Checks health of printer fleet using sensor data", permission=ToolPermission.ADMIN)
def fleet_health_checker() -> dict:
    """Collects sensor data to assess the health of the printer fleet."""
    data = {
        "fleet_status": "healthy" if random.random() > 0.2 else "issue_detected",
        "timestamp": "2023-10-15T10:00:00Z",
        "details": "All systems operational" if random.random() > 0.2 else "Paper jam detected in Printer 5"
    }
    return data