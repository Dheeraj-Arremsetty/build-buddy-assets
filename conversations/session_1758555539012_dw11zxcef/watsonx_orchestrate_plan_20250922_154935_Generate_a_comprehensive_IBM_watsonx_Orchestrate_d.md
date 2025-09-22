# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-22 15:49:35
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Operations Co-Pilot for Starbucks Store Managers

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building the "AI-Powered Operations Co-Pilot," a multi-agent solution for Starbucks using IBM watsonx Orchestrate. The primary business objective is to empower store managers by automating high-frequency administrative tasks related to sales, inventory, and HR. This solution directly addresses the client's goal of achieving a **15-25% reduction in time spent on administrative overhead**, thereby freeing up managers to focus on enhancing customer experience, leading their teams, and driving store profitability.

The architecture leverages the powerful **Supervisor-Collaborator pattern** within watsonx Orchestrate. A central `StoreManagerCoPilot` agent acts as the primary conversational interface, intelligently understanding a manager's natural language requests and delegating them to a team of specialized collaborator agents: `SalesAgent`, `InventoryAgent`, and `HRAgent`. This modular design ensures that each component is focused, maintainable, and highly effective at its specific task. The solution also incorporates a knowledge base to answer policy-related questions, demonstrating a sophisticated blend of transactional task automation (via tools) and informational retrieval (via Retrieval-Augmented Generation).

## 2. Prerequisites

Before beginning, ensure your development environment is set up with the following components. This setup is essential for creating, importing, and testing the agents and tools according to IBM watsonx Orchestrate best practices.

*   **Python (3.9 or higher):** The watsonx Orchestrate Agent Development Kit (ADK) is a Python library and requires a compatible Python version.
    *   **Verification Command:** `python3 --version`
*   **pip (Python Package Installer):** The standard package manager for Python, used to install the ADK.
    *   **Verification Command:** `pip3 --version`
*   **IBM watsonx Orchestrate Agent Development Kit (ADK):** The core command-line interface (CLI) and library for building and managing agents and tools.
    *   **Installation Command:**
        ```bash
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
```yaml
spec_version: v1
kind: knowledge_base 
name: store_operations_manual
description: >
   Contains information from the Starbucks Store Operations Manual, including standard procedures for opening/closing, health codes, and customer service policies.
documents:
   - "docs/Starbucks_SOP_Manual.pdf"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 3.4: Create the Agent Configurations (YAML)

We will now define our agents using YAML configuration files. The descriptions and instructions are crafted to be highly detailed, guiding the LLM's reasoning and ensuring accurate task delegation and execution.

*   **Agent 1: SalesAgent**
    **Purpose:** This agent serves as a specialized data access layer for sales information. Its role is to execute the sales tool and pass the raw, structured data back to the supervisor. This single-responsibility design makes it highly reliable and predictable. The detailed description ensures the supervisor agent knows exactly when to delegate sales-related tasks to it, such as queries about revenue, transactions, or product performance.
    
    **Create `agents/SalesAgent.yaml`:**
    ```yaml
    spec_version: v1
    kind: native
    name: SalesAgent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent responsible for retrieving and providing daily sales data from the Point-of-Sale (POS) system. Its primary capability is to access detailed sales reports, including total revenue, transaction counts, peak operational hours, and lists of top-selling products. 
      
      Use this agent exclusively for any requests directly related to store sales performance for the current day. It is the designated expert for all quantitative sales metrics. It does not analyze trends or make forecasts; it only retrieves the raw data for the day's report.
    instructions: >
      Your sole function is to act as a data retriever for sales information. When you are activated by a supervisor agent, you must perform the following steps:
      1. Immediately execute the 'get_daily_sales_report' tool without any modification to the request.
      2. Take the raw JSON output from the tool.
      3. Return this complete, unaltered JSON object directly to the calling agent. Do not attempt to format, summarize, or interpret the data. Your task is data fetching, not presentation.
    tools:
      - get_daily_sales_report
    ```

*   **Agent 2: InventoryAgent**
    **Purpose:** This agent provides a focused interface for querying the inventory management system. Its clear description, centered on "stock levels" and "item quantities," signals its purpose to the supervisor. By handling only inventory checks, it ensures that requests like "how much espresso do we have?" are routed correctly and efficiently.
    
    **Create `agents/InventoryAgent.yaml`:**
    ```yaml
    spec_version: v1
    kind: native
    name: InventoryAgent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent that provides real-time stock level information for specific items by querying the inventory management system. This agent is the go-to resource for checking the quantity of any inventory item, such as coffee beans, milk, syrups, cups, or food items.
      
      Delegate to this agent whenever a user's request involves asking about the availability or current amount of a physical product. It can only check the stock of one item at a time and requires the item's name to perform its function.
    instructions: >
      You are an inventory data access agent. Your process is as follows:
      1. Receive a request that includes the name of an inventory item.
      2. Immediately execute the 'check_stock_level' tool, passing the item name as the argument.
      3. Return the complete, unaltered JSON object from the tool to the supervisor. Do not add any conversational text.
    tools:
      - check_stock_level
    ```

