# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 19:32:01
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy Demo (Iteration 2)

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying the **"Barista Buddy: AI-Powered Onboarding & Operations Assistant"** for the client. This demonstration is meticulously tailored to address the client's specific challenges within the fast-paced coffee shop environment, focusing on accelerating new hire training, ensuring product consistency, and increasing operational efficiency. This plan is an enhanced version of the previous iteration, incorporating feedback to create a more robust and sophisticated solution.

The plan implements a multi-agent architecture using the supervisor-collaborator pattern, a core strength of IBM watsonx Orchestrate. The `Barista_Buddy_Assistant` will act as the primary user interface, intelligently routing barista queries to specialized collaborator agents: the `Recipe_Expert_Agent`, which uses a knowledge base for drink recipes via Retrieval-Augmented Generation (RAG), and the `Operations_Support_Agent`, which uses custom Python tools to handle inventory and equipment issues. This approach showcases how watsonx Orchestrate can create a sophisticated, scalable, and highly effective digital assistant to meet specific business needs.

## 2. Prerequisites

Before starting, ensure your environment is set up with the following components. This setup is crucial for the successful creation and deployment of the agents and tools outlined in this plan.

*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured. This is the primary toolset for building, importing, and managing agents, tools, and knowledge bases.
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
*   **Active Orchestrate Environment:** You must have an active watsonx Orchestrate environment (either local Developer Edition or a cloud instance) initialized and ready for use.
    ```bash
    # Example for initializing a new environment and activating it
    orchestrate env add
    orchestrate env activate <your_env_name>
    ```
*   **Python 3.9+:** A compatible version of Python is required to create the custom tools for the `Operations_Support_Agent`.
*   **Project Directory Structure:** Create a dedicated directory for this project to keep all configuration files, tools, and mock data organized. This structure is essential for the relative paths used in the configuration files.
    ```bash
    mkdir barista-buddy-demo
    cd barista-buddy-demo
    mkdir -p mock_data/recipes
    mkdir -p mock_data/procedures
    touch requirements.txt
    ```

## 3. Step-by-Step Instructions

This section details the creation of all components, from mock data and knowledge bases to the final supervisor agent, culminating in a fully functional demo.

### Step 1: Create Mock Data and Knowledge Base

The `Recipe_Expert_Agent` relies on Retrieval-Augmented Generation (RAG) to provide accurate answers grounded in official documentation. We will populate a knowledge base with mock PDF documents containing recipes and procedures, which serves as the "source of truth" for the agent. This step is foundational to demonstrating how Orchestrate can reduce hallucinations and provide reliable, context-aware information.

**A. Create Mock Data Files**

Create the following PDF files inside the `mock_data/` subdirectories with the specified content. These documents simulate the client's real-world training materials.

1.  **File:** `mock_data/recipes/caramel_macchiato.pdf`
    **Content:**
    > **Venti Iced Caramel Macchiato**
    > **Ingredients:**
    > - 2 shots of espresso
    > - Vanilla syrup (5 pumps)
    > - Milk (to the top line of the cup)
    > - Ice
    > - Caramel drizzle
    > **Instructions:**
    > 1. Pump 5 pumps of vanilla syrup into a venti cup.
    > 2. Queue 2 shots of espresso.
    > 3. Pour milk to the top black line of the cup.
    > 4. Add ice, leaving about 1/2 inch of room at the top.
    > 5. Pour the 2 espresso shots over the top of the ice.
    > 6. Finish with a crosshatch pattern of caramel drizzle.
    > **Pro-Tip:** Do not stir the drink. The layers are intentional.

2.  **File:** `mock_data/recipes/cold_brew_process.pdf`
    **Content:**
    > **Cold Brew Coffee - 24 Hour Process**
    > **Ingredients:**
    > - 5 lbs coarse-ground coffee beans
    > - 7 liters of cold, filtered water
    > **Instructions:**
    > 1. Place the coffee grounds in the toddy filter bag.
    > 2. Slowly pour 7 liters of water over the grounds, ensuring all grounds are saturated.
    > 3. Let the coffee steep at room temperature for 24 hours.
    > 4. After steeping, drain the concentrate into a sealed container.
    > 5. Date the container. The concentrate is good for 14 days.
    > **Serving:** Dilute with water or milk at a 1:1 ratio.

