# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-22 15:54:38
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Store Operations Co-Pilot for Starbucks

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an "AI-Powered Store Operations Co-Pilot" for Starbucks using IBM watsonx Orchestrate. The solution is designed to address the client's core challenge: empowering store managers by automating routine administrative tasks, thereby freeing them to focus on high-value activities like customer engagement and team development.

The demo implements a sophisticated multi-agent architecture, a key pattern in watsonx Orchestrate. A central **Supervisor Agent** (`store_manager_copilot`) acts as the manager's primary interface. It intelligently interprets natural language requests and delegates tasks to a team of specialized **Collaborator Agents** responsible for sales analytics, inventory management, and HR shift coordination. This modular design showcases Orchestrate's ability to create scalable, maintainable, and powerful AI assistants that integrate seamlessly into complex business workflows. The plan also includes a Retrieval-Augmented Generation (RAG) component via a knowledge base, allowing the manager to ask questions about company policies and procedures.

## 2. Prerequisites

Before beginning, ensure your development environment is correctly configured.

*   **Python:** Python 3.10 or higher installed.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed. If not, install it via pip:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. If you haven't done so, run:
    ```bash
    orchestrate login
    orchestrate env init
    ```
*   **Project Structure:** A dedicated directory for the project is required. All commands and file paths in this plan assume they are run from the root of this project directory.

## 3. Project Setup and File Structure

To ensure a clean and organized build, create the following directory and file structure. This structure separates agents, tools, mock data, and knowledge base assets.

```
starbucks_copilot_demo/
├── agents/
│   ├── store_manager_copilot.yaml
│   ├── sales_analytics_agent.yaml
│   ├── inventory_management_agent.yaml
│   └── hr_shift_coordinator_agent.yaml
├── tools/
│   ├── sales_tool.py
│   ├── inventory_tool.py
│   └── hr_tool.py
├── data/
│   ├── sales_data.json
│   ├── inventory.json
│   └── schedules.json
├── knowledge_base/
│   ├── starbucks_sop_kb.yaml
│   └── docs/
│       ├── HR_Policy_Shift_Swapping.pdf
│       └── Holiday_Drink_Recipes_2024.docx
└── requirements.txt
```
*(Note: The `.pdf` and `.docx` files in `docs/` can be empty placeholder files for this demo.)*

## 4. Step-by-Step Implementation

### Step 4.1: Create Mock Data Files

These JSON files simulate the data sources that the agents' tools will interact with.

**1. Sales Data (`data/sales_data.json`)**
This file mimics output from a Point-of-Sale (POS) system.

```json
{
  "report_date": "2024-10-26",
  "total_revenue": 4850.75,
  "transactions_count": 512,
  "top_selling_items": [
    {"item_name": "Pumpkin Spice Latte", "units_sold": 85},
    {"item_name": "Cold Brew", "units_sold": 62},
    {"item_name": "Blonde Espresso Roast", "units_sold": 55},
    {"item_name": "Chocolate Croissant", "units_sold": 48}
  ],
  "peak_hours": "8:00 AM - 10:00 AM"
}
```

**2. Inventory Data (`data/inventory.json`)**
This file represents the store's current stock levels.

```json
[
  {"item_name": "Blonde Espresso Beans", "sku": "SKU-BEB-001", "quantity_on_hand": 8, "reorder_level": 10},
  {"item_name": "Oat Milk", "sku": "SKU-OAM-004", "quantity_on_hand": 25, "reorder_level": 20},
  {"item_name": "Vanilla Syrup", "sku": "SKU-VNS-012", "quantity_on_hand": 15, "reorder_level": 12},
  {"item_name": "Paper Cups - Grande", "sku": "SKU-PCG-101", "quantity_on_hand": 150, "reorder_level": 200}
]
```

**3. Employee Schedules (`data/schedules.json`)**
This file simulates an HR scheduling system.