*   **Agent 3: HRAgent**
    **Purpose:** This agent is dedicated to HR and staffing tasks, specifically finding available employees for shift coverage. This is a critical operational need, and having a dedicated agent ensures a fast and accurate response. The description clearly outlines this capability, making it the obvious choice for the supervisor when a manager asks about covering a shift.
    
    **Create `agents/HRAgent.yaml`:**
    ```yaml
    spec_version: v1
    kind: native
    name: HRAgent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent that assists with urgent staffing and scheduling needs. Its primary function is to identify and list employees who are marked as available for call-in shifts from the HR system. 
      
      This agent should be used to quickly find coverage when an employee calls in sick or there is an unexpected need for additional staff. It provides a list of available personnel, including their names and roles, to facilitate rapid decision-making for the store manager.
    instructions: >
      You are an HR availability agent. Your task is simple and direct:
      1. Upon activation, execute the 'find_available_employees' tool.
      2. Return the resulting JSON object, which contains a list of available employees, directly to the supervisor agent. Do not format the list or add any introductory text.
    tools:
      - find_available_employees
    ```

*   **Agent 4: StoreManagerCoPilot (Supervisor)**
    **Purpose:** This is the orchestrator and the manager's primary point of contact. It holds no tools itself. Instead, its detailed instructions and the descriptions of its collaborators guide it to delegate tasks correctly. It is also equipped with the knowledge base to handle informational queries, making it a versatile assistant that can switch between transactional and informational tasks.
    
    **Create `agents/StoreManagerCoPilot.yaml`:**
    ```yaml
    spec_version: v1
    kind: native
    name: StoreManagerCoPilot
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A supervisor agent and AI co-pilot for Starbucks store managers. It acts as the central point of contact, understanding the manager's needs and delegating tasks to a team of specialist agents. It can answer questions about daily sales, current inventory levels, and employee availability by collaborating with these specialists. 
      
      In addition to its delegation capabilities, this agent can directly answer questions about store policies, standard operating procedures, and health codes by consulting its integrated knowledge base, which is based on the Store Operations Manual.
    instructions: >
      You are an AI Co-Pilot for a Starbucks Store Manager. Your primary role is to understand the manager's request, delegate it to the correct specialist agent, process the structured data you receive back, and present a final, helpful, and conversational response.

      Your reasoning process must be:
      1.  **Analyze the Request:** Determine the user's intent. Is it about sales, inventory, staffing, or store policy?
      2.  **Delegate the Task:**
          - If the request is about sales figures, daily reports, or top-selling items, use the 'SalesAgent'.
          - If the request is about stock levels, inventory counts, or specific product quantities (e.g., 'beans', 'milk'), use the 'InventoryAgent'.
          - If the request is about staffing, shift coverage, or finding available employees, use the 'HRAgent'.
          - If the request is about store policies, procedures, or the operations manual, use your knowledge base to find the answer.
      3.  **Process the Response:** You will receive a structured JSON object from your collaborator agents.
      4.  **Format the Final Answer:** Convert the JSON data into a clear, concise, and professional natural language response for the manager. For example, if you receive `{"total_sales": 5480.75}`, you should say "Today's total sales are $5,480.75."
    collaborators:
      - SalesAgent
      - InventoryAgent
      - HRAgent
    knowledge_base:
      - store_operations_manual
    ```

### Step 3.5: Import All Assets into watsonx Orchestrate

With all configuration files and tools created, we will now import them into the watsonx Orchestrate environment using the ADK CLI. The order is critical: tools must be imported first, followed by the knowledge base, then the collaborator agents, and finally the supervisor agent that depends on them.

Execute these commands from the root of your `starbucks-copilot` directory.

1.  **Import the Tools:**
    ```bash
    orchestrate tools import -f tools/sales_tools.py
    orchestrate tools import -f tools/inventory_tools.py
    orchestrate tools import -f tools/hr_tools.py
    ```

