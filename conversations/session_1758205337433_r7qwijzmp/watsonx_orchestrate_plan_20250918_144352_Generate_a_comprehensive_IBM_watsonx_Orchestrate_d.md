# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 14:43:52
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: The AI-Powered Barista Coach

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Barista Coach," a multi-agent system for a retail coffee client, as outlined in the provided strategic demo concept. This solution addresses the client's core business needs for accelerated onboarding, enhanced consistency, and increased operational efficiency in a fast-paced retail environment. By leveraging the IBM watsonx Orchestrate Agent Development Kit (ADK), we will construct a supervisor agent (`barista_coach_agent`) that intelligently delegates tasks to specialized collaborator agents for drink recipes, store procedures, and promotions. This plan details the creation of all required agents, custom Python tools, knowledge bases, and mock data, culminating in a fully functional demo that showcases the power of a sophisticated, multi-agent architecture.

## Prerequisites

Before beginning, ensure your development environment is correctly configured. This is crucial for the successful creation and deployment of the agents and their components.

1.  **IBM watsonx Orchestrate ADK Installed**: The Agent Development Kit (ADK) must be installed and configured. This includes the Python library and the `orchestrate` CLI.
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
2.  **Active watsonx Orchestrate Environment**: You must have an active environment initialized. This could be the local Developer Edition or a cloud-based SaaS environment.
    ```bash
    # Example for initializing a local environment
    orchestrate env init local-dev -u http://localhost:8765
    orchestrate env use local-dev
    ```
3.  **Python 3.9+**: A compatible version of Python is required for creating custom tools.
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing YAML, Python, and text files.
5.  **Project Directory Structure**: Create the following folder structure to organize all the files for this demo. This structure is essential for the CLI commands to work correctly.
    ```
    barista_coach_demo/
    ├── agents/
    │   ├── barista_coach_agent.yaml
    │   ├── recipe_master_agent.yaml
    │   ├── store_ops_pro_agent.yaml
    │   └── promo_pro_agent.yaml
    ├── tools/
    │   ├── promotions_tool.py
    │   └── recipe_tool.py
    ├── mock_data/
    │   ├── drink_recipes.pdf
    │   └── store_procedures.docx
    ├── knowledge_bases/
    │   ├── recipe_kb.yaml
    │   └── store_procedures_kb.yaml
    └── requirements.txt
    ```

## Step 1: Create Mock Data and `requirements.txt`

The foundation of our agent's knowledge lies in realistic data. We will create the source documents for our knowledge bases and a `requirements.txt` file for our Python tools.

1.  **Create `requirements.txt`**: This file lists the Python dependencies for our custom tools. Place this in the root of your `barista_coach_demo` directory.
    ```text
    # requirements.txt
    pydantic
    ```

2.  **Create `drink_recipes.pdf`**: In the `mock_data/` directory, create a PDF file named `drink_recipes.pdf`. For this demo, you can create a simple text file and save it as a PDF. Add the following content, which will be ingested by our `Recipe_KB` knowledge base for basic recipe lookups.

    **File:** `mock_data/drink_recipes.pdf`
    ```text
    Starbucks Standard Drink Recipes

    Caffè Latte (Grande)
    - Ingredients: 2 shots of Espresso, Steamed 2% Milk, 1/4 inch of foam.
    - Steps:
      1. Pull 2 shots of espresso into the cup.
      2. Steam 2% milk to 150-160°F.
      3. Pour steamed milk over espresso, leaving a small layer of foam on top.

    Caramel Macchiato (Grande)
    - Ingredients: 2 shots of Espresso, Steamed 2% Milk, Vanilla Syrup (3 pumps), Caramel Drizzle.
    - Steps:
      1. Pump 3 pumps of vanilla syrup into the cup.
      2. Add steamed 2% milk.
      3. Pull 2 shots of espresso and pour them over the milk (marking the foam).
      4. Top with caramel drizzle in a crosshatch pattern.

    Pike Place Roast (Grande)
    - Ingredients: Freshly brewed Pike Place Roast coffee.
    - Steps:
      1. Pour brewed coffee into the cup, leaving about 1 inch of room for cream and sugar if requested.
    ```