```json
[
  {"employee_name": "Alex Chen", "role": "Barista", "is_available_today": false, "next_available_shift": "2024-10-28 09:00 AM"},
  {"employee_name": "Maria Garcia", "role": "Barista", "is_available_today": true, "availability_notes": "Available after 1 PM"},
  {"employee_name": "David Smith", "role": "Shift Supervisor", "is_available_today": false, "next_available_shift": "2024-10-29 06:00 AM"},
  {"employee_name": "Chloe Kim", "role": "Barista", "is_available_today": true, "availability_notes": "Fully available all day"}
]
```

### Step 4.2: Develop Python Tools

These Python functions, decorated with `@tool`, are the actions our agents can perform.

**1. Sales Tool (`tools/sales_tool.py`)**

This tool retrieves the daily sales report from the mock data file. It provides a quick, data-driven summary of store performance, enabling managers to understand revenue, transaction volume, and popular products without manually running reports. This directly supports agile, in-the-moment decision-making.

```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_daily_sales_report", permission=ToolPermission.ADMIN)
def get_daily_sales_report() -> dict:
    """
    Retrieves the sales report for the previous day.

    The report includes total revenue, number of transactions, and a list of the top-selling items.
    This tool is used to get a quick summary of the store's financial performance.

    Returns:
        dict: A dictionary containing the sales report details.
    """
    try:
        with open('data/sales_data.json', 'r') as f:
            sales_data = json.load(f)
        return sales_data
    except FileNotFoundError:
        return {"error": "Sales data file not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding sales data JSON."}
```

**2. Inventory Tool (`tools/inventory_tool.py`)**

This tool checks the stock level of a specific item. For a store manager, this is critical for preventing stockouts of key ingredients like "blonde espresso beans," ensuring customer satisfaction and avoiding lost sales. The tool simulates a real-time lookup into an inventory management system.

```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="check_stock_level", permission=ToolPermission.ADMIN)
def check_stock_level(item_name: str) -> dict:
    """
    Checks the current stock level for a specific item in the inventory system.

    Args:
        item_name (str): The name of the product to check (e.g., 'blonde espresso beans').

    Returns:
        dict: A dictionary containing the item name and its quantity on hand, or a 'not found' message.
    """
    try:
        with open('data/inventory.json', 'r') as f:
            inventory = json.load(f)
        for item in inventory:
            if item['item_name'].lower() == item_name.lower():
                return {"item": item['item_name'], "quantity": item['quantity_on_hand']}
        return {"item": item_name, "quantity": "not found"}
    except FileNotFoundError:
        return {"error": "Inventory data file not found."}
```

**3. HR Tool (`tools/hr_tool.py`)**

This tool finds available employees to cover a shift, a common and urgent need for any store manager. By automating this lookup, the Co-Pilot drastically reduces the time and stress associated with finding last-minute coverage, improving operational stability and employee morale.

```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="find_available_employees", permission=ToolPermission.ADMIN)
def find_available_employees(shift_details: str) -> list:
    """
    Finds employees who are available to cover an open shift based on today's schedule.

    Args:
        shift_details (str): A description of the shift that needs coverage (e.g., '2 PM shift today'). This argument provides context but the tool currently checks for general availability today.

    Returns:
        list: A list of dictionaries, where each dictionary represents an available employee.
    """
    try:
        with open('data/schedules.json', 'r') as f:
            schedules = json.load(f)
        
        available_staff = [
            emp for emp in schedules if emp.get('is_available_today')
        ]
        return available_staff
    except FileNotFoundError:
        return [{"error": "Schedule data file not found."}]
```

### Step 4.3: Create `requirements.txt`

This file ensures any dependencies for your tools are managed. For this demo, no external libraries are needed, but it's a best practice to include the file.

```text
# No external packages required for this demo
```

### Step 4.4: Define Collaborator Agents

These YAML files define the specialized agents. Their `description` is crucial, as it's what the supervisor agent uses to decide where to route a task.

**1. Sales Agent (`agents/sales_analytics_agent.yaml`)**

