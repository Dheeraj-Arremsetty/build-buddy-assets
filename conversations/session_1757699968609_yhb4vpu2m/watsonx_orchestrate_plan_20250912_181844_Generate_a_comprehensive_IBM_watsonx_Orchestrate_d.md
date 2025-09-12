# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 18:18:44
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy Demo

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Barista Buddy," an AI-powered store operations assistant for a coffee shop client, using IBM watsonx Orchestrate. The plan directly implements the client's specified Proof of Concept (POC), which aims to streamline daily tasks, reduce administrative overhead, and improve store efficiency. The solution architecture is centered around a supervisor agent that intelligently delegates tasks to specialized collaborator agents for inventory management, operational procedure lookup (using Retrieval-Augmented Generation - RAG), and maintenance reporting. This multi-agent system demonstrates a robust, scalable, and powerful pattern for enterprise automation, showcasing how Orchestrate can create a unified conversational interface to complex backend systems and knowledge sources.

## Prerequisites

Before beginning, ensure your development environment is correctly set up. This is crucial for the successful creation and deployment of the agents and tools outlined in this plan.

1.  **Python Environment**: An installation of Python 3.9 or higher is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment Configuration**: Your ADK must be configured to connect to an IBM watsonx Orchestrate environment. Follow the official documentation for `orchestrate login` or setting up environment variables.
4.  **Project Directory**: Create a dedicated project folder to keep all files organized.

    ```bash
    # Create the main project directory
    mkdir barista_buddy_poc
    cd barista_buddy_poc

    # Create subdirectories for assets
    mkdir agents
    mkdir tools
    mkdir mock_data
    mkdir mock_data/docs
    ```

## Step 1: Create Mock Operational Documents and Knowledge Base

The `Operations_Knowledge_Agent` will use a knowledge base to answer questions about store procedures. This demonstrates the powerful RAG capabilities of watsonx Orchestrate, allowing the agent to provide accurate answers from your company's official documentation.

First, create the mock documents that will be ingested into the knowledge base.

1.  **Create `Espresso_Machine_Cleaning_Guide.txt`**:
    *   Path: `barista_buddy_poc/mock_data/docs/Espresso_Machine_Cleaning_Guide.txt`
    *   Content:
        ```text
        End-of-Day Espresso Machine Cleaning Protocol

        1. Backflush each group head with a blind filter basket and cleaning detergent. Run a 10-second cycle 5 times.
        2. Remove and clean the portafilters and baskets with hot water and a designated brush. Soak overnight in a detergent solution.
        3. Purge the steam wands to clear any milk residue. Wipe down with a sanitized cloth.
        4. Clean the drip tray and grate. Wash with soap and hot water, then sanitize.
        5. Wipe down all external surfaces of the machine with a clean, damp cloth.
        ```

2.  **Create `Customer_Complaint_Policy.txt`**:
    *   Path: `barista_buddy_poc/mock_data/docs/Customer_Complaint_Policy.txt`
    *   Content:
        ```text
        Customer Complaint Handling Policy

        Our policy is to Listen, Acknowledge, Solve, and Thank (LAST).
        - Listen: Give the customer your full attention.
        - Acknowledge: Acknowledge their frustration and apologize for their experience.
        - Solve: Offer a solution. This could be remaking their drink, offering a refund, or providing a voucher for their next visit. Empower yourself to make the customer happy.
        - Thank: Thank the customer for bringing the issue to our attention.
        ```

Now, create the YAML configuration for the knowledge base.

### Configuration File: `operations_kb.yaml`

This file defines the knowledge base, names it, describes its purpose, and points to the documents to be ingested. The `embeddings_model_name` specifies the model used to create vector embeddings for efficient searching.

*   Path: `barista_buddy_poc/knowledge_bases/operations_kb.yaml`