3.  **Create `store_procedures.docx`**: In the `mock_data/` directory, create a Word document named `store_procedures.docx`. Add the following content. This document will populate the `Store_Procedures_KB` knowledge base.

    **File:** `mock_data/store_procedures.docx`
    ```text
    Starbucks Standard Operating Procedures (SOPs)

    Morning Opening Checklist
    1.  Unlock doors and disable alarm.
    2.  Perform cash register till count and setup.
    3.  Turn on all espresso machines, ovens, and brewers.
    4.  Brew the first batch of Pike Place Roast and dark roast.
    5.  Restock milk, syrups, and pastries at the front line.
    6.  Sanitize all countertops and condiment bars.

    Espresso Machine Cleaning Guide (Closing)
    1.  Press and hold the 1 and 2 shot buttons simultaneously to start the cleaning cycle.
    2.  Insert the blind filter basket into the portafilter.
    3.  Add one Cafiza cleaning tablet to the blind basket.
    4.  Lock the portafilter into the group head.
    5.  The machine will run a backflush cycle automatically. Repeat 5 times.
    6.  Remove the portafilter, rinse the blind basket, and run a water-only cycle to rinse.
    7.  Wipe down the group head and drip tray.
    ```

## Step 2: Configure Knowledge Bases

Knowledge bases allow our agents to perform Retrieval-Augmented Generation (RAG) on our mock data documents. We will use the built-in Milvus vector database provided by watsonx Orchestrate.

1.  **Create Recipe Knowledge Base YAML**: This configuration ingests the `drink_recipes.pdf` to answer questions about standard recipes.

    **Business Value**: This component directly addresses the need for consistent and accessible recipe knowledge, reducing reliance on memory or physical manuals and ensuring every barista can make standard drinks correctly.

    **File:** `knowledge_bases/recipe_kb.yaml`
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: Recipe_KB
    description: >
      Contains the official recipes and preparation instructions for all standard Starbucks beverages.
      Use this to answer general questions about how to make a drink.
    documents:
      - "mock_data/drink_recipes.pdf"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

2.  **Create Store Procedures Knowledge Base YAML**: This configuration ingests `store_procedures.docx` to answer questions about operational tasks.

    **Business Value**: This provides instant access to critical SOPs, improving compliance, safety, and efficiency. It empowers employees to find answers to procedural questions independently, freeing up supervisors for more complex tasks.

    **File:** `knowledge_bases/store_procedures_kb.yaml`
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: Store_Procedures_KB
    description: >
      Contains official Standard Operating Procedures (SOPs) for store operations, including
      opening and closing checklists, and equipment maintenance guides.
    documents:
      - "mock_data/store_procedures.docx"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 3: Create Custom Python Tools

Custom tools extend an agent's capabilities beyond knowledge bases, allowing for dynamic data retrieval and complex logic. We will create two tools as specified in the demo concept.

1.  **Create Promotions Tool (`promotions_tool.py`)**: This tool simulates a real-time API call to fetch current promotional offers.

    **Business Value**: In a real-world scenario, promotions change frequently. This tool pattern ensures baristas always have up-to-the-minute information, preventing errors in applying discounts and improving customer satisfaction. It demonstrates how Orchestrate can integrate with dynamic, external data sources.

    **Technical Implementation**: The `@tool` decorator registers the function as a watsonx Orchestrate tool. The function `get_current_promotions` contains a hardcoded list of dictionaries, simulating a JSON response from an external promotions API. The docstring is critical, as it provides the description the agent uses to understand the tool's purpose, inputs, and outputs.

    **File:** `tools/promotions_tool.py`
    ```python
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    from typing import List, Dict

    @tool(name="get_current_promotions", permission=ToolPermission.ADMIN)
    def get_current_promotions() -> List[Dict]:
        """
        Retrieves the list of currently active promotional offers and special deals.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains the 'name' and 'details' of an active promotion.
        """
        # This is mock data simulating a real-time API call to a promotions database.
        mock_promos = [
            {
                "name": "Happy Hour",
                "details": "50% off all Frappuccino blended beverages on Thursdays from 2-7 PM."
            },
            {
                "name": "Mobile Order Bonus",
                "details": "Earn 25 bonus Stars when you place a mobile order over $10."
            },
            {
                "name": "Double Star Day",
                "details": "Earn double stars on all purchases for loyalty members today."
            }
        ]
        return mock_promos
    ```

