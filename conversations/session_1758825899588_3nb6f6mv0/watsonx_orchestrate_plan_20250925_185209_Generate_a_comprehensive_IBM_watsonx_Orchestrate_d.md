# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-25 18:52:09
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building the "Barista Buddy" proof-of-concept (POC) using IBM watsonx Orchestrate. The solution is tailored to the client's specific need to accelerate barista onboarding and ensure consistent in-store operations. We will construct a multi-agent system featuring a supervisor agent that intelligently delegates tasks to specialized collaborators. One collaborator will leverage a knowledge base (RAG) to answer recipe and policy questions from mock corporate documents, while another will use tools to perform operational tasks like reporting equipment issues and checking inventory. This plan directly implements the architecture and scenarios outlined in the client's demo concept, showcasing the power of Orchestrate to create sophisticated, value-driven AI assistants.

## 2. Prerequisites

Before starting, ensure your development environment is correctly configured.

*   **Python:** Python 3.9 or higher must be installed.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have an active IBM watsonx Orchestrate environment configured. If you have not logged in, run `orchestrate login` and follow the prompts.
*   **Text Editor:** A text editor like Visual Studio Code is recommended for creating and editing Python, YAML, and JSON files.

## 3. Step-by-Step Instructions

### Step 1: Project Setup

First, create a structured directory for all the project assets. This organization simplifies management and deployment.

Open your terminal and run the following commands:

```bash
# Create the main project directory
mkdir barista_buddy_poc
cd barista_buddy_poc

# Create subdirectories for agents, tools, knowledge base, and mock data
mkdir agents
mkdir tools
mkdir knowledge_base
mkdir mock_data
```

Your project structure should now look like this:

```
barista_buddy_poc/
├── agents/
├── tools/
├── knowledge_base/
└── mock_data/
```

### Step 2: Create Mock Data and Knowledge Base Configuration

To power the `Recipe_and_Policy_Agent`, we need to create synthetic documents and a knowledge base configuration file that tells Orchestrate how to ingest them.

1.  **Create Mock `Drink_Recipes.pdf`:**
    For this demo, create a simple text file and save it as `Drink_Recipes.pdf` inside the `mock_data` directory.
    > **Note:** In a real scenario, this would be an actual PDF. For simplicity, we'll use text files that you can convert to PDF if desired.

    **File:** `mock_data/Drink_Recipes.pdf` (Content)
    ```text
    Starbucks Drink Recipes - Internal Use Only

    **Grande Caramel Macchiato**

    Ingredients:
    - 2 shots of Espresso
    - 3 pumps of Vanilla Syrup
    - Steamed 2% Milk
    - Caramel Drizzle

    Instructions:
    1. Pump 3 pumps of Vanilla Syrup into the bottom of a grande cup.
    2. Queue 2 shots of espresso.
    3. While espresso is pulling, steam 2% milk to 160°F.
    4. Pour the steamed milk into the cup, leaving room at the top.
    5. Add the 2 shots of espresso on top of the milk.
    6. Top with caramel drizzle in a crosshatch pattern.
    ```

2.  **Create Mock `Partner_Handbook_Policies.pdf`:**
    Create another file named `Partner_Handbook_Policies.pdf` in the `mock_data` directory.

    **File:** `mock_data/Partner_Handbook_Policies.pdf` (Content)
    ```text
    Starbucks Partner Handbook - Official Policies

    **Customer Drink Remake Policy**

    Our mission is to ensure every customer leaves happy. If a customer is not satisfied with their beverage for any reason, partners are empowered to remake the drink at no additional charge.

    Procedure:
    1. Acknowledge the customer's concern with empathy.
    2. Ask clarifying questions to understand what was wrong with the original drink.
    3. Offer to remake the drink immediately.
    4. Prepare the new drink according to the customer's preference, ensuring it meets quality standards.
    5. There is no need to process a transaction or charge for the remade beverage.
    ```