2.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f docs/store_operations_manual.yaml
    ```
    *(Note: The first time you import a knowledge base with documents, it may take a few minutes to process and index the files. You can check the status with `orchestrate knowledge-bases status --name store_operations_manual`.)*

3.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/SalesAgent.yaml
    orchestrate agents import -f agents/InventoryAgent.yaml
    orchestrate agents import -f agents/HRAgent.yaml
    ```

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/StoreManagerCoPilot.yaml
    ```

## 4. Verification and Demo Scenarios

After successfully importing all assets, you can verify the solution by interacting with the `StoreManagerCoPilot` agent.

1.  **Start the Chat Interface:**
    ```bash
    orchestrate chat start --agent StoreManagerCoPilot
    ```

2.  **Execute Demo Scenarios:**
    Engage with the agent in the command line using the following prompts from the client demo concept.

    *   **Scenario 1 (Sales):**
        *   **Manager asks:** `Pull up the sales report for today.`
        *   **Expected Response:** The `StoreManagerCoPilot` delegates to `SalesAgent`, gets back JSON, and formats it into a conversational summary:
            > "Today's total sales are $5,480.75 with 450 transactions. Our peak hours were 8:00 AM - 10:00 AM, and the top-selling item was the Grande Caramel Macchiato."

    *   **Scenario 2 (Inventory):**
        *   **Manager asks:** `How are we doing on blonde espresso beans?`
        *   **Expected Response:** The `StoreManagerCoPilot` delegates to `InventoryAgent`, gets back JSON, and formats the response:
            > "We have 8.5 kg of blonde espresso beans remaining in stock."

    *   **Scenario 3 (HR):**
        *   **Manager asks:** `Sarah called in sick for the closing shift. Who can I call to cover?`
        *   **Expected Response:** The `StoreManagerCoPilot` delegates to `HRAgent`, gets back a list of employees in JSON, and formats it:
            > "The following employees are available for call-in: John Smith (Barista) and Maria Garcia (Shift Supervisor)."

    *   **Scenario 4 (Knowledge Base):**
        *   **Manager asks:** `What is the policy for handling customer complaints?`
        *   **Expected Response:** The `StoreManagerCoPilot` uses its knowledge base to answer based on the PDF content:
            > "According to the operations manual, customer complaints should be escalated to the shift supervisor immediately."

## 5. Troubleshooting

*   **Issue: `Agent 'SalesAgent' not found` during `StoreManagerCoPilot` import.**
    *   **Cause:** The collaborator agents were not imported before the supervisor agent. The supervisor's definition requires its collaborators to already exist in the environment.
    *   **Solution:** Ensure you run the `orchestrate agents import` commands for `SalesAgent`, `InventoryAgent`, and `HRAgent` *before* running it for `StoreManagerCoPilot`.

*   **Issue: Agent gives a generic response instead of routing to a collaborator.**
    *   **Cause:** The supervisor agent's `description` and `instructions`, or the collaborator agent `descriptions`, may not be clear enough for the LLM to understand how to delegate the task.
    *   **Solution:** Refine the `instructions` in `StoreManagerCoPilot.yaml` to be more explicit (e.g., "If the user mentions 'sales' or 'report', use SalesAgent."). Also, ensure the `description` of each collaborator agent clearly states its unique capability.

*   **Issue: Tool returns `FileNotFoundError`.**
    *   **Cause:** The `orchestrate chat` command is being run from a directory other than the project root (`starbucks-copilot/`). The tool's code uses relative paths (e.g., `data/sales_data.json`).
    *   **Solution:** Always run `orchestrate chat start` from the project's root directory where the `data/` folder is located.

*   **Issue: Agent response is just the raw JSON output.**
    *   **Cause:** The `StoreManagerCoPilot` agent's instructions are not specific enough about its responsibility to format the data it receives from collaborators.
    *   **Solution:** Enhance the `instructions` in `agents/StoreManagerCoPilot.yaml` to explicitly state: "You will receive a structured JSON object from your collaborators. Your final step is to convert this JSON data into a clear, conversational response for the manager."

## 6. Best Practices

*   **Separation of Concerns:** The architecture of tools returning raw JSON and the supervisor agent handling presentation is a key best practice. It makes tools reusable and keeps the logic for presentation (which may change) within the agent's instructions, making the system more modular and maintainable.

*   **Craft High-Quality Descriptions:** The supervisor agent relies heavily on the `description` field of its collaborators to make routing decisions. Write clear, concise, and distinct descriptions for each agent that highlight its unique skills and the types of questions it can answer.

*   **Be Explicit in Supervisor Instructions:** Don't leave routing to chance. In the supervisor's `instructions`, provide explicit rules for delegation. Use phrases like "For tasks related to X, use Agent Y" to guide the LLM's reasoning process effectively.

*   **Embrace Granularity (Single Responsibility Principle):** The architecture of separate, specialized agents is a key strength. Resist the temptation to combine unrelated tools into a single agent. Granular agents are easier to build, test, maintain, and for the supervisor to reason about.

*   **Plan for Scalability:** This architecture is highly scalable. To add new capabilities, such as handling maintenance requests, simply create a new `MaintenanceAgent` with its own tools, add it to the `StoreManagerCoPilot`'s `collaborators` list, and update the supervisor's instructions. This avoids modifying existing, working components.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