2.  **Create Parameterized Recipe Tool (`recipe_tool.py`)**: This tool handles complex, customized drink orders by parsing parameters and dynamically generating a recipe.

    **Business Value**: This tool goes beyond simple RAG to handle the reality of customer customizations. It demonstrates the agent's ability to perform complex reasoning, reduce order errors, and ensure even the most complex drinks are made consistently, directly impacting product quality and waste reduction.

    **Technical Implementation**: The `get_drink_recipe` function accepts multiple arguments with types (`size`, `milk`, `syrup_flavor`, `syrup_pumps`, `extra_shots`). This allows the agent to extract these specific parameters from a natural language request (e.g., "venti iced skinny vanilla latte with an extra shot"). The function then uses conditional logic to build a step-by-step recipe string based on the provided inputs, showcasing dynamic response generation.

    **File:** `tools/recipe_tool.py`
    ```python
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    from typing import Optional

    @tool(name="get_drink_recipe", permission=ToolPermission.ADMIN)
    def get_drink_recipe(
        size: str,
        drink_name: str,
        milk: Optional[str] = "2%",
        syrup_flavor: Optional[str] = None,
        syrup_pumps: Optional[int] = None,
        extra_shots: Optional[int] = 0
    ) -> str:
        """
        Generates a recipe for a customized Starbucks drink based on specific parameters.
        Use this for complex or modified drink requests, not for standard, unmodified drinks.

        Args:
            size (str): The size of the drink (e.g., 'grande', 'venti').
            drink_name (str): The base name of the drink (e.g., 'latte', 'macchiato').
            milk (str, optional): The type of milk to use. Defaults to "2%".
            syrup_flavor (str, optional): The flavor of syrup to add.
            syrup_pumps (int, optional): The number of pumps for the syrup.
            extra_shots (int, optional): The number of extra espresso shots to add.

        Returns:
            str: A formatted string containing the step-by-step recipe for the custom drink.
        """
        # Determine base shots based on size
        shots = 0
        if size.lower() == 'short':
            shots = 1
        elif size.lower() == 'tall':
            shots = 1
        elif size.lower() == 'grande':
            shots = 2
        elif size.lower() == 'venti':
            shots = 2 # Venti hot has 2, Venti iced has 3, but we'll simplify for the demo
        
        total_shots = shots + (extra_shots or 0)

        recipe_steps = [f"Recipe for a {size} {drink_name} with customizations:"]
        
        if syrup_flavor and syrup_pumps:
            recipe_steps.append(f"1. Pump {syrup_pumps} pumps of {syrup_flavor} syrup into the cup.")
        
        recipe_steps.append(f"2. Pull {total_shots} shots of espresso into the cup.")
        recipe_steps.append(f"3. Steam {milk} milk to the appropriate temperature.")
        recipe_steps.append(f"4. Pour steamed milk over the espresso.")
        recipe_steps.append("5. Finish with lid and serve.")

        return "\n".join(recipe_steps)
    ```

## Step 4: Define the Agent Architecture (YAML Files)

With the dependencies in place, we now define our agents using YAML configuration files. We'll start with the specialized collaborator agents and finish with the main supervisor agent.

1.  **Create `promo_pro_agent.yaml`**: This agent is the specialist for promotional information.

    **File:** `agents/promo_pro_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: promo_pro_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert agent that provides real-time information on all current promotional offers,
      loyalty program details, weekly deals, discounts, and special offers.
    instructions: >
      Your sole purpose is to provide information about current promotions.
      Use the 'get_current_promotions' tool to fetch the latest offers and present them clearly to the user.
      Do not answer questions about any other topic.
    tools:
      - get_current_promotions
    ```

