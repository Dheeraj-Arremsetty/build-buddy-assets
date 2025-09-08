# order_status_checker.py
import json
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="order_status_checker", description="Checks the status of orders", permission=ToolPermission.ADMIN)
def order_status_checker(order_id: str) -> str:
    """Provides the current status of an order based on its ID.

    Args:
        order_id (str): The unique identifier for the order.

    Returns:
        str: The current status of the order.
    """
    statuses = ["Processing", "Shipped", "Delivered", "Cancelled"]
    return json.dumps({"order_id": order_id, "status": random.choice(statuses)})