```yaml
spec_version: v1
kind: knowledge_base
name: operations_procedures_kb
description: >
  Contains all operational documents for the coffee shop, including equipment cleaning procedures, health and safety guidelines, customer service policies, and official drink recipes.
documents:
  - "mock_data/docs/Espresso_Machine_Cleaning_Guide.txt"
  - "mock_data/docs/Customer_Complaint_Policy.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Develop Python Tools

Tools are the actions your agents can perform. We will create two Python-based tools: one to check inventory and another to report equipment issues. These tools will simulate interactions with external systems like an inventory database or a ticketing system.

### Tool 1: Inventory Checker

**Business Value**: This tool provides staff with real-time access to inventory data through a simple conversational query. It eliminates the need for manual stock checks in the back room, saving time and ensuring baristas can quickly determine if they have enough product to fulfill an order, improving operational efficiency and customer service.

**Technical Implementation**: The `check_stock_level` function simulates a call to an inventory management API. It contains a hardcoded dictionary representing the current stock levels. In a production environment, this function would be modified to make an actual HTTP request to a real inventory system. It returns a structured JSON object with the item's stock information.

*   Create file: `barista_buddy_poc/tools/inventory_tools.py`

```python
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
```

### Tool 2: Maintenance Reporter

**Business Value**: This tool automates and standardizes the process of reporting equipment issues. Instead of manually filling out a form or making a phone call, staff can simply describe the problem in natural language. This accelerates the maintenance cycle, reduces equipment downtime, and ensures all issues are tracked with a unique ticket ID, improving accountability and operational continuity.

**Technical Implementation**: The `report_equipment_issue` function simulates a transactional API call to a maintenance or IT service management (ITSM) system like ServiceNow or Jira. It accepts the equipment name and a description of the issue, then returns a synthetic ticket number in a structured `TicketResponse` object, confirming the action was completed. The use of Pydantic models ensures the output is well-defined and predictable for the agent.

*   Create file: `barista_buddy_poc/tools/maintenance_tools.py`

```python
# tools/maintenance_tools.py
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

class TicketResponse(BaseModel):
    status: str = Field(description="The status of the ticket creation, e.g., 'success'.")
    ticket_id: str = Field(description="The unique identifier for the created maintenance ticket.")
    message: str = Field(description="A confirmation message for the user.")

@tool
def report_equipment_issue(equipment_name: str, issue_description: str) -> TicketResponse:
    """
    Creates a maintenance ticket for broken or malfunctioning equipment.

    Args:
        equipment_name (str): The name of the equipment that is broken (e.g., 'main grinder', 'espresso machine').
        issue_description (str): A detailed description of the problem.

    Returns:
        TicketResponse: An object containing the status and ID of the newly created ticket.
    """
    print(f"SIMULATING API CALL: Creating ticket for '{equipment_name}' with issue: '{issue_description}'")
    
    # Generate a random, realistic-looking ticket ID
    ticket_id = f"INC{random.randint(1000000, 9999999)}"
    
    confirmation_message = f"Maintenance ticket {ticket_id} has been successfully logged for the {equipment_name}."
    
    return TicketResponse(
        status="success", 
        ticket_id=ticket_id, 
        message=confirmation_message
    )
```

### Create `requirements.txt`

This file lists the Python dependencies for our tools.

*   Path: `barista_buddy_poc/requirements.txt`
```text
pydantic
```

## Step 3: Define Agent Configurations (YAML)

With the tools and knowledge base defined, we can now create the YAML configurations for our agents. We will start with the specialized collaborator agents and finish with the main supervisor agent.

### Collaborator Agent 1: `Inventory_Manager_Agent.yaml`

This agent is specialized in handling all tasks related to inventory. Its description is crafted to clearly state its capability, which the supervisor agent will use to route relevant queries.

*   Path: `barista_buddy_poc/agents/Inventory_Manager_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: Inventory_Manager_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  This agent is an expert in inventory management for the coffee shop. Use it to check current stock levels of any product, including beans, milk, syrups, and paper goods.
instructions: >
  Your sole purpose is to answer questions about inventory. When a user asks about stock, use the check_stock_level tool to find the information and report it back clearly.
tools:
  - check_stock_level
```

### Collaborator Agent 2: `Operations_Knowledge_Agent.yaml`

This agent's purpose is to act as a subject matter expert on store operations by leveraging the knowledge base we created. It does not have custom tools; its primary capability comes from the RAG pattern.

*   Path: `barista_buddy_poc/agents/Operations_Knowledge_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: Operations_Knowledge_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  This agent is an expert on all official store procedures, policies, and recipes. Use it for questions about how to perform tasks like cleaning equipment, handling customer complaints, or preparing drinks.
instructions: >
  You answer questions by searching the company's operational documents. Provide clear, step-by-step answers based on the information found in the knowledge base.
knowledge_base:
  - operations_procedures_kb
```

### Collaborator Agent 3: `Maintenance_Reporter_Agent.yaml`

This agent is responsible for the transactional task of creating maintenance tickets. Its purpose is narrowly focused on this action.

*   Path: `barista_buddy_poc/agents/Maintenance_Reporter_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: Maintenance_Reporter_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  This agent is used to report broken or malfunctioning store equipment. Use it to log a maintenance ticket for any piece of hardware that needs repair.
instructions: >
  When a user wants to report a broken item, use the report_equipment_issue tool. You must gather the equipment name and a description of the problem from the user's request. Confirm the action by returning the ticket number to the user.
tools:
  - report_equipment_issue
