# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 19:45:47
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: The Perfect Blend AI Assistant

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying "The Perfect Blend," an AI assistant for barista excellence, using IBM watsonx Orchestrate. This solution is tailored to address the client's core business challenge of accelerating new hire onboarding and ensuring operational consistency. By creating a multi-agent system, we will provide an always-on, expert assistant that empowers new baristas with instant access to drink recipes and store procedures.

The architecture leverages a **Supervisor Agent pattern**, where the main `Barista_Concierge_Agent` intelligently routes user queries to specialized collaborator agents. The `Recipe_Expert_Agent` utilizes a **Knowledge Base (RAG)** to provide precise drink recipes from official company documents, while the `Store_Ops_Agent` uses a **Custom Python Tool** to retrieve standard operating procedures (SOPs). This plan will result in a functional Proof of Concept (POC) that demonstrates a projected 30-50% reduction in training time, ensures consistent product quality, and minimizes waste, directly contributing to improved customer satisfaction and employee confidence.

## Prerequisites
Before beginning, ensure your development environment is properly configured.

1.  **Python Installation**: Python 3.10 or higher must be installed on your system.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) is the core tool for this project. Install or upgrade it using pip:
    ```bash
    pip install --upgrade "ibm-watsonx-orchestrate[all]"
    ```
3.  **Orchestrate Environment**: You must have an active IBM watsonx Orchestrate environment configured. If you haven't already, initialize one using the ADK CLI.
4.  **Project Directory Structure**: To keep all assets organized, create the following directory structure in your workspace:
    ```
    perfect-blend-demo/
    ├── agents/
    │   ├── Barista_Concierge_Agent.yaml
    │   ├── Recipe_Expert_Agent.yaml
    │   └── Store_Ops_Agent.yaml
    ├── knowledge_base/
    │   ├── company_recipe_book_kb.yaml
    │   └── documents/
    │       ├── hot_drinks.pdf
    │       ├── cold_drinks.pdf
    │       └── seasonal_specials.pdf
    ├── tools/
    │   ├── store_procedures_tool.py
    │   └── procedures.json
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Knowledge Base Documents

The foundation of our specialized agents relies on high-quality, domain-specific data. We will create mock data for both the knowledge base and the custom tool.

### 1.1. Create the Tool's Data Source (`procedures.json`)
This JSON file acts as a mock database for our `Store_Ops_Agent`. It maps procedural keywords to detailed, step-by-step instructions.

**File:** `perfect-blend-demo/tools/procedures.json`
```json
{
  "clean espresso machine": "1. Perform a backflush with a blind filter. 2. Use espresso machine cleaning tablets as directed. 3. Purge the steam wands. 4. Wipe down all exterior surfaces with a sanitized cloth. 5. Check and empty the drip tray.",
  "closing checklist": "1. Clean the espresso machine. 2. Empty and clean all coffee grinders. 3. Wash and sanitize all pitchers, utensils, and containers. 4. Restock all stations (cups, lids, sleeves, syrups). 5. Wipe down counters, tables, and the condiment bar. 6. Sweep and mop all floors. 7. Count the cash drawer and secure it. 8. Lock all doors.",
  "calibrate the grinder": "1. Empty the hopper of all beans. 2. Run the grinder to clear any remaining grounds. 3. Turn the adjustment collar to a finer setting. 4. Add a small amount of fresh beans. 5. Pull a test shot and time it, aiming for 25-30 seconds. 6. Adjust the collar as needed and repeat until the target time is achieved.",
  "restock inventory": "1. Check milk levels in all refrigerators and restock from the back cooler. 2. Refill all syrup bottles at the bar. 3. Restock cup, lid, and sleeve dispensers for all sizes. 4. Check pastry case and bring out fresh items if needed. 5. Refill bean hoppers for all grinders.",
  "handle a customer complaint": "1. Listen actively and empathetically to the customer's concern. 2. Apologize sincerely for the issue. 3. Offer a solution, such as remaking the drink or providing a refund. 4. Thank the customer for their feedback. 5. Inform the shift supervisor of the incident."
}
```

### 1.2. Create Knowledge Base Documents
For this demo, you will need to create three PDF files with recipe content. Create text files with the content below and save them as PDFs inside the `perfect-blend-demo/knowledge_base/documents/` directory.

**Content for `hot_drinks.pdf`:**
> **Official Hot Drink Recipes**
>
> **Caffè Latte**
> - Ingredients: 1-2 shots of espresso, steamed milk, 1/4 inch of foam.
> - Steps: 1. Pull espresso shot(s) into the cup. 2. Steam milk to 150-160°F. 3. Pour steamed milk over espresso, holding back foam. 4. Top with the remaining foam.
>
> **Cappuccino**
> - Ingredients: 1-2 shots of espresso, equal parts steamed milk and foam.
> - Steps: 1. Pull espresso shot(s) into the cup. 2. Steam milk, creating a thick layer of microfoam. 3. Pour milk into espresso, ensuring an equal distribution of milk and foam.

**Content for `cold_drinks.pdf`:**
> **Official Cold Drink Recipes**
>
> **Venti Iced Caramel Macchiato**
> - Ingredients: 3 pumps of vanilla syrup, milk, ice, 2 shots of espresso, caramel drizzle.
> - Steps: 1. Pump vanilla syrup into a Venti-sized cold cup. 2. Fill the cup with milk to the third black line. 3. Add ice, leaving about 1/2 inch of room at the top. 4. Queue 2 shots of espresso. 5. Pour the espresso shots slowly over the top of the ice. 6. Top with caramel drizzle in a crosshatch pattern.
>
> **Iced Coffee**
> - Ingredients: Chilled brewed coffee, ice. Optional: classic syrup, milk.
> - Steps: 1. Pump classic syrup if requested. 2. Fill cup with iced coffee to the third line. 3. Add ice. 4. Top with milk if requested.

**Content for `seasonal_specials.pdf`:**
> **Official Seasonal Specials**
>
> **Pumpkin Spice Latte**
> - Ingredients: 1-2 shots espresso, 4 pumps pumpkin spice sauce, steamed milk, whipped cream, pumpkin spice topping.
> - Steps: 1. Pump sauce into cup. 2. Pull espresso shots over sauce. 3. Swirl to combine. 4. Add steamed milk. 5. Top with whipped cream and pumpkin spice topping.

## Step 2: Define and Import the Knowledge Base

The `Recipe_Expert_Agent` will use this knowledge base to answer questions about drink recipes. This configuration creates a built-in Milvus knowledge base that ingests and indexes the content of our PDF documents.

**File:** `perfect-blend-demo/knowledge_base/company_recipe_book_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: Company_Recipe_Book
description: >
  Contains all official recipes for hot, cold, and seasonal beverages. Use this to answer any question about how to make a drink, including specific ingredients, measurements, and step-by-step preparation instructions.