2.  **Create `store_ops_pro_agent.yaml`**: The authority on standard operating procedures.

    **File:** `agents/store_ops_pro_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: store_ops_pro_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert agent on all standard operating procedures (SOPs).
      It can provide information on opening/closing checklists, equipment maintenance guides,
      and inventory management tasks by searching its knowledge base of official documents.
    instructions: >
      Your purpose is to answer questions about store operations and procedures.
      Use the knowledge base to find relevant information from the SOP documents.
      Provide clear, step-by-step instructions when available.
    knowledge_base:
      - Store_Procedures_KB
    ```

3.  **Create `recipe_master_agent.yaml`**: The expert on all beverage recipes, handling both simple and complex queries.

    **File:** `agents/recipe_master_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: recipe_master_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert agent for all beverage recipes. It can retrieve standard recipes from its knowledge base
      and generate recipes for customized drinks using its specialized tool.
    instructions: >
      You are an expert on drink recipes.
      - For simple, standard recipe questions (e.g., "how to make a latte"), use the 'Recipe_KB' knowledge base.
      - For complex or customized drink orders that include modifications like size, milk type, extra shots, or syrups
        (e.g., "recipe for a venti iced skinny vanilla latte with an extra shot"), you MUST use the 'get_drink_recipe' tool
        by extracting all the necessary parameters from the user's request.
    tools:
      - get_drink_recipe
    knowledge_base:
      - Recipe_KB
    ```

4.  **Create `barista_coach_agent.yaml` (Supervisor)**: This is the main agent that interacts with the user and delegates tasks.

    **Business Value**: The supervisor/collaborator pattern is the core of this solution's strategic value. It creates a scalable and maintainable system where expertise is modularized. The supervisor agent acts as an intelligent router, ensuring the user gets the most accurate answer from the correct specialist, which mirrors an efficient human team structure.

    **File:** `agents/barista_coach_agent.yaml`
    ```yaml
    spec_version: v1
    kind: native
    name: barista_coach_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A helpful AI assistant for Starbucks baristas. It acts as a primary coach that can answer
      questions about drink recipes, store operations, and current promotions by consulting
      with its team of specialist agents.
    instructions: >
      Your purpose is to assist baristas with their daily tasks by routing their questions to the correct expert.
      Carefully analyze the user's request to determine the topic.

      Routing Rules:
      - For ANY questions about how to make a drink, its ingredients, standard recipes, or drink customizations, you MUST use the 'recipe_master_agent'.
      - For ANY questions about store procedures, cleaning tasks, opening/closing duties, or operational checklists, you MUST use the 'store_ops_pro_agent'.
      - For ANY questions about weekly deals, discounts, loyalty offers, or current promotions, you MUST use the 'promo_pro_agent'.

      Do not attempt to answer questions yourself. Your only job is to delegate to the correct collaborator.
    collaborators:
      - recipe_master_agent
      - store_ops_pro_agent
      - promo_pro_agent
    tools: []
    ```

## Step 5: Import All Components using the ADK CLI

With all configuration files and tools created, we will now import them into watsonx Orchestrate in the correct dependency order. Run these commands from the root of your `barista_coach_demo` directory.

