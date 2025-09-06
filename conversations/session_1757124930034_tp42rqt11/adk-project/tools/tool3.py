from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="order_trigger", description="Triggers supply orders based on inventory levels", permission=ToolPermission.ADMIN)
def order_trigger() -> dict:
    """Automates supply ordering to maintain optimal inventory levels."""
    order_details = {
        "order_id": "ORD123456",
        "items": ["Toner", "Paper"],
        "order_date": "2023-10-15",
        "estimated_delivery": "2023-10-20"
    }
    return order_details