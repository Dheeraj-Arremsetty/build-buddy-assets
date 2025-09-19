import json
import os
from datetime import datetime
from typing import List, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

# --- Pydantic Models for Structured Output ---
class ToolError(BaseModel):
    error: str = Field(description="Description of the error that occurred.")

class SalesData(BaseModel):
    product_name: str = Field(description="The name of the product.")
    sales_yesterday: int = Field(description="The number of units sold yesterday.")

class InventoryStatus(BaseModel):
    product_name: str = Field(description="The name of the product.")
    stock_level: int = Field(description="The current number of units in stock.")
    reorder_threshold: int = Field(description="The stock level at which a reorder is recommended.")

class ReorderConfirmation(BaseModel):
    status: str = Field(description="The outcome of the reorder request.")
    reorder_id: Optional[str] = Field(None, description="The unique ID for the created reorder request.")
    product_name: str = Field(description="The name of the product.")
    message: str = Field(description="A descriptive message about the action taken.")

# --- Tool Implementation ---
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'mock_data', 'sales_inventory.json')

def _load_data():
    """Helper function to load mock data from the JSON file."""
    try:
        with open(MOCK_DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@tool(name="get_sales_data", description="Retrieves the sales figures for a specific product from yesterday.")
def get_sales_data(product_name: str) -> SalesData | ToolError:
    """
    Retrieves the number of units sold for a given product on the previous day.

    Args:
        product_name (str): The name of the product to query (e.g., "Venti Pumpkin Spice Latte").

    Returns:
        SalesData | ToolError: A structured object with sales data or an error.
    """
    data = _load_data()
    for item in data:
        if product_name.lower() in item['name'].lower():
            return SalesData(product_name=item['name'], sales_yesterday=item['sales_yesterday'])
    return ToolError(error=f"Product '{product_name}' not found.")

@tool(name="get_inventory_levels", description="Checks the current stock level for a given product.")
def get_inventory_levels(product_name: str) -> InventoryStatus | ToolError:
    """
    Retrieves the current stock level and reorder threshold for a given product.

    Args:
        product_name (str): The name of the product to check (e.g., "oat milk").

    Returns:
        InventoryStatus | ToolError: A structured object with inventory status or an error.
    """
    data = _load_data()
    for item in data:
        if product_name.lower() in item['name'].lower():
            return InventoryStatus(
                product_name=item['name'],
                stock_level=item['stock_level'],
                reorder_threshold=item['reorder_threshold']
            )
    return ToolError(error=f"Product '{product_name}' not found.")

@tool(name="create_reorder_request", description="Creates a reorder request for a product if its stock is below the threshold.")
def create_reorder_request(product_name: str) -> ReorderConfirmation | ToolError:
    """
    Checks product stock and creates a reorder request if the level is at or below the threshold.

    Args:
        product_name (str): The name of the product to reorder.

    Returns:
        ReorderConfirmation | ToolError: A structured object confirming the action or an error.
    """
    data = _load_data()
    for item in data:
        if product_name.lower() in item['name'].lower():
            if item['stock_level'] <= item['reorder_threshold']:
                reorder_id = f"RO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                return ReorderConfirmation(
                    status="Reorder Request Created",
                    reorder_id=reorder_id,
                    product_name=item['name'],
                    message=f"Reorder created for {item['name']} (Stock: {item['stock_level']}, Threshold: {item['reorder_threshold']})."
                )
            else:
                return ReorderConfirmation(
                    status="No Action Needed",
                    product_name=item['name'],
                    message="Stock level is above the reorder threshold."
                )
    return ToolError(error=f"Product '{product_name}' not found.")