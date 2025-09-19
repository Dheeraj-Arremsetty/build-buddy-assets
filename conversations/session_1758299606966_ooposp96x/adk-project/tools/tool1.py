# tools/get_menu.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field
from typing import List, Dict

class MenuItem(BaseModel):
    item_id: str = Field(description="The unique identifier for the menu item.")
    name: str = Field(description="The name of the menu item.")
    category: str = Field(description="The category of the item (e.g., 'Coffee', 'Pastry').")
    prices: Dict[str, float] = Field(description="A dictionary of available sizes and their prices.")

@tool
def get_menu() -> List[MenuItem]:
    """
    Retrieves the full menu of available coffee, tea, and pastry items with their prices.
    Use this tool when a customer asks what is available or wants to see the menu.

    Returns:
        List[MenuItem]: A list of available menu items, including their name, category, and prices.
    """
    menu_data = [
        {"item_id": "cof-001", "name": "Latte", "category": "Coffee", "prices": {"small": 3.50, "medium": 4.25, "large": 5.00}},
        {"item_id": "cof-002", "name": "Cappuccino", "category": "Coffee", "prices": {"small": 3.50, "medium": 4.25, "large": 5.00}},
        {"item_id": "cof-003", "name": "Espresso", "category": "Coffee", "prices": {"single": 2.75, "double": 3.25}},
        {"item_id": "tea-001", "name": "Chai Tea", "category": "Tea", "prices": {"small": 3.00, "medium": 3.75, "large": 4.50}},
        {"item_id": "pst-001", "name": "Croissant", "category": "Pastry", "prices": {"one_size": 2.50}},
        {"item_id": "pst-002", "name": "Muffin", "category": "Pastry", "prices": {"one_size": 2.75}}
    ]
    return [MenuItem(**item) for item in menu_data]