3.  **File:** `mock_data/procedures/espresso_machine_cleaning.pdf`
    **Content:**
    > **Espresso Machine Daily Cleaning Procedure**
    > **End of Day Task**
    > **Steps:**
    > 1. Insert the blind filter basket into the portafilter.
    > 2. Add a small amount of cleaning powder (Cafiza).
    > 3. Lock the portafilter into the group head.
    > 4. Run the brew cycle for 10 seconds, then stop for 10 seconds. Repeat 5 times.
    > 5. Remove the portafilter and rinse the blind basket.
    > 6. Re-insert the portafilter and repeat step 4 with only water to rinse.
    > 7. Wipe down the group head and shower screen with a clean cloth.

**B. Define the Knowledge Base Configuration**

Create a YAML file that defines the knowledge base. This file instructs Orchestrate to ingest the specified documents into its built-in Milvus vector database, making their content searchable by the agent.

**File:** `recipe_kb.yaml`

```yaml
spec_version: v1
kind: knowledge_base
name: barista_recipe_knowledge_base
description: >
  Contains all official company recipes for hot and cold beverages, 
  as well as standard operating procedures for equipment cleaning and maintenance. 
  This is the primary source of truth for how to make drinks and perform daily tasks.
documents:
  - "mock_data/recipes/caramel_macchiato.pdf"
  - "mock_data/recipes/cold_brew_process.pdf"
  - "mock_data/procedures/espresso_machine_cleaning.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 2: Create Custom Python Tools

The `Operations_Support_Agent` requires custom tools to interact with external systems (simulated here) and perform actions. We will create these tools in a single Python file using the `@tool` decorator. The docstrings are critical, as they provide the agent with the necessary context to understand when and how to use each tool, effectively serving as the tool's API documentation for the LLM.

**A. Implement the Tools**

This file contains the logic for checking inventory and reporting equipment issues. The `check_inventory` tool has been enhanced to handle ambiguous user queries, a common real-world challenge. This showcases the ability to build more intelligent and user-friendly tools.

**File:** `operations_tools.py`

```python
import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock inventory database, simulating a real-time connection to a stock management system.
# We've included items with similar names to test ambiguity handling.
INVENTORY = {
    'espresso_beans_kg': 5.5,
    'oat_milk_cartons': 12,
    'vanilla_syrup_bottles': 3,
    'caramel_syrup_bottles': 6,
    'sugar_free_caramel_syrup_bottles': 2,
    'mocha_sauce_bottles': 4,
    'white_mocha_sauce_bottles': 0,
    'grande_hot_cups_sleeve': 8,
    'venti_cold_cups_sleeve': 11
}

@tool(name="check_inventory", permission=ToolPermission.ADMIN)
def check_inventory(item_name: str) -> str:
    """
    Checks the current stock level for a specific inventory item. Use this tool
    when a user asks about the quantity of an item, such as 'how many vanilla syrup bottles do we have'.

    Args:
        item_name (str): The specific name of the inventory item to check.
                         Example format: 'vanilla_syrup_bottles', 'espresso_beans_kg'.

    Returns:
        str: A message indicating the current stock level, asking for clarification if the item is ambiguous, or stating if the item is not found.
    """
    normalized_item = item_name.lower().replace(" ", "_")
    
    # First, try for an exact match
    if normalized_item in INVENTORY:
        stock_level = INVENTORY[normalized_item]
        return f"We currently have {stock_level} units of {normalized_item} in stock."

    # If no exact match, search for partial matches
    possible_matches = [key for key in INVENTORY.keys() if normalized_item in key]
    
    if len(possible_matches) == 1:
        found_key = possible_matches[0]
        stock_level = INVENTORY[found_key]
        return f"We currently have {stock_level} units of {found_key} in stock."
    elif len(possible_matches) > 1:
        # If multiple matches are found, ask the user for clarification.
        options = ", ".join(possible_matches)
        return f"I found multiple items matching '{item_name}'. Can you be more specific? Options are: {options}."
    else:
        return f"Sorry, I could not find the item '{item_name}' in the inventory system."

@tool(name="report_equipment_issue", permission=ToolPermission.ADMIN)
def report_equipment_issue(equipment_name: str, issue_description: str) -> str:
    """
    Logs a maintenance ticket for a piece of broken or malfunctioning equipment.
    Use this when a user reports a problem like 'the grinder is making a weird noise' or 'the espresso machine is leaking'.

    Args:
        equipment_name (str): The name of the equipment that is broken (e.g., 'Espresso Grinder', 'Main Ice Machine').
        issue_description (str): A detailed description of the problem.

    Returns:
        str: A confirmation message with a generated ticket number.
    """
    ticket_id = random.randint(10000, 99999)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # This print block simulates logging to a backend system or service desk application.
    print(f"--- MOCK TICKETING SYSTEM ---")
    print(f"Timestamp: {timestamp}")
    print(f"Equipment: {equipment_name}")
    print(f"Issue: {issue_description}")
    print(f"Ticket ID: {ticket_id}")
    print(f"---------------------------")
    
    return f"SUCCESS: I've logged the issue for '{equipment_name}' with description '{issue_description}'. Your ticket number is #{ticket_id}."
