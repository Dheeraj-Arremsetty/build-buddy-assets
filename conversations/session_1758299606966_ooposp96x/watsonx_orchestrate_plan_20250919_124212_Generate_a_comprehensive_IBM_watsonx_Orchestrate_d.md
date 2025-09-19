# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-19 12:42:12
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: The Virtual Barista Agent

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying a "Virtual Barista" agent using IBM watsonx Orchestrate. This demonstration is specifically designed for clients in the retail and food service industry to showcase how Orchestrate can automate and streamline the customer order-taking process. The Virtual Barista agent will act as a conversational AI, capable of presenting a menu, checking item availability, taking customer orders, and providing order status updates.

The plan leverages the IBM watsonx Orchestrate Agent Development Kit (ADK) to create a `native` agent equipped with a suite of custom Python tools. These tools will simulate interactions with a Point of Sale (POS) system by generating realistic, synthetic data for the menu, inventory, and order management. This approach provides a powerful and tangible example of how Orchestrate can be integrated into a client's existing operational workflows to enhance customer experience, improve efficiency, and reduce the workload on human staff. This revised plan addresses all previous gaps to ensure a complete and executable solution.

## 2. Prerequisites

Before beginning the implementation, ensure your environment is configured with the following prerequisites. This setup is crucial for a successful build and deployment process.

*   **IBM watsonx Orchestrate ADK Installed**: The Agent Development Kit is the core command-line tool used for creating, importing, and managing agents and tools. If not installed, follow the official documentation.
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Python Environment**: A working Python environment (version 3.9 or later) is required to create the custom tools.
*   **Configured Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured and logged in via the ADK CLI. This connects your local development to your Orchestrate instance.
    ```bash
    # Log in to your watsonx Orchestrate environment
    orchestrate login
    ```
*   **Project Directory**: Create a dedicated directory for the demo project to keep all files organized.
    ```bash
    mkdir barista_demo
    cd barista_demo
    mkdir agents tools
    ```

## 3. Step-by-Step Instructions

This plan is divided into four main steps: creating the dependencies file, building the individual Python tools, defining the agent's logic in a YAML file, and finally, importing everything into watsonx Orchestrate to bring the Virtual Barista to life.

### Step 3.1: Create Project Dependencies

Our Python tools will use the `pydantic` library for data validation and structuring, which is a best practice for creating robust tools in Orchestrate. Create a `requirements.txt` file in the root of your `barista_demo` directory to manage this dependency.

Create the file `requirements.txt`:
```text
# requirements.txt
pydantic
```

Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

### Step 3.2: Create the Python Tools

Tools are the foundational components that allow the agent to perform actions. We will create four distinct Python tools to simulate a complete order-taking workflow. Each tool will generate realistic synthetic data to mimic a real-world cafe environment.

---

#### Tool 1: Get Menu (`get_menu.py`)

**Business Value**: This tool provides the foundational capability for the agent to interact with customers by presenting the available products. It simulates a query to a POS or product catalog system, ensuring the customer is always shown an up-to-date list of items and prices. This is the first step in any sales conversation and is critical for customer engagement.

**Technical Implementation**: The `get_menu` function generates a static list of Pydantic `MenuItem` objects. Each object represents a menu item with its ID, name, category, and a dictionary of prices for different sizes. This structured data is easily interpreted by the LLM and can be formatted into a user-friendly list in the chat interface. The function requires no input and returns a JSON-serializable list.

Create the file `tools/get_menu.py`:

```python
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
```

---

#### Tool 2: Check Inventory (`check_inventory.py`)

**Business Value**: This tool is critical for managing customer expectations and preventing order failures. By checking real-time inventory before confirming an order, the agent avoids selling out-of-stock items, which improves customer satisfaction and operational efficiency. It simulates a direct lookup into an inventory management system.

**Technical Implementation**: The `check_inventory` function takes an `item_id` as input. It contains a mock inventory dictionary mapping item IDs to stock levels. The function returns an `InventoryStatus` object containing the item's stock status and the available quantity. This provides a clear, actionable response for the agent to proceed with or halt the order. An out-of-stock item is included for a comprehensive demo.

Create the file `tools/check_inventory.py`:

```python
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
```

---

#### Tool 3: Place Order (`place_order.py`)

**Business Value**: This is the core transactional tool that converts a customer request into a confirmed order. It automates the data entry process, reducing manual errors and speeding up service. The tool provides immediate confirmation with an order number, which is essential for tracking and customer assurance.

**Technical Implementation**: The `place_order` function accepts a list of `OrderItem` objects. It generates a unique, timestamp-based order ID, calculates the total cost, and simulates placing the order in a system. The function returns a confirmation object containing the new order ID, a summary, the total amount, and an estimated preparation time.

Create the file `tools/place_order.py`:

```python
# tools/place_order.py
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field
from typing import List, Dict

class OrderItem(BaseModel):
    item_id: str = Field(description="The unique ID of the item being ordered.")
    size: str = Field(description="The selected size of the item (e.g., 'medium').")
    quantity: int = Field(description="The number of units for this item.")

class OrderConfirmation(BaseModel):
    order_id: str = Field(description="The unique confirmation ID for the placed order.")
    status: str = Field(description="The initial status of the order.")
    items_summary: List[Dict] = Field(description="A summary of the items in the order.")
    total_cost: float = Field(description="The total cost of the order.")
    estimated_prep_time_minutes: int = Field(description="Estimated preparation time in minutes.")

@tool
def place_order(items: List[OrderItem]) -> OrderConfirmation:
    """
    Places a new order for a list of items.
    Use this tool after confirming the items with the customer and checking their availability.

    Args:
        items (List[OrderItem]): A list of items to include in the order.

    Returns:
        OrderConfirmation: A confirmation object with the order ID, status, and total cost.
    """
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    order_id = f"ORD-{timestamp}"
    
    # In a real scenario, you would fetch prices and calculate the total.
    # For the demo, we'll use a mock calculation.
    mock_total_cost = sum(item.quantity * 4.50 for item in items) # Average price

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
