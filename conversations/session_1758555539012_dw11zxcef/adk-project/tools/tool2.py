import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="check_stock_level", permission=ToolPermission.ADMIN)
def check_stock_level(item_name: str) -> dict:
    """
    Checks the current stock level for a specific item in the inventory system.

    Args:
        item_name (str): The name of the product to check (e.g., 'blonde espresso beans').

    Returns:
        dict: A dictionary containing the item name and its quantity on hand, or a 'not found' message.
    """
    try:
        with open('data/inventory.json', 'r') as f:
            inventory = json.load(f)
        for item in inventory:
            if item['item_name'].lower() == item_name.lower():
                return {"item": item['item_name'], "quantity": item['quantity_on_hand']}
        return {"item": item_name, "quantity": "not found"}
    except FileNotFoundError:
        return {"error": "Inventory data file not found."}