```

**B. Create requirements.txt**

While our tools only use standard libraries, including a `requirements.txt` file is a best practice for managing dependencies in any Python project. If you were to add libraries like `requests`, you would list them here.

**File:** `requirements.txt`
```text
# No external packages required for this demo.
# Add packages like 'requests' or 'pandas' here if needed.
```

### Step 3: Define the Agent Configurations (YAML)

We will now define the three agents in our architecture: two specialized collaborators and one supervisor to orchestrate them. The `description` fields are paramount, as they are used by the supervisor agent to determine where to route a user's request.

**A. Collaborator 1: Recipe Expert Agent**

This agent's sole purpose is to be an expert on recipes and procedures, leveraging the knowledge base we defined. Its instructions and description are tightly scoped to prevent it from attempting tasks outside its expertise.

**File:** `recipe_expert_agent.yaml`

```yaml
spec_version: v1
kind: native
name: Recipe_Expert_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent with deep knowledge of all beverage recipes, ingredients, customizations, 
  and preparation steps. It also knows about standard operational procedures like cleaning tasks. 
  Use this agent for any questions related to "how to make" a drink or "how to perform" a store procedure.
instructions: >
  You are an expert barista trainer. Your sole purpose is to provide clear, accurate, and step-by-step 
  instructions based on the official documents in your knowledge base. When asked for a recipe or procedure, 
  consult the knowledge base and present the information in an easy-to-follow format. Do not answer questions 
  outside of this scope. If the information is not in the knowledge base, state that you cannot find the procedure.
collaborators: []
tools: []
knowledge_base:
  - barista_recipe_knowledge_base
```

**B. Collaborator 2: Operations Support Agent**

This agent handles operational tasks by executing the custom Python tools. Its description clearly outlines its capabilities related to inventory and maintenance, making it easy for the supervisor to delegate appropriate tasks.

**File:** `operations_support_agent.yaml`

```yaml
spec_version: v1
kind: native
name: Operations_Support_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent that handles day-to-day operational procedures, including checking inventory levels and 
  reporting equipment issues. Use this agent for requests about stock counts or to log a ticket for broken equipment.
instructions: >
  You are an operations support specialist for a coffee shop.
  - When a user asks about the quantity of an item, use the `check_inventory` tool to find the current stock level.
  - When a user reports that a piece of equipment is broken or malfunctioning, use the `report_equipment_issue` 
    tool to create a maintenance ticket. Be sure to capture the equipment name and a description of the problem from the user's request.
collaborators: []
tools:
  - check_inventory
  - report_equipment_issue
```

**C. Supervisor: Barista Buddy Assistant**

This is the main, user-facing agent. It acts as an intelligent router or orchestrator. Its instructions explicitly tell it *not* to perform tasks itself but to delegate to the correct specialist based on the user's intent. This demonstrates a key scalable pattern in watsonx Orchestrate.

**File:** `barista_buddy_assistant.yaml`

```yaml
spec_version: v1
kind: native
name: Barista_Buddy_Assistant
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A helpful AI assistant for baristas. It can answer questions about drink recipes by consulting the Recipe Expert,
  and can help with operational tasks like checking inventory or reporting broken equipment by consulting the Operations Expert.
instructions: >
  You are the primary Barista Buddy assistant. Your main goal is to understand the user's request and route it to the correct 
  specialist collaborator. You do not perform tasks yourself.
  - For any questions about how to make drinks, ingredients, recipes, or how to perform a procedure, use the `Recipe_Expert_Agent`.
  - For questions about inventory levels, stock counts, or if a user reports broken equipment, use the `Operations_Support_Agent`.
collaborators:
  - Recipe_Expert_Agent
  - Operations_Support_Agent