3.  **Create Knowledge Base YAML Configuration:**
    This YAML file defines the knowledge base, pointing to our mock documents. Orchestrate will use this to create a vector index using the built-in Milvus instance.

    **File:** `knowledge_base/starbucks_kb.yaml`
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: starbucks_knowledge_base
    description: >
       Contains official Starbucks documents including detailed drink recipes, food preparation guides, and partner handbook policies on customer service and store operations.
    documents:
       - "mock_data/Drink_Recipes.pdf"
       - "mock_data/Partner_Handbook_Policies.pdf"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rvr-v2
    ```

### Step 3: Create Tools for the `Store_Operations_Agent`

The `Store_Operations_Agent` will handle real-time tasks. We will create two tools: one using a Python script and another using an OpenAPI specification.

1.  **Python Tool: `report_equipment_issue`**

    This tool simulates creating a maintenance ticket for broken equipment. It demonstrates how Orchestrate can trigger actions in external systems (like a service desk or maintenance platform) directly from a conversation. The tool generates a synthetic ticket number to confirm the action was completed, providing immediate feedback to the barista and improving operational uptime.

    Create the following Python file:

    **File:** `tools/maintenance_reporter.py`
    ```python
    import random
    import datetime
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="report_equipment_issue", permission=ToolPermission.ADMIN)
    def report_equipment_issue(equipment_name: str, issue_description: str) -> str:
        """
        Creates a maintenance ticket for a piece of store equipment that is malfunctioning or broken.

        Args:
            equipment_name (str): The name of the equipment that is broken (e.g., 'espresso machine', 'ice maker').
            issue_description (str): A brief, clear description of the problem (e.g., 'leaking water', 'not cooling').

        Returns:
            str: A confirmation message with a synthetic ticket number.
        """
        # Generate a realistic, synthetic ticket ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        random_num = random.randint(1000, 9999)
        ticket_id = f"TICKET-{timestamp}-{random_num}"

        print(f"Generating maintenance ticket for '{equipment_name}' with issue: '{issue_description}'")
        
        # In a real application, this is where you would make an API call to a system like ServiceNow or Jira.
        # For this demo, we return a confirmation message.
        confirmation_message = f"Successfully created maintenance ticket {ticket_id} for the {equipment_name}. A technician will be dispatched shortly."
        
        return confirmation_message
    ```

2.  **OpenAPI Tool: `check_inventory_status`**

    This tool allows a barista to check the stock level of an item using natural language. It is defined by an OpenAPI specification, which is a standard way to describe REST APIs. This pattern is ideal for integrating with existing microservices or enterprise systems that expose API endpoints. By enabling quick inventory checks, this tool helps prevent stockouts and ensures partners can fulfill customer orders efficiently.

    Create the following JSON file:

    **File:** `tools/Mock_Inventory_API.json`
    ```json
    {
      "openapi": "3.0.0",
      "info": {
        "title": "Mock Store Inventory API",
        "version": "1.0.0",
        "description": "A simple API to check the stock status of store inventory items."
      },
      "servers": [
        {
          "url": "https://mock.inventory.api"
        }
      ],
      "paths": {
        "/inventory/{item_name}": {
          "get": {
            "summary": "Check Inventory Status",
            "operationId": "check_inventory_status",
            "description": "Retrieves the current stock level and status for a specific inventory item.",
            "parameters": [
              {
                "name": "item_name",
                "in": "path",
                "required": true,
                "description": "The name of the inventory item to check (e.g., 'Vanilla Syrup', 'Espresso Beans').",
                "schema": {
                  "type": "string"
                }
              }
            ],
            "responses": {
              "200": {
                "description": "Successful response with inventory status.",
                "content": {
                  "application/json": {
                    "schema": {
                      "type": "object",
                      "properties": {
                        "item": {
                          "type": "string"
                        },
                        "status": {
                          "type": "string",
                          "enum": ["In Stock", "Low Stock", "Out of Stock"]
                        },
                        "quantity": {
                          "type": "integer"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    ```
    > **Note:** The `url` in the `servers` block is a placeholder. Orchestrate uses the OpenAPI definition to understand the tool's inputs and outputs, but for this demo, the tool's execution will be mocked and will not make a live API call.

### Step 4: Create Agent Definitions (YAML)

Now we will define the three agents that make up our solution architecture.

1.  **`Recipe_and_Policy_Agent` (Collaborator)**

    This agent is a specialist in information retrieval. Its sole purpose is to answer questions by searching the `starbucks_knowledge_base`. By isolating this function, we create a modular and maintainable component that can be easily updated by simply adding new documents to its knowledge base, without changing any other part of the system.

    **File:** `agents/recipe_policy_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: Recipe_and_Policy_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      This agent is an expert on all official Starbucks documents. Use it to answer questions about drink recipes, food preparation standards, and official company policies found in the partner handbook. It does not perform operational tasks.
    instructions: >
      Your only purpose is to answer questions based on the provided knowledge base.
      Search the knowledge base for relevant information to the user's query about recipes or policies.
      Provide clear, concise answers and cite your sources. Do not answer questions outside of this scope.
    tools: []
    collaborators: []
    knowledge_base:
      - starbucks_knowledge_base
    ```

2.  **`Store_Operations_Agent` (Collaborator)**

    This agent is the "doer." It is equipped with tools to execute specific, action-oriented tasks. Its description clearly outlines its capabilities—reporting issues and checking inventory—which allows the supervisor agent to route relevant requests to it. This tool-using agent pattern is fundamental for automating business processes and integrating Orchestrate with other systems.

    **File:** `agents/store_operations_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: Store_Operations_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      This agent handles practical, in-store operational tasks. Use it to report broken equipment to create a maintenance ticket or to check the current inventory status of an item.
    instructions: >
      You are an operations assistant.
      - When a user wants to report a broken piece of equipment, use the `report_equipment_issue` tool. You must collect the equipment name and a description of the issue from the user before using the tool.
      - When a user asks about the stock level of an item, use the `check_inventory_status` tool.
    tools:
      - report_equipment_issue
      - check_inventory_status
    collaborators: []
    ```

3.  **`Barista_Buddy_Agent` (Supervisor)**

    This is the main agent and the single point of contact for the user. It acts as an intelligent router or "supervisor." Its instructions are critical; they define the reasoning logic for delegating tasks. Based on the user's intent, it decides whether to consult the `Recipe_and_Policy_Agent` for information or the `Store_Operations_Agent` for actions. This supervisor-collaborator pattern is a powerful way to build scalable and complex AI systems.

    **File:** `agents/barista_buddy_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: Barista_Buddy_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A helpful AI assistant for Starbucks store partners. It can answer questions about drink recipes and company policies by consulting the Recipe_and_Policy_Agent. It can also help with store operations like reporting broken equipment or checking inventory by using the Store_Operations_Agent.
    instructions: >
      Persona: You are the Barista Buddy, a friendly and helpful AI assistant for Starbucks partners.

      Reasoning:
      - For any questions about how to make drinks, food preparation, or official company policies, you MUST use the `Recipe_and_Policy_Agent`.
      - For any tasks related to store equipment, maintenance, or checking inventory stock levels, you MUST use the `Store_Operations_Agent`.
      - If the user's request is unclear, ask clarifying questions to determine if it is a knowledge question or an operational task.
    collaborators:
      - Recipe_and_Policy_Agent
      - Store_Operations_Agent
    ```

### Step 5: Create `requirements.txt`

This file lists any Python packages required by our tools. While our tool is simple, it's a best practice to include this file.

**File:** `requirements.txt`
```text
# No external packages are needed for maintenance_reporter.py
# If we were using 'requests' or other libraries, they would be listed here.
# For example:
# requests
```

### Step 6: Deploy the Solution using ADK CLI

With all the assets created, we will now use the `orchestrate` CLI to import everything into your environment in the correct order: tools first, then the knowledge base, then the collaborator agents, and finally the supervisor agent.

Open your terminal in the root of the `barista_buddy_poc` directory and run these commands one by one:

```bash
# 1. Import the Python and OpenAPI tools for the operations agent
echo "Importing tools..."
orchestrate tools import -k python -f tools/maintenance_reporter.py
orchestrate tools import -k openapi -f tools/Mock_Inventory_API.json

# 2. Import the knowledge base. This may take a few minutes as documents are ingested.
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/starbucks_kb.yaml

# 3. Import the collaborator agents (Recipe and Operations)
echo "Importing collaborator agents..."
orchestrate agents import -f agents/recipe_policy_agent.yaml
orchestrate agents import -f agents/store_operations_agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/barista_buddy_agent.yaml

echo "Deployment complete!"
```

## 4. Verification

After successful deployment, you can test the entire solution by starting a chat session with the main `Barista_Buddy_Agent`.

1.  **Start the Chat:**
    Run the following command in your terminal:
    ```bash
    orchestrate chat start --agent Barista_Buddy_Agent
    ```

2.  **Test Scenario 1: New Partner Onboarding (RAG)**
    *   **User Input:** `How do I make a grande Caramel Macchiato?`
    *   **Expected Behavior:** The `Barista_Buddy_Agent` should delegate this to the `Recipe_and_Policy_Agent`. This agent will query the knowledge base using the `Drink_Recipes.pdf` and return the step-by-step instructions.

3.  **Test Scenario 2: Handling a Customer Issue (RAG)**
    *   **User Input:** `A customer didn't like their drink, what's our policy for remaking it?`
    *   **Expected Behavior:** The supervisor will again route this to the `Recipe_and_Policy_Agent`, which will retrieve the official policy from the `Partner_Handbook_Policies.pdf`.

4.  **Test Scenario 3: Resolving an Operational Problem (Tool Use)**
    *   **User Input:** `The main espresso machine is leaking. Please report it.`
    *   **Expected Behavior:** The `Barista_Buddy_Agent` will identify this as an operational task and delegate it to the `Store_Operations_Agent`. This agent will then execute the `report_equipment_issue` tool, which will return a confirmation message with a unique, synthetic ticket number (e.g., `Successfully created maintenance ticket TICKET-20231027-5821...`).

## 5. Troubleshooting

*   **Issue: Agent/Tool Not Found during import.**
    *   **Solution:** Ensure you are running the `orchestrate` commands from the root directory (`barista_buddy_poc`). Check for typos in file paths and in the `name` fields within your YAML files (e.g., collaborator names must match the agent names exactly).
*   **Issue: Supervisor agent doesn't delegate correctly.**
    *   **Solution:** This is almost always due to the `description` and `instructions` of the agents. Review the supervisor's instructions to ensure they are clear and unambiguous. Also, check the collaborator agents' descriptions to ensure they accurately reflect their capabilities. A well-written description is crucial for the supervisor's reasoning.
*   **Issue: Knowledge base isn't returning answers.**
    *   **Solution:** Run `orchestrate knowledge-bases status --name starbucks_knowledge_base` to check if the ingestion is complete and the status is `Ready`. If the content is simple, ensure your query is specific enough to match the text in the mock documents.
*   **Issue: Python tool fails to import.**
    *   **Solution:** Check for syntax errors in your Python code (`tools/maintenance_reporter.py`). Ensure all necessary libraries are imported and that the `@tool` decorator is used correctly.

## 6. Best Practices

*   **Modular Design:** The supervisor-collaborator architecture is a powerful pattern. Keep agents specialized. One agent for knowledge (RAG), one for actions (tools), and one to orchestrate. This makes the system easier to manage, debug, and scale.
*   **Descriptive Clarity is Key:** The quality of the `description` and `instructions` fields directly impacts the performance of supervisor agents. Be explicit about what each agent and tool can (and cannot) do. Use the `Reasoning` section in instructions to provide direct guidance for delegation.
*   **Atomic Tools:** Design tools to perform one specific task well. The `report_equipment_issue` tool doesn't also check the warranty; it just creates a ticket. This makes tools reusable and easier to manage.
*   **Iterative Testing:** Use `orchestrate chat start` frequently during development to test each component as you build it. Test the tools and collaborator agents individually before testing the full supervisor flow.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
