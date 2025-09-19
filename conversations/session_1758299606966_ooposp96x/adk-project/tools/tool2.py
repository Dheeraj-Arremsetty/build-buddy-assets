# tools/check_inventory.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

class InventoryStatus(BaseModel):
    item_id: str = Field(description="The unique identifier for the item checked.")
    is_in_stock: bool = Field(description="True if the item is in stock, otherwise False.")
    quantity_available: int = Field(description="The current stock level for the item.")

@tool
def check_inventory(item_id: str) -> InventoryStatus:
    """
    Checks the current stock level for a given menu item ID.
    Use this tool before placing an order to ensure the item is available.

    Args:
        item_id (str): The unique identifier of the menu item (e.g., 'cof-001').

    Returns:
        InventoryStatus: An object containing the stock status and available quantity.
    """
    # Synthetic inventory data. In a real scenario, this would call an API.
    mock_inventory = {
        "cof-001": 50, "cof-002": 35, "cof-003": 100,
        "tea-001": 40, "pst-001": 0, "pst-002": 25
    }
    quantity = mock_inventory.get(item_id, 0)
    
    return InventoryStatus(
        item_id=item_id,
        is_in_stock=quantity > 0,
        quantity_available=quantity
    )