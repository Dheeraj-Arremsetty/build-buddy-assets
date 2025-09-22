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