```yaml
spec_version: v1
kind: native
name: sales_analytics_agent
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
description: >
  An agent specializing in sales data. Use this agent to get daily sales reports,
  understand revenue, transaction counts, and identify top-selling products.
instructions: >
  Your purpose is to provide sales data. When asked for a sales report, use the
  get_daily_sales_report tool and present the information clearly to the user.
tools:
  - get_daily_sales_report
```

**2. Inventory Agent (`agents/inventory_management_agent.yaml`)**

```yaml
spec_version: v1
kind: native
name: inventory_management_agent
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
description: >
  An agent that manages and reports on store inventory. Use this agent to check
  the stock levels of specific items like coffee beans, milk, or syrups.
instructions: >
  Your purpose is to check inventory. When a user asks about the quantity of an item,
  use the check_stock_level tool with the item's name as input.
tools:
  - check_stock_level
```

**3. HR Agent (`agents/hr_shift_coordinator_agent.yaml`)**

```yaml
spec_version: v1
kind: native
name: hr_shift_coordinator_agent
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
description: >
  An agent focused on employee scheduling and availability. Use this agent to find
  out which employees are available to cover an open shift.
instructions: >
  Your purpose is to find available staff. When the manager needs to cover a shift,
  use the find_available_employees tool and list the names and roles of those who can work.
tools:
  - find_available_employees
```

### Step 4.5: Define the Supervisor Agent

This is the main agent that orchestrates the others. Its `instructions` explicitly tell it how to delegate tasks based on user intent.

**`agents/store_manager_copilot.yaml`**

```yaml
spec_version: v1
kind: native
name: store_manager_copilot
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
description: >
  An AI assistant for Starbucks store managers. It helps with sales reports, inventory checks,
  and employee scheduling by collaborating with specialized agents. It can also answer questions
  about company policies using its knowledge base.
instructions: >
  You are an AI Co-Pilot for a Starbucks Store Manager. Your goal is to assist with daily operational tasks by intelligently routing requests to your specialist agents.
  - For any questions about sales figures, daily performance, or revenue reports, you MUST use the sales_analytics_agent.
  - For any questions about stock levels, product quantities, or inventory, you MUST use the inventory_management_agent.
  - For finding employees to cover shifts, checking staff availability, or other scheduling questions, you MUST use the hr_shift_coordinator_agent.
  - For questions about company policies, procedures, or recipes, search your knowledge base.
collaborators:
  - sales_analytics_agent
  - inventory_management_agent
  - hr_shift_coordinator_agent
tools: []
knowledge_base:
  - starbucks_sop_kb
```

### Step 4.6: Create the Knowledge Base

This component adds RAG capabilities to the Co-Pilot, allowing it to answer questions from unstructured documents.

**`knowledge_base/starbucks_sop_kb.yaml`**

```yaml
spec_version: v1
kind: knowledge_base
name: starbucks_sop_kb
description: >
  Contains standard operating procedures (SOPs), HR policies, and seasonal drink
  recipe guides for Starbucks. Use this to answer questions about official company guidelines.
documents:
  - "knowledge_base/docs/HR_Policy_Shift_Swapping.pdf"
  - "knowledge_base/docs/Holiday_Drink_Recipes_2024.docx"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 4.7: Deploy the Solution with ADK CLI

Run these commands from your project's root directory. The order is important: dependencies (tools, KBs) must be imported before the agents that use them.

```bash
# 1. Import all Python tools
echo "Importing tools..."
orchestrate tools import -f tools/sales_tool.py
orchestrate tools import -f tools/inventory_tool.py
orchestrate tools import -f tools/hr_tool.py

# 2. Import the Knowledge Base
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/starbucks_sop_kb.yaml

# 3. Import the collaborator agents
echo "Importing collaborator agents..."
orchestrate agents import -f agents/sales_analytics_agent.yaml
orchestrate agents import -f agents/inventory_management_agent.yaml
orchestrate agents import -f agents/hr_shift_coordinator_agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/store_manager_copilot.yaml