1.  **Import Knowledge Bases**: These have no dependencies and can be imported first.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/recipe_kb.yaml
    orchestrate knowledge-bases import -f knowledge_bases/store_procedures_kb.yaml
    ```
2.  **Import Tools**: Tools must exist before the agents that use them can be imported.
    ```bash
    orchestrate tools import -k python -f tools/promotions_tool.py -r requirements.txt
    orchestrate tools import -k python -f tools/recipe_tool.py -r requirements.txt
    ```
3.  **Import Collaborator Agents**: These agents depend on the tools and knowledge bases we just imported.
    ```bash
    orchestrate agents import -f agents/promo_pro_agent.yaml
    orchestrate agents import -f agents/store_ops_pro_agent.yaml
    orchestrate agents import -f agents/recipe_master_agent.yaml
    ```
4.  **Import Supervisor Agent**: Finally, import the main agent, which depends on the collaborator agents.
    ```bash
    orchestrate agents import -f agents/barista_coach_agent.yaml
    ```

## Verification Steps

After successfully importing all components, you can verify the solution by interacting with the `barista_coach_agent` in the chat interface.

1.  **Start the Chat**:
    ```bash
    orchestrate chat start --agent barista_coach_agent
    ```
2.  **Test Scenario 1 (Simple Recipe Query - RAG)**:
    *   **User Input**: `"How do I make a grande Pike Place?"`
    *   **Expected Behavior**: The `barista_coach_agent` should route the request to the `recipe_master_agent`. The `recipe_master_agent` should use its `Recipe_KB` knowledge base to retrieve and display the simple steps from the `drink_recipes.pdf` document.

3.  **Test Scenario 2 (Complex Recipe Query - Tool)**:
    *   **User Input**: `"What's the recipe for a venti latte with soy milk and an extra shot?"`
    *   **Expected Behavior**: The `barista_coach_agent` should route to `recipe_master_agent`. The `recipe_master_agent` should recognize the customizations and use the `get_drink_recipe` tool, passing the parameters (`size='venti'`, `drink_name='latte'`, `milk='soy'`, `extra_shots=1`). The tool will return a dynamically generated recipe string, which the agent will display.

4.  **Test Scenario 3 (Procedural Query - RAG)**:
    *   **User Input**: `"What are the steps for cleaning the espresso machine at closing?"`
    *   **Expected Behavior**: The `barista_coach_agent` should route this to the `store_ops_pro_agent`. This agent will search its `Store_Procedures_KB` knowledge base and return the official cleaning checklist from the `store_procedures.docx` document.

5.  **Test Scenario 4 (Promotion Query - Tool)**:
    *   **User Input**: `"Are there any special deals today?"`
    *   **Expected Behavior**: The `barista_coach_agent` should route this to the `promo_pro_agent`. This agent will execute the `get_current_promotions` tool and list the mock promotions defined in the Python file.

## Troubleshooting

-   **Agent Routing Issues**: If the `barista_coach_agent` fails to select the correct collaborator, review its `instructions`. The routing rules must be explicit and clear. Also, verify that the `description` of each collaborator agent accurately reflects its capabilities, as the supervisor uses these descriptions for routing decisions.
-   **Tool Not Found**: If an agent reports it cannot find a tool, ensure the tool was imported successfully using `orchestrate tools list`. Check for typos in the `tools` section of the agent's YAML file.
-   **Knowledge Base Not Working**: If a knowledge base query returns no results, verify the knowledge base was imported correctly (`orchestrate knowledge-bases list`) and that the file path in the YAML is correct relative to where you are running the import command.
-   **Python Tool Errors**: Use the `--debug` flag with the `orchestrate chat start` command to see more detailed logs. This can help identify runtime errors within your Python tool code. Ensure all dependencies from your tool are listed in `requirements.txt`.

## Best Practices

-   **Explicit Supervisor Instructions**: The success of the supervisor/collaborator pattern hinges on the supervisor's `instructions`. Be as direct and explicit as possible in the routing logic (e.g., "For ANY questions about X, you MUST use agent Y").
-   **Descriptive Collaborator Descriptions**: The supervisor agent relies heavily on the `description` field of collaborator agents to make routing decisions. Write clear, concise, and comprehensive descriptions that act as an "advertisement" for the agent's skills.
-   **Modular Design**: Keep agents and tools specialized. The `Recipe Master` handles only recipes, and the `Store Ops Pro` handles only procedures. This modularity makes the system easier to maintain, update, and scale. For example, adding a new `Inventory Pro` agent would be straightforward.
-   **Combine RAG and Tools**: This demo effectively shows the power of combining knowledge bases for static information (standard recipes, procedures) with tools for dynamic or complex logic (customized drinks, real-time promotions). This hybrid approach creates a more robust and capable agent.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
