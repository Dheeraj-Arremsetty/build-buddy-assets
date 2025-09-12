# tools/inventory_tools.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field

# Mock database of coffee shop inventory
_INVENTORY_DATA = {
    "espresso_beans": {"item": "Espresso Beans", "quantity": 25, "unit": "kg"},
    "oat_milk": {"item": "Oat Milk", "quantity": 12, "unit": "cartons"},
    "whole_milk": {"item": "Whole Milk", "quantity": 24, "unit": "cartons"},
    "vanilla_syrup": {"item": "Vanilla Syrup", "quantity": 8, "unit": "bottles"},
    "paper_cups": {"item": "12oz Paper Cups", "quantity": 450, "unit": "cups"},
}

class StockInfo(BaseModel):
    item: str = Field(description="The name of the inventory item.")
    quantity: int = Field(description="The current quantity in stock.")
    unit: str = Field(description="The unit of measurement for the quantity (e.g., kg, cartons).")

@tool
def check_stock_level(item_name: str) -> StockInfo:
    """
    Checks the current stock level for a given inventory item in the coffee shop.

    Args:
        item_name (str): The name of the item to check. Should be a simple identifier like 'oat_milk' or 'espresso_beans'.

    Returns:
        StockInfo: An object containing the item name, quantity, and unit of the stock.
    """
    normalized_item = item_name.lower().replace(" ", "_")
    
    if normalized_item in _INVENTORY_DATA:
        return StockInfo(**_INVENTORY_DATA[normalized_item])
    else:
        # In a real scenario, you might raise an error or return a specific "not found" message.
        # For this demo, we return a zero quantity.
        return StockInfo(item=item_name, quantity=0, unit="units")