documents:
  - "./knowledge_base/documents/hot_drinks.pdf"
  - "./knowledge_base/documents/cold_drinks.pdf"
  - "./knowledge_base/documents/seasonal_specials.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

**Import the Knowledge Base:**
Run the following command from the root of your `perfect-blend-demo` directory.
```bash
orchestrate knowledge-bases import -f ./knowledge_base/company_recipe_book_kb.yaml
```

## Step 3: Create and Import the Custom Tool

This Python tool provides the `Store_Ops_Agent` with the ability to look up procedures from our mock `procedures.json` file. The `@tool` decorator makes the function discoverable by Orchestrate, and the docstring serves as the description that the agent uses to understand the tool's capability.

**Business Value:** This pattern demonstrates how Orchestrate can connect an LLM-based agent to any internal system of record, API, or database. By encapsulating the data retrieval logic in a tool, the agent can access real-time, structured information to provide accurate answers for operational questions, reducing errors and ensuring compliance with standard procedures.

**File:** `perfect-blend-demo/tools/store_procedures_tool.py`
```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_store_procedure", permission=ToolPermission.ADMIN)
def get_store_procedure(procedure_name: str) -> str:
    """
    Retrieves the official, step-by-step instructions for a given store operating procedure. Use this tool to answer questions about how to perform operational tasks like cleaning equipment, following checklists, or handling specific situations.

    Args:
        procedure_name (str): The name of the procedure to look up. Examples include "closing checklist", "clean espresso machine", or "calibrate the grinder".

    Returns:
        str: The detailed steps for the procedure, or a message indicating the procedure was not found.
    """
    try:
        # It's important to use a relative path that works from where the orchestrate command is run
        with open('./tools/procedures.json', 'r') as f:
            procedures = json.load(f)
        # Use case-insensitive matching for robustness
        return procedures.get(procedure_name.lower(), f"I'm sorry, I couldn't find a procedure named '{procedure_name}'.")
    except FileNotFoundError:
        return "Error: The procedures data file could not be found. Please check the system configuration."
    except json.JSONDecodeError:
        return "Error: The procedures data file is not formatted correctly."

```

**Import the Tool:**
Run the following command from the root of your `perfect-blend-demo` directory.
```bash
orchestrate tools import -f ./tools/store_procedures_tool.py
```

## Step 4: Define the Agent Configurations

With our data, knowledge base, and tool in place, we now define the three agents. We will create the collaborator agents first, followed by the supervisor agent that orchestrates them.

### 4.1. Recipe Expert Agent (Collaborator)
This agent's sole purpose is to leverage the `Company_Recipe_Book` knowledge base to answer recipe-related questions. Its description is crucial for the supervisor to know when to route requests to it.

**File:** `perfect-blend-demo/agents/Recipe_Expert_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Recipe_Expert_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An expert agent for all beverage recipes. Use this agent for any question related to making a drink, including ingredients, measurements, steps, or variations. It has access to the official company recipe book.
instructions: >
  You are a master barista trainer. Your only job is to provide clear, accurate, and step-by-step instructions for making drinks based on the information in your knowledge base. If asked a question not about a recipe, state that you can only help with drink recipes.
knowledge_base:
  - Company_Recipe_Book
```

### 4.2. Store Operations Agent (Collaborator)
This agent specializes in operational procedures by using the `get_store_procedure` tool. Its description clearly states its capabilities, enabling the supervisor to delegate tasks effectively.