tools: []
```

### Step 4: Import and Deploy the Components

With all files created, we use the ADK CLI to import them into watsonx Orchestrate. The order is critical: dependencies like tools and knowledge bases must be imported before the agents that use them. Collaborator agents must be imported before the supervisor agent that collaborates with them.

**Execute these commands from your project root (`barista-buddy-demo/`) directory:**

1.  **Import the Custom Tools:** This makes the Python functions available as executable tools within Orchestrate.
    ```bash
    orchestrate tools import -f operations_tools.py
    ```
2.  **Import the Knowledge Base:** This command ingests the PDF documents and creates the vector index.
    ```bash
    orchestrate knowledgebases import -f recipe_kb.yaml
    ```
3.  **Import the Collaborator Agents:** These are the specialist agents that will perform the actual work.
    ```bash
    orchestrate agents import -f recipe_expert_agent.yaml
    orchestrate agents import -f operations_support_agent.yaml
    ```
4.  **Import the Supervisor Agent:** This is the final step, bringing the user-facing agent online.
    ```bash
    orchestrate agents import -f barista_buddy_assistant.yaml
    ```

## 4. Verification and Demo Scenarios

After successfully importing all components, start the interactive chat to test the solution. This is where you will demonstrate the value to the client by running through their key use cases.

**Start the chat session:**

```bash
orchestrate chat start
```

Once the chat interface is running, test the following scenarios as outlined in the demo concept:

*   **Scenario 1 (Knowledge Base Retrieval):**
    *   **User Input:** `How do I make a venti iced caramel macchiato?`
    *   **Expected Behavior:** The `Barista_Buddy_Assistant` routes to the `Recipe_Expert_Agent`. The agent queries the `barista_recipe_knowledge_base`, finds the relevant information in the PDF, and returns a formatted, step-by-step guide.

*   **Scenario 2 (Custom Tool Execution - Inventory):**
    *   **User Input:** `How many bottles of vanilla syrup do we have left?`
    *   **Expected Behavior:** The `Barista_Buddy_Assistant` routes to the `Operations_Support_Agent`. The agent executes the `check_inventory` tool with `item_name='vanilla_syrup_bottles'`, which looks up the value and returns: "We currently have 3 units of vanilla_syrup_bottles in stock."

*   **Scenario 3 (Custom Tool Execution - Ticketing):**
    *   **User Input:** `The main grinder is making a weird buzzing sound.`
    *   **Expected Behavior:** The `Barista_Buddy_Assistant` routes to the `Operations_Support_Agent`. The agent executes the `report_equipment_issue` tool, passing the equipment name and description. The tool simulates creating a ticket and returns a confirmation message, such as: "SUCCESS: I've logged the issue for 'main grinder'... Your ticket number is #12345."

*   **Scenario 4 (Tool Logic - Ambiguity Handling):**
    *   **User Input:** `How much caramel syrup is left?`
    *   **Expected Behavior:** The `Barista_Buddy_Assistant` routes to the `Operations_Support_Agent`. The `check_inventory` tool finds multiple matches (`caramel_syrup_bottles`, `sugar_free_caramel_syrup_bottles`) and returns a clarifying question: "I found multiple items matching 'caramel syrup'. Can you be more specific? Options are: caramel_syrup_bottles, sugar_free_caramel_syrup_bottles."

## 5. Troubleshooting

*   **Agent Routing Issues:** If the `Barista_Buddy_Assistant` fails to route correctly, review the `description` fields in the collaborator agent YAML files and the `instructions` in the supervisor agent YAML. The supervisor relies heavily on these descriptions to make routing decisions. Ensure they are distinct and accurately describe each collaborator's capabilities.
*   **Tool Not Found Error:** If an agent reports it cannot find a tool, ensure `orchestrate tools import` was run *before* importing the `Operations_Support_Agent`. Verify the tool names in `operations_support_agent.yaml` exactly match the `@tool` function names in `operations_tools.py`.
*   **Knowledge Base Not Working:** If the `Recipe_Expert_Agent` cannot answer questions, verify the `orchestrate knowledgebases import` command completed without errors. Check that the file paths in `recipe_kb.yaml` are correct relative to where you are running the command.
*   **Python Tool Errors:** If a tool fails during execution (e.g., after the ambiguity handling change), check the console output where you ran `orchestrate chat start` for any Python tracebacks. This can help debug logic issues within the tool's code.

## 6. Best Practices

*   **Descriptive Naming and Descriptions:** Use clear, unique names for all assets. The agent `description` fields are not just for users; they are critical for supervisor agents to perform routing. The more descriptive and distinct they are, the better the routing performance.
*   **Modular Design (Supervisor-Collaborator):** The architecture used here is highly scalable. New capabilities can be added by creating a new specialist agent (e.g., `HR_Support_Agent` for payroll) and adding it to the `Barista_Buddy_Assistant`'s collaborator list, without modifying existing agents.
*   **Explicit Instructions:** The `instructions` field in a native agent's YAML is powerful. Be direct and explicit about how the agent should behave, what tools it should use, and what its persona should be. This significantly improves reliability and predictability.
*   **Detailed Tool Docstrings:** For Python tools, the Google-style docstring is not just for documentation. The LLM reads the docstring, including the `Args` section, to understand what the tool does and what parameters it requires. A well-written docstring is essential for the agent to use the tool correctly and reliably.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
