#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate-adk"
        ```
*   **IBM watsonx Orchestrate Environment:** You must have an active watsonx Orchestrate environment configured and logged into via the ADK.
    *   **Configuration Command:** Run `orchestrate login` and follow the interactive prompts to authenticate and set your default environment.
*   **Text Editor or IDE:** A code editor such as Visual Studio Code is highly recommended for creating and editing the required Python (`.py`) and YAML (`.yaml`) files.

## 3. Step-by-Step Instructions

### Step 3.1: Project Structure and Mock Data Setup

A well-organized project structure is crucial for managing the different components of our solution. We will create dedicated folders for agents, tools, mock data, and knowledge base documents.

1.  **Create the Project Directory Structure:**
    Open your terminal and execute the following commands to create the necessary folders.
    ```bash
    mkdir starbucks-copilot
    cd starbucks-copilot
    mkdir agents tools data docs
    ```
    Your project structure should now look like this:
    ```
    starbucks-copilot/
    ├── agents/
    ├── data/
    ├── docs/
    └── tools/
    ```

2.  **Create Mock Data Files:**
    These JSON files simulate the real-world operational systems (POS, Inventory, HR) that the Co-Pilot will interact with. This strategy allows for robust development and testing without requiring live system integrations.

    *   **Create `data/sales_data.json` (Mock POS Data):** This file contains a daily sales summary.
        ```json
        {
          "report_date": "2024-10-26",
          "total_sales": 5480.75,
          "transaction_count": 450,
          "average_transaction_value": 12.18,
          "peak_hours": "8:00 AM - 10:00 AM",
          "top_selling_items": [
            {"item": "Grande Caramel Macchiato", "units_sold": 75},
            {"item": "Venti Iced Coffee", "units_sold": 62},
            {"item": "Pumpkin Spice Latte", "units_sold": 55},
            {"item": "Chocolate Croissant", "units_sold": 48}
          ]
        }
        ```
    *   **Create `data/inventory.json` (Mock Inventory System):** This file maps product names to their current stock levels.
        ```json
        {
          "blonde_espresso_beans_kg": 8.5,
          "pike_place_roast_kg": 15.2,
          "oat_milk_liters": 25.0,
          "caramel_syrup_bottles": 5,
          "vanilla_syrup_bottles": 12,
          "grande_hot_cups_sleeve": 30
        }
        ```
    *   **Create `data/employees.json` (Mock Employee Roster):** This file lists employees and their availability for covering shifts.
        ```json
        [
          {
            "name": "John Smith",
            "role": "Barista",
            "is_available_for_call_in": true,
            "contact": "555-0101"
          },
          {
            "name": "Maria Garcia",
            "role": "Shift Supervisor",
            "is_available_for_call_in": true,
            "contact": "555-0102"
          },
          {
            "name": "David Lee",
            "role": "Barista",
            "is_available_for_call_in": false,
            "contact": "555-0103"
          },
          {
            "name": "Sarah Johnson",
            "role": "Barista",
            "is_available_for_call_in": false,
            "contact": "555-0104"
          }
        ]
        ```

3.  **Create a Placeholder Knowledge Base Document:**
    For the demo, we will use a placeholder PDF to represent a store operations manual. Create a simple text file with the content below, then save it as a PDF named `Starbucks_SOP_Manual.pdf` and place it inside the `docs/` folder.
    *Content for the PDF:* "Store opening procedure requires two baristas on-site 30 minutes before opening. Customer complaints should be escalated to the shift supervisor immediately. All food items must be dated upon delivery."

4.  **Create `requirements.txt`:**
    While our tools for this demo do not require external packages, creating a `requirements.txt` file is a best practice for any Python project. This file would list any dependencies needed for the tools to run.
    ```bash
    touch requirements.txt
    ```

### Step 3.2: Create the Specialist Tools (Python)

Tools are the functional heart of our agents, enabling them to perform actions by executing code. We will create three Python-based tools, each in its own file. A key design principle here is that **tools should return structured data (like JSON)**, separating the act of data retrieval from its presentation. The agent will be responsible for formatting this data into a user-friendly, conversational response.

*   **Tool 1: Sales Reporting Tool**
    **Business Value:** This tool automates the daily task of pulling and summarizing sales data. It saves the manager time from manually logging into a POS system and compiling a report, providing instant, structured insights into store performance that the agent can then articulate.
    **Technical Implementation:** The tool reads the mock sales JSON file and returns a dictionary containing the key performance indicators. It includes robust error handling to manage cases where the data file might be missing or corrupted.

    **Create `tools/sales_tools.py`:**
    ```python
    import json
    from typing import Dict, Any
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(permission=ToolPermission.ADMIN)
    def get_daily_sales_report() -> Dict[str, Any]:
        """
        Retrieves the daily sales report from the Point-of-Sale system as a structured object.
        This tool provides key metrics like total sales, transaction count, and top-selling items.

        Returns:
            Dict[str, Any]: A dictionary containing the structured daily sales report data.
        """
        try:
            with open('data/sales_data.json', 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {"error": "The sales data file could not be found."}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the sales data file. It may be corrupted."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}
    ```

*   **Tool 2: Inventory Checking Tool**
    **Business Value:** This tool provides immediate visibility into stock levels, preventing stockouts of key ingredients and ensuring a consistent customer experience. It allows managers to make proactive ordering decisions based on real-time data retrieved in a structured format.
    **Technical Implementation:** This tool takes an `item_name` as input, normalizes it for better matching, and queries the inventory data. It returns a structured dictionary with the item's name, quantity, and unit of measure, or an error if the item is not found.

    **Create `tools/inventory_tools.py`:**
    ```python
    import json
    from typing import Dict, Any
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(permission=ToolPermission.ADMIN)
    def check_stock_level(item_name: str) -> Dict[str, Any]:
        """
        Checks the current stock level for a given inventory item from the inventory system.

        Args:
            item_name (str): The name of the item to check, e.g., 'blonde espresso beans' or 'oat milk'.

        Returns:
            Dict[str, Any]: A dictionary with the item name, quantity, and unit, or an error message.
        """
        try:
            with open('data/inventory.json', 'r') as f:
                inventory = json.load(f)

            search_key = item_name.lower().replace(' ', '_')
            found_key = None
            for key in inventory:
                if search_key in key:
                    found_key = key
                    break
            
            if found_key:
                quantity = inventory[found_key]
                unit = "kg" if "kg" in found_key else \
                       "liters" if "liters" in found_key else \
                       "bottles" if "bottles" in found_key else \
                       "sleeves" if "sleeve" in found_key else "units"
                return {"item_name": item_name, "quantity": quantity, "unit": unit}
            else:
                return {"error": f"Item '{item_name}' not found in the inventory system."}
        except FileNotFoundError:
            return {"error": "The inventory data file could not be found."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}
    ```

*   **Tool 3: HR Availability Tool**
    **Business Value:** This tool streamlines the critical and time-sensitive process of finding coverage for a shift. It eliminates manual checks of schedules or phone lists, quickly providing a structured list of available staff that the agent can present to the manager, reducing store disruption.
    **Technical Implementation:** The tool reads the employee roster, filters for staff marked as `is_available_for_call_in`, and returns a list of dictionaries, where each dictionary represents an available employee.

    **Create `tools/hr_tools.py`:**
    ```python
    import json
    from typing import Dict, List, Any
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(permission=ToolPermission.ADMIN)
    def find_available_employees() -> Dict[str, List[Dict[str, Any]]]:
        """
        Identifies employees who are marked as available for call-in shifts from the HR system.
        This is used to quickly find coverage when an employee calls in sick.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of available employees.
        """
        try:
            with open('data/employees.json', 'r') as f:
                employees = json.load(f)
            
            available_staff = [
                {"name": emp["name"], "role": emp["role"]}
                for emp in employees if emp.get('is_available_for_call_in', False)
            ]

            return {"available_employees": available_staff}
        except FileNotFoundError:
            return {"error": "The employee roster file could not be found."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}
    ```

### Step 3.3: Create the Knowledge Base

The knowledge base allows the Co-Pilot to answer informational questions about store policies by searching through provided documents. This demonstrates the RAG capabilities of watsonx Orchestrate.

**Create `docs/store_operations_manual.yaml`:**