echo "Deployment complete. You can now start the chat."
```

## 5. Verification and Demo Scenarios

Start the interactive chat interface to test the complete solution.

```bash
orchestrate chat start
```

Once the chat is running, use the following prompts to walk through the demo scenarios:

*   **Scenario 1: Daily Sales Briefing**
    *   **User Prompt:** `"What were our sales yesterday?"`
    *   **Expected Behavior:** The `store_manager_copilot` will delegate to the `sales_analytics_agent`. The agent will call the `get_daily_sales_report` tool and present a summary of the revenue, transactions, and top-selling items from `sales_data.json`.

*   **Scenario 2: Real-time Inventory Check**
    *   **User Prompt:** `"How many bags of blonde espresso beans do we have left?"`
    *   **Expected Behavior:** The Co-Pilot will route the request to the `inventory_management_agent`. The agent will use the `check_stock_level` tool, find the "Blonde Espresso Beans" entry in `inventory.json`, and respond with the quantity (e.g., "We have 8 bags of Blonde Espresso Beans on hand.").

*   **Scenario 3: Urgent Shift Coverage**
    *   **User Prompt:** `"Jamie can't make her 2 PM shift today. Who is available to cover?"`
    *   **Expected Behavior:** The Co-Pilot will delegate to the `hr_shift_coordinator_agent`. The agent will call the `find_available_employees` tool, which will filter `schedules.json` and return a list of available staff (Maria Garcia and Chloe Kim).

*   **Scenario 4: Knowledge Base Query (RAG)**
    *   **User Prompt:** `"What is the official policy on shift swapping?"`
    *   **Expected Behavior:** The Co-Pilot will recognize this as a policy question and query the `starbucks_sop_kb` knowledge base. It will synthesize an answer based on the content of the (placeholder) `HR_Policy_Shift_Swapping.pdf` document.

## 6. Troubleshooting

*   **`Tool not found` Error:** This usually happens if a tool was not imported before the agent that uses it. Rerun the `orchestrate tools import -f ...` command for the missing tool, then re-import the agent.
*   **Supervisor Agent Fails to Delegate:** If the Co-Pilot answers directly instead of routing, check two things:
    1.  The `description` of the collaborator agents. It must be clear and contain keywords related to its function (e.g., "sales," "inventory," "schedule").
    2.  The `instructions` of the `store_manager_copilot`. Ensure they are explicit about which agent to use for which task.
*   **File Not Found Error in Tools:** Ensure the tool's `open()` command uses the correct relative path to the data file (e.g., `data/inventory.json`). Also, confirm you are running `orchestrate chat start` from the project's root directory.
*   **Knowledge Base Not Working:** Check the status of the knowledge base after import with `orchestrate knowledge-bases status --name starbucks_sop_kb`. Ensure the `Ready` property is `true`. If not, there may be an issue with document ingestion.

## 7. Best Practices

*   **Modular Design (Supervisor/Collaborator):** The architecture used in this demo is a powerful IBM best practice. It allows you to build complex systems from simple, single-purpose agents, making the solution easier to develop, test, and maintain.
*   **Descriptive Naming and Descriptions:** The success of agent collaboration hinges on high-quality, descriptive text in the `name` and `description` fields of agents and tools. The LLM uses this metadata to make its routing and tool-use decisions.
*   **Explicit Instructions:** For supervisor agents, providing clear, rule-based `instructions` on when to use each collaborator removes ambiguity and leads to more reliable and predictable behavior.
*   **Separate Data from Logic:** Using external JSON files for mock data is a good practice. It allows you to update or change the demo data without modifying the Python tool code, simulating how a real application would interact with a dynamic database or API.
*   **Combine Orchestration with RAG:** Augmenting agentic actions with a knowledge base provides a comprehensive solution. The Co-Pilot can perform tasks (via tools) and answer informational questions (via RAG), making it a more versatile and valuable assistant.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
