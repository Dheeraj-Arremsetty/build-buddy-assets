# product_info_provider.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="product_info_provider", description="Provides product information", permission=ToolPermission.ADMIN)
def product_info_provider(product_id: str) -> str:
    """Retrieves information about a specific product.

    Args:
        product_id (str): The unique identifier for the product.

    Returns:
        str: The detailed information about the product.
    """
    products = {
        "001": {"name": "Printer Model X", "price": "299.99", "features": "Fast printing, Wireless"},
        "002": {"name": "Scanner Model Y", "price": "199.99", "features": "High resolution, Portable"}
    }
    return json.dumps(products.get(product_id, "Product not found."))