**File:** `perfect-blend-demo/agents/Store_Ops_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Store_Ops_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent for all store operations and procedures. Use this agent for questions about cleaning equipment, opening or closing checklists, inventory management, or how to perform any non-beverage-making task.
instructions: >
  You are an experienced store operations manager. Your goal is to provide official procedures for store tasks.
  When a user asks how to do something, use the 'get_store_procedure' tool to find the relevant instructions.
  Present the steps clearly to the user.
tools:
  - get_store_procedure
```

### 4.3. Barista Concierge Agent (Supervisor)
This is the primary agent the user interacts with. It holds no specialized tools or knowledge itself. Instead, its `instructions` define its persona and, most importantly, the reasoning logic for delegating tasks to its `collaborators`.

**File:** `perfect-blend-demo/agents/Barista_Concierge_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Barista_Concierge_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A helpful AI assistant for baristas, acting as a single point of contact. It can answer questions about drink recipes and store operations by collaborating with other expert agents.
instructions: >
  Persona:
  - Your purpose is to be the "Barista Buddy", a friendly and encouraging assistant for new hires.
  - I will be a new barista asking for help.
  - You will understand my question and route it to the correct expert to get me the answer.

  Reasoning:
  - If the user asks "how to make", "what's in", or any question about a specific drink or beverage recipe, use the Recipe_Expert_Agent.
  - If the user asks about a store process, a checklist, "how to clean", "how to calibrate", or any operational task, use the Store_Ops_Agent.
  - If the user's query is ambiguous, ask a clarifying question before routing to an agent. For example, if they ask about "macchiato", ask if they mean the recipe or how to ring it up.
collaborators:
  - Recipe_Expert_Agent
  - Store_Ops_Agent
```

## Step 5: Define Dependencies and Import Agents

### 5.1. Create `requirements.txt`
This file lists the Python packages required for the custom tool. While our tool only uses standard libraries, it's a best practice to include this file.
**File:** `perfect-blend-demo/requirements.txt`
```
ibm-watsonx-orchestrate
```

### 5.2. Import the Agents
It is critical to import collaborator agents *before* the supervisor agent that depends on them. Run these commands sequentially from the root of your project directory.

```bash
# 1. Import the Recipe Expert collaborator
orchestrate agents import -f ./agents/Recipe_Expert_Agent.yaml

# 2. Import the Store Ops collaborator
orchestrate agents import -f ./agents/Store_Ops_Agent.yaml

# 3. Import the Supervisor agent
orchestrate agents import -f ./agents/Barista_Concierge_Agent.yaml
```

## Verification
After successfully importing all components, you can test the complete solution by interacting with the supervisor agent.

1.  **Start the Chat Interface**: Launch the Orchestrate chat, specifying the `Barista_Concierge_Agent` as the entry point.
    ```bash
    orchestrate chat start --agent Barista_Concierge_Agent
    ```
2.  **Run Demo Scenarios**: Test the scenarios outlined in the client concept.
    *   **Recipe Retrieval**: Type: `"How do I make a venti iced caramel macchiato?"`
        *   **Expected Outcome**: The `Barista_Concierge_Agent` should delegate to the `Recipe_Expert_Agent`, which will retrieve and display the step-by-step instructions from the `cold_drinks.pdf` document.
    *   **Procedural Guidance**: Type: `"What are the steps for calibrating the grinder?"`
        *   **Expected Outcome**: The `Barista_Concierge_Agent` should delegate to the `Store_Ops_Agent`, which will execute the `get_store_procedure` tool with the argument `"calibrate the grinder"` and return the steps from `procedures.json`.
    *   **Ambiguous Query Handling**: Type: `"I need to get the store ready for closing."`
        *   **Expected Outcome**: The `Barista_Concierge_Agent` should understand the intent, delegate to the `Store_Ops_Agent`, which will use its tool to retrieve the `"closing checklist"` procedure and present it to the user.

## Troubleshooting

*   **Agent Import Fails**: If an agent import fails with a "collaborator not found" error, ensure you are importing agents in the correct order (collaborators first, then supervisor). Verify the `name` in the collaborator's YAML matches the entry in the supervisor's `collaborators` list.
*   **Knowledge Base Not Working**: If the `Recipe_Expert_Agent` cannot answer questions, check the knowledge base status with `orchestrate knowledge-bases status --name Company_Recipe_Book`. Ensure the status is `Ready`. Also, verify the file paths in `company_recipe_book_kb.yaml` are correct relative to where you are running the command.
*   **Tool Not Found/Failing**: If the `Store_Ops_Agent` fails, first verify the tool was imported successfully. Check for typos in the tool name in the agent's YAML. Ensure the `procedures.json` file exists at the specified path (`./tools/procedures.json`) and contains valid JSON.
*   **Incorrect Routing**: If the `Barista_Concierge_Agent` sends a query to the wrong collaborator, refine its `instructions` and the `description` of the collaborator agents. The descriptions are critical for the supervisor's routing decisions. Make them as distinct and descriptive as possible. Use the `--debug` flag (`orchestrate --debug ...`) to see more detailed logs.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
