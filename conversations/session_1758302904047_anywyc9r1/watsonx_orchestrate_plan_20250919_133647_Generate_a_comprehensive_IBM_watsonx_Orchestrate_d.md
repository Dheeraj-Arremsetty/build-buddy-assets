# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-19 13:36:47
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy AI Operations Assistant

## Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying the "Barista Buddy AI Operations Assistant," a multi-agent solution tailored for the client's coffee shop operations. This Proof of Concept (POC) demonstrates the power of IBM watsonx Orchestrate to streamline daily tasks, automate inventory management, and provide instant knowledge access for staff. The proposed architecture leverages a supervisor agent to delegate tasks to specialized collaborator agents, showcasing a sophisticated and scalable AI pattern. By following this plan, we will create a functional demo that directly addresses the client's business goals: increasing operational efficiency by 25-35%, reducing waste through proactive inventory monitoring, and empowering employees with on-demand training and support. This revised plan is a complete implementation, addressing all components of the proposed architecture.

## Prerequisites

Before beginning, ensure your development environment is correctly set up. This is crucial for a smooth implementation process.

1.  **Python Installation**: Ensure you have Python 3.9 or later installed on your system.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) is the core command-line tool for this project. Install it using pip:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
3.  **Orchestrate Environment Initialization**: You must initialize a project directory and log in to your watsonx Orchestrate instance.
    *   Create a project directory: `mkdir barista_buddy_poc && cd barista_buddy_poc`
    *   Initialize the environment: `orchestrate init`
    *   Log in to your watsonx Orchestrate instance (follow the CLI prompts): `orchestrate login`
4.  **Project Directory Structure**: To keep the project organized, create the following subdirectories inside `barista_buddy_poc`:
    ```bash
    mkdir agents
    mkdir tools
    mkdir knowledge_docs
    mkdir data
    ```
    This structure will house the agent YAML files, Python tool definitions, knowledge base documents, and mock data files, respectively.

## Step 1: Create Mock Data and Knowledge Base Documents

To simulate a real-world environment, we will create the documents for our `Barista Knowledge Agent`'s knowledge base and a JSON file to act as our mock inventory database.

1.  **Knowledge Documents**: Navigate to the `knowledge_docs` directory.
    *   Create a file named `espresso_machine_cleaning_guide.txt`.

        **File: `knowledge_docs/espresso_machine_cleaning_guide.txt`**
        ```text
        Espresso Machine Daily Cleaning Protocol

        Effective Date: 2024-01-01
        Version: 3.1

        Introduction:
        Daily cleaning is essential for maintaining machine performance, ensuring coffee quality, and extending the equipment's lifespan. Failure to follow these steps can result in bitter-tasting espresso and costly repairs.

        Procedure:
        1. Backflush with Water: At the end of the day, insert the blind filter basket into the portafilter. Run the brew cycle for 10 seconds, then stop. Repeat 5 times. This flushes out coffee grounds from the group head.
        2. Backflush with Cleaner: Add a small amount (1/2 teaspoon) of espresso machine cleaning powder to the blind basket. Run the brew cycle for 10 seconds and stop. Repeat 5 times. You will see foamy, brown water discharged.
        3. Rinse Cycle: Remove the portafilter, rinse the blind basket thoroughly. Re-insert and perform the water-only backflush (Step 1) again to rinse out any residual cleaner.

        Troubleshooting:
        - Low Pressure: Check for blockages in the group head. A thorough cleaning cycle often resolves this.
        - Leaking from Group Head: The group head gasket may be worn. This is a common wear-and-tear item that needs replacement every 6-12 months.
        ```
    *   Create a second file named `latte_art_basics.txt`.

        **File: `knowledge_docs/latte_art_basics.txt`**
        ```text
        Latte Art Basics for New Baristas

        Principle 1: Perfect Milk Texture
        The key to latte art is microfoam. You are not creating stiff, bubbly foam. You are texturing the milk to a smooth, velvety consistency like wet paint.
        - Aeration: Introduce air for only 1-3 seconds at the beginning. The milk should only increase in volume by about 20-30%.
        - Emulsification: Submerge the steam wand tip below the surface and create a whirlpool. This vortex breaks down large bubbles and integrates the air, creating silky microfoam.
        - Temperature: Stop steaming when the pitcher is too hot to comfortably touch (around 140-150°F / 60-65°C).

        Principle 2: The Pour
        1. The High Pour: Start pouring from a height of 4-6 inches. This allows the milk to dive underneath the crema, creating the canvas.
        2. The Low Pour: Bring the pitcher spout close to the surface of the espresso to draw the design.
        ```

2.  **Mock Inventory Database**: Navigate to the `data` directory and create `inventory.json`. This file will be read by our Python tools to simulate a live inventory system.

    **File: `data/inventory.json`**
    ```json
    {
      "inventory": [
        {"item_id": "COF-001", "item_name": "Espresso Beans", "category": "Coffee", "quantity": 12, "unit": "kg", "reorder_level": 10, "supplier_id": "SUP-A"},
        {"item_id": "MLK-001", "item_name": "Whole Milk", "category": "Dairy", "quantity": 6, "unit": "gallons", "reorder_level": 4, "supplier_id": "SUP-B"},
        {"item_id": "MLK-002", "item_name": "Oat Milk", "category": "Dairy Alternative", "quantity": 8, "unit": "cartons", "reorder_level": 5, "supplier_id": "SUP-B"},
        {"item_id": "SYR-001", "item_name": "Vanilla Syrup", "category": "Syrups", "quantity": 3, "unit": "bottles", "reorder_level": 2, "supplier_id": "SUP-A"},
        {"item_id": "CUP-001", "item_name": "12oz Hot Cups", "category": "Disposables", "quantity": 150, "unit": "units", "reorder_level": 100, "supplier_id": "SUP-C"}
      ],
      "suppliers": [
        {"supplier_id": "SUP-A", "name": "Global Coffee Importers", "contact_email": "orders@gci.com"},
        {"supplier_id": "SUP-B", "name": "Fresh Farm Dairy Co.", "contact_email": "sales@freshfarm.com"},
        {"supplier_id": "SUP-C", "name": "Eco-Friendly Packaging Inc.", "contact_email": "contact@efp.com"}
      ]
    }
    ```

## Step 2: Implement Python Tools

We will now create the Python functions that our agents will use to perform actions. These tools are the building blocks of our agents' capabilities.

1.  **Inventory & Supply Tools**: Navigate to the `tools` directory and create a file named `inventory_tools.py`. This file will contain all tools related to inventory management.

    **File: `tools/inventory_tools.py`**
    ```python
    import json
    from typing import List, Optional
    from ibm_watsonx_orchestrate.agent_builder.tools import tool

    INVENTORY_FILE = 'data/inventory.json'

    def _load_data():
        """Helper function to load data from the mock JSON database."""
        try:
            with open(INVENTORY_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"inventory": [], "suppliers": []}

    @tool
    def check_stock_level(item_name: str) -> str:
        """
        Checks the current stock level for a specific item in the inventory.

        Args:
            item_name (str): The name of the item to check (e.g., "Whole Milk", "Espresso Beans").

        Returns:
            str: A message indicating the current quantity and unit of the item, or a not-found message.
        """
        data = _load_data()
        for item in data.get('inventory', []):
            if item_name.lower() in item['item_name'].lower():
                return f"We currently have {item['quantity']} {item['unit']} of {item['item_name']} in stock."
        return f"Item '{item_name}' not found

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