```

### Supervisor Agent: `Barista_Buddy_Supervisor.yaml`

This is the main agent that the user will interact with. It does not have its own tools or knowledge base. Its primary role is to understand the user's intent and delegate the task to the correct collaborator agent. The `description` and `instructions` are critical for ensuring correct routing.

*   Path: `barista_buddy_poc/agents/Barista_Buddy_Supervisor.yaml`

```yaml
spec_version: v1
kind: native
name: Barista_Buddy_Supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A helpful AI assistant for coffee shop staff named Barista Buddy. It can check inventory, look up operational procedures, and report broken equipment by collaborating with a team of specialized agents.
instructions: >
  You are the primary point of contact for the user. Your goal is to understand the user's request and delegate it to the correct specialist collaborator. Do not attempt to answer questions yourself; always use a collaborator.
  - For any questions about stock, inventory, or product levels, use the Inventory_Manager_Agent.
  - For questions about 'how to' do something, procedures, policies, or recipes, use the Operations_Knowledge_Agent.
  - If the user wants to report a broken, faulty, or malfunctioning piece of equipment, use the Maintenance_Reporter_Agent.
collaborators:
  - Inventory_Manager_Agent
  - Operations_Knowledge_Agent
  - Maintenance_Reporter_Agent
```

## Step 4: Import All Assets Using the ADK CLI

Now that all configuration files and tools are created, you will import them into your watsonx Orchestrate environment. The order of operations is important: dependencies (tools, knowledge bases) must be imported before the assets that rely on them (agents).

Execute these commands from the root of your `barista_buddy_poc` directory.

1.  **Import the Python Tools**:
    ```bash
    # Import the inventory tool
    orchestrate tools import -f tools/inventory_tools.py

    # Import the maintenance tool
    orchestrate tools import -f tools/maintenance_tools.py
    ```

2.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledgebases import -f knowledge_bases/operations_kb.yaml
    ```
    *Note: Ingestion may take a few moments. You can check the status with `orchestrate knowledge-bases status --name operations_procedures_kb`.*

3.  **Import the Collaborator Agents**:
    ```bash
    orchestrate agents import -f agents/Inventory_Manager_Agent.yaml
    orchestrate agents import -f agents/Operations_Knowledge_Agent.yaml
    orchestrate agents import -f agents/Maintenance_Reporter_Agent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/Barista_Buddy_Supervisor.yaml
    ```

## Step 5: Verification and Testing

After successfully importing all assets, you can test the complete solution using the ADK's interactive chat interface.

1.  **Start the Chat**:
    ```bash
    orchestrate chat start
    ```

2.  **Select the Supervisor Agent**: When prompted, choose `Barista_Buddy_Supervisor` as the agent to chat with.

3.  **Run Demo Scenarios**: Test the three core functionalities by typing the following prompts, one at a time.

    *   **Scenario 1: Inventory Check**
        *   **User Prompt**: `Hey Barista Buddy, how much oat milk do we have in stock?`
        *   **Expected Behavior**: The Supervisor will delegate to the `Inventory_Manager_Agent`. The agent will call the `check_stock_level` tool and respond with a message like: "We currently have 12 cartons of oat milk in stock."

    *   **Scenario 2: Procedure Lookup (RAG)**
        *   **User Prompt**: `What are the steps for the end-of-day cleaning for the espresso machine?`
        *   **Expected Behavior**: The Supervisor will delegate to the `Operations_Knowledge_Agent`. The agent will query the knowledge base and return a summarized, step-by-step guide based on the content from `Espresso_Machine_Cleaning_Guide.txt`.

    *   **Scenario 3: Equipment Reporting**
        *   **User Prompt**: `The main grinder is making a loud noise and not grinding beans properly. Can you please log a high-priority maintenance ticket for it?`
        *   **Expected Behavior**: The Supervisor will delegate to the `Maintenance_Reporter_Agent`. The agent will use the `report_equipment_issue` tool and confirm with a message like: "I've logged a ticket for the main grinder. The ticket number is INCxxxxxxx."

## Troubleshooting

-   **Incorrect Routing**: If the Supervisor agent doesn't delegate to the correct collaborator, review the `instructions` in `Barista_Buddy_Supervisor.yaml` and the `description` fields in each collaborator agent's YAML. The descriptions must be distinct and accurately reflect each agent's unique capability.
-   **Tool Not Found**: If an agent responds that it cannot find a tool, ensure the tool was imported successfully using `orchestrate tools list`. Also, verify the tool name in the agent's YAML `tools` list exactly matches the function name in the Python file.
-   **Knowledge Base Fails**: If the `Operations_Knowledge_Agent` cannot answer questions, check the knowledge base status with `orchestrate knowledge-bases status --name operations_procedures_kb`. Ensure the `Ready` status is `true` and that the file paths in `operations_kb.yaml` are correct relative to where you run the command.
-   **Import Errors**: Carefully check YAML file indentation and syntax. Ensure all file paths are correct. Run the import commands from the project's root directory (`barista_buddy_poc`).

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
