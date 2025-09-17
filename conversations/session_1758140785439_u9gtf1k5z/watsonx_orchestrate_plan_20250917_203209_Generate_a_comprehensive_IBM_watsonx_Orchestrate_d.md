# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 20:32:09
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Culinary Onboarding Assistant

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Culinary Onboarding Assistant" for the client. The solution directly addresses the client's need for a scalable and efficient training tool for new culinary partners. By creating a multi-agent system using the IBM watsonx Orchestrate Agent Development Kit (ADK), we will build an intelligent assistant that automates responses to common queries about recipes, operational policies, and standard procedures. This will accelerate new hire productivity, ensure brand consistency, and reduce the training burden on senior staff, aligning with the project goal of achieving a **30-50% reduction in new hire ramp-up time**.

The architecture leverages a supervisor-collaborator pattern. A primary `Onboarding_Supervisor_Agent` acts as the user-facing interface, intelligently routing queries to specialized collaborator agents: a `Recipe_Expert_Agent` for culinary questions and a `Policy_Procedures_Agent` for operational inquiries. Each specialist agent utilizes a dedicated knowledge base built from the client's own documentation (mocked for this demo), demonstrating a powerful Retrieval-Augmented Generation (RAG) pattern for providing accurate, contextually-grounded answers.

## Prerequisites

Before beginning, ensure your development environment is correctly configured.

1.  **IBM watsonx Orchestrate ADK**: The ADK must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
2.  **Python Environment**: A working Python environment (version 3.9 or later) is required to create custom tools.
3.  **Orchestrate CLI**: You must have the `orchestrate` command-line tool installed, and you should be logged into your target environment (`orchestrate login`).
4.  **Project Directory**: Create a main project directory to organize all files. This plan will assume the following structure:

    ```
    culinary_demo/
    ├── agents/
    │   ├── policy_procedures_agent.yaml
    │   ├── recipe_expert_agent.yaml
    │   └── supervisor_agent.yaml
    ├── knowledge/
    │   ├── policy_kb.yaml
    │   └── recipe_kb.yaml
    ├── mock_data/
    │   ├── Classic_Marinara_Sauce.pdf
    │   ├── Employee_Code_of_Conduct.txt
    │   ├── End_of_Day_Closing_Procedures.html
    │   ├── Food_Safety_Handling_Policy.docx
    │   └── Perfect_Pizza_Dough.pdf
    ├── tools/
    │   └── recipe_tools.py
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Project Structure

First, create the directory structure outlined above. Then, create the synthetic documents that will populate our knowledge bases. This step is crucial for demonstrating the RAG capabilities without using proprietary client data.

**Action:** Create the following files inside the `mock_data/` directory. For the `.pdf` and `.docx` files, copy the provided text into a text editor and use the "Save As" or "Print to PDF" functionality to create the files in the correct format.

1.  **`mock_data/Classic_Marinara_Sauce.pdf`** (Save as PDF)
    ```text
    # Classic Marinara Sauce

    ## Ingredients
    - 28 ounces canned whole San Marzano tomatoes
    - 1/4 cup extra-virgin olive oil
    - 7 cloves garlic, thinly sliced
    - 1 small dried chili, or a pinch of crushed red pepper flakes
    - 1 teaspoon kosher salt
    - 1 large sprig fresh basil

    ## Instructions
    1.  Pour tomatoes into a large bowl and crush them with your hands.
    2.  In a large skillet over medium heat, heat the oil. Add garlic and cook, stirring, until fragrant and lightly golden.
    3.  Add the tomatoes, their juices, and the chili. Stir in the salt.
    4.  Place the basil sprig in the sauce. Simmer for about 20 minutes.
    5.  Remove basil and chili before serving.

    ## Pro-Tips
    For a richer flavor, add a parmesan rind while simmering.
    ```

2.  **`mock_data/Perfect_Pizza_Dough.pdf`** (Save as PDF)
    ```text
    # Perfect Pizza Dough

    ## Ingredients
    - 1 1/2 cups (355 ml) warm water (105°F-115°F)
    - 2 1/4 teaspoons active dry yeast
    - 1 tablespoon granulated sugar
    - 2 tablespoons olive oil
    - 4 cups (480g) all-purpose flour
    - 2 teaspoons fine sea salt

    ## Instructions
    1.  Combine water, yeast, and sugar in a bowl. Let stand for 5 minutes until foamy.
    2.  Stir in olive oil, flour, and salt.
    3.  Knead on a floured surface for 10-12 minutes until smooth.
    4.  Place in an oiled bowl, cover, and let rise for 1-1.5 hours until doubled.
    ```

3.  **`mock_data/Food_Safety_Handling_Policy.docx`** (Save as DOCX)
    ```text
    # Company Food Safety and Handling Policy

    ## Temperature Control
    Proper temperature control is critical to prevent foodborne illness.
    - All poultry products, including chicken, must be cooked to a minimum internal temperature of 165°F (74°C).
    - Ground meats must reach an internal temperature of 160°F (71°C).
    - Cold foods must be held at 40°F (4°C) or below.
    - Hot foods must be held at 140°F (60°C) or above.
    - Use a calibrated food thermometer to check temperatures.

    ## Cross-Contamination
    Prevent cross-contamination by separating raw meats from ready-to-eat foods. Use separate cutting boards, utensils, and plates for raw and cooked items.
    ```

4.  **`mock_data/Employee_Code_of_Conduct.txt`** (Save as TXT)
    ```text
    Employee Code of Conduct

    All employees are expected to maintain a high level of professionalism. This includes treating colleagues and partners with respect, adhering to all safety guidelines, and maintaining a clean and organized workspace. Harassment of any kind is not tolerated.
    ```

5.  **`mock_data/End_of_Day_Closing_Procedures.html`** (Save as HTML)
    ```html
    <!DOCTYPE html>
    <html>
    <head><title>End of Day Closing Procedures</title></head>
    <body>
        <h1>End of Day Closing Checklist</h1>
        <ul>
            <li>Clean all food preparation surfaces with approved sanitizer.</li>
            <li>Sweep and mop all kitchen floors.</li>
            <li>Ensure all perishable food items are properly stored and refrigerated below 40°F.</li>
            <li>Check and record refrigerator and freezer temperatures.</li>
            <li>Turn off all cooking equipment, including ovens, grills, and fryers.</li>
            <li>Empty all trash and recycling receptacles.</li>
            <li>Lock all doors and set the security alarm.</li>
        </ul>
        <p><strong>Food Safety Note:</strong> All food safety steps, including temperature checks and proper storage, are mandatory to comply with health regulations.</p>
    </body>
    </html>
    ```

## Step 2: Create the Knowledge Bases

Knowledge bases allow our agents to access information from the documents we just created. We will create two distinct knowledge bases using the built-in Milvus vector database provided by Orchestrate.

1.  **Recipe Knowledge Base**: This will contain all culinary recipes.
    *   **File**: `knowledge/recipe_kb.yaml`
    *   **Explanation**: This configuration defines a knowledge base named `recipe_knowledge_base`. It instructs Orchestrate to ingest the two recipe PDFs from our `mock_data` directory. It uses the default `ibm/slate-125m-english-rtrvr-v2` embedding model to convert the document text into vectors for efficient searching.

    ```yaml
    # knowledge/recipe_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: recipe_knowledge_base
    description: >
      Contains detailed information and instructions for all official company recipes, including ingredient lists, preparation steps, and cooking tips.
    documents:
      - "mock_data/Classic_Marinara_Sauce.pdf"
      - "mock_data/Perfect_Pizza_Dough.pdf"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

2.  **Policy & Procedures Knowledge Base**: This will contain all operational documents.
    *   **File**: `knowledge/policy_kb.yaml`
    *   **Explanation**: Similarly, this file defines the `policy_knowledge_base`. It ingests the policy, conduct, and procedure documents. By separating knowledge bases, we create specialized information sources, which improves the accuracy and relevance of answers from our expert agents.

    ```yaml
    # knowledge/policy_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: policy_knowledge_base
    description: >
      An authoritative source for all company policies and standard operating procedures (SOPs), including food safety, HR guidelines, and daily checklists.
    documents:
      - "mock_data/Food_Safety_Handling_Policy.docx"
      - "mock_data/Employee_Code_of_Conduct.txt"
      - "mock_data/End_of_Day_Closing_Procedures.html"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 3: Develop the Custom Python Tool

To demonstrate extensibility, we will create a simple Python tool for the `Recipe_Expert_Agent`.

*   **File**: `tools/recipe_tools.py`
*   **Business Value**: The `unit_converter_tool` provides immediate utility in a culinary setting, allowing partners to quickly convert measurements without leaving the chat interface. This showcases how Orchestrate can be extended with custom logic to solve domain-specific problems, enhancing user efficiency.
*   **Technical Implementation**: This tool is created using the `@tool` decorator from the ADK. The function signature defines the inputs (`quantity`, `from_unit`, `to_unit`), and the Google-style docstring provides a detailed description that the agent uses to understand the tool's purpose and arguments. For this demo, the conversion logic is mocked, but it can be easily replaced with a real conversion library.

```python
# tools/recipe_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="unit_converter_tool", description="Converts between common kitchen measurement units.")
def unit_converter_tool(quantity: float, from_unit: str, to_unit: str) -> str:
    """
    Converts between common kitchen measurement units like grams, ounces, cups.

    Args:
        quantity (float): The amount to convert.
        from_unit (str): The starting unit (e.g., 'cups', 'grams').
        to_unit (str): The target unit (e.g., 'ounces', 'ml').
    Returns:
        str: The converted quantity and unit as a string.
    """
    # Mock conversion logic for the demo
    # A real implementation would use a conversion library.
    if from_unit.lower() == "cups" and to_unit.lower() == "ml":
        converted_quantity = quantity * 236.588
        return f"{quantity} {from_unit} is approximately {converted_quantity:.2f} {to_unit}."
    elif from_unit.lower() == "ounces" and to_unit.lower() == "grams":
        converted_quantity = quantity * 28.35
        return f"{quantity} {from_unit} is approximately {converted_quantity:.2f} {to_unit}."
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported in this mock tool. A real tool would handle this."

```

*   **File**: `requirements.txt`
*   **Explanation**: This file lists any external Python libraries your tools depend on. While our simple tool has no external dependencies, it's a best practice to include this file.

```text
# requirements.txt
# No external dependencies for this simple tool.
# If using libraries like 'requests', add them here.
```

## Step 4: Define the Collaborator Agents

Now we define the specialist agents that will perform the core work.

1.  **Recipe Expert Agent**
    *   **File**: `agents/recipe_expert_agent.yaml`
    *   **Explanation**: This agent is an expert on all things culinary. Its description clearly states its capabilities. Its instructions guide it to primarily use its `recipe_knowledge_base` to answer questions. Crucially, it is also equipped with the `unit_converter_tool`, expanding its capabilities beyond simple information retrieval.

    ```yaml
    # agents/recipe_expert_agent.yaml
    spec_version: v1
    kind: native
    name: Recipe_Expert_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent with deep knowledge of all company recipes. It can retrieve specific ingredient lists, preparation steps, and cooking instructions. It can also convert kitchen measurements.
    instructions: >
      You are an expert culinary assistant. Your primary goal is to answer questions about recipes using the information in your knowledge base. If asked to convert units, use the unit_converter_tool. Be precise and clear in your responses.
    tools:
      - unit_converter_tool
    knowledge_base:
      - recipe_knowledge_base
    ```

2.  **Policy & Procedures Agent**
    *   **File**: `agents/policy_procedures_agent.yaml`
    *   **Explanation**: This agent is the authority on company operations. Its description highlights its expertise in policies, safety, and procedures. Its instructions direct it to rely on the `policy_knowledge_base` to provide accurate and compliant answers. It has no custom tools, as its function is purely RAG-based.

    ```yaml
    # agents/policy_procedures_agent.yaml
    spec_version: v1
    kind: native
    name: Policy_Procedures_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert on all company policies and operational procedures, including food safety, HR guidelines, and end-of-day closing tasks. It provides official, documented answers.
    instructions: >
      You are a policy and procedures expert. You must answer user questions strictly based on the content within your knowledge base. Do not invent information. If the answer is not in the documents, state that you cannot find the information.
    knowledge_base:
      - policy_knowledge_base
    ```

## Step 5: Define the Supervisor Agent

The supervisor agent is the orchestrator of the entire system. It doesn't answer questions directly but routes them to the correct specialist.

*   **File**: `agents/supervisor_agent.yaml`
*   **Explanation**: This is the top-level agent that the user interacts with. Its description clearly defines its role as an onboarding assistant. The `collaborators` section lists the two specialist agents it can delegate tasks to. The `instructions` are the most critical part: they provide the reasoning logic for routing. By explicitly stating "If it is about a recipe, use the Recipe_Expert_Agent" and "If it is about policies... use the Policy_Procedures_Agent", we are programming its decision-making process.

```yaml
# agents/supervisor_agent.yaml
spec_version: v1
kind: native
name: Onboarding_Supervisor_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A helpful onboarding assistant for new culinary partners. It can answer questions about recipes, company policies, and standard procedures by consulting with expert agents.
instructions: >
  Your goal is to understand the user's question and delegate it to the correct expert.
  - If the user asks about a specific recipe, ingredients, or cooking steps, use the Recipe_Expert_Agent.
  - If the user asks about company policies, safety rules, HR guidelines, or operational procedures like closing tasks, use the Policy_Procedures_Agent.
  - You do not have tools or knowledge yourself. You must always use one of your collaborator agents to answer the user.
collaborators:
  - Recipe_Expert_Agent
  - Policy_Procedures_Agent
```

## Step 6: Deployment and Execution

With all configuration files in place, we will use the `orchestrate` CLI to deploy the entire system. The order of operations is important to ensure dependencies are met (e.g., agents cannot be imported before their tools and knowledge bases exist).

**Action:** Run the following commands from the root of your `culinary_demo/` directory.

1.  **Import Knowledge Bases**:
    *   **Command**:
        ```bash
        orchestrate knowledge-bases import -f knowledge/recipe_kb.yaml
        orchestrate knowledge-bases import -f knowledge/policy_kb.yaml
        ```
    *   **Explanation**: These commands register the knowledge bases with Orchestrate and begin the process of ingesting and indexing the associated documents. You can check the status with `orchestrate knowledge-bases status --name <kb_name>`.

2.  **Import Custom Tool**:
    *   **Command**:
        ```bash
        orchestrate tools import -f tools/recipe_tools.py
        ```
    *   **Explanation**: This command parses the Python file, identifies the function with the `@tool` decorator, and registers it as an available tool within your Orchestrate environment.

3.  **Import Collaborator Agents**:
    *   **Command**:
        ```bash
        orchestrate agents import -f agents/recipe_expert_agent.yaml
        orchestrate agents import -f agents/policy_procedures_agent.yaml
        ```
    *   **Explanation**: These commands import the specialist agents. Orchestrate will validate that their declared knowledge bases and tools (`recipe_knowledge_base`, `unit_converter_tool`, etc.) exist in the environment.

4.  **Import the Supervisor Agent**:
    *   **Command**:
        ```bash
        orchestrate agents import -f agents/supervisor_agent.yaml
        ```
    *   **Explanation**: This final agent import registers the main user-facing agent. Orchestrate validates that its declared collaborators (`Recipe_Expert_Agent`, `Policy_Procedures_Agent`) are available.

## Step 7: Verification and Demo Scenarios

Now, you can interact with your AI assistant and run the demo scenarios.

**Action:** Start the interactive chat interface.

```bash
orchestrate chat start
```

This will launch a chat session. Select the `Onboarding_Supervisor_Agent` to begin. Now, test the specific scenarios outlined in the demo concept.

*   **Scenario 1: Specific Recipe Inquiry**
    *   **User Input**: `How much fresh basil is needed for the classic marinara sauce?`
    *   **Expected Behavior**: The `Onboarding_Supervisor_Agent` will recognize the query is about a recipe and delegate it to the `Recipe_Expert_Agent`. The `Recipe_Expert_Agent` will search the `recipe_knowledge_base`, find the `Classic_Marinara_Sauce.pdf`, extract the relevant information, and respond with "1 large sprig fresh basil."

*   **Scenario 2: Policy & Safety Question**
    *   **User Input**: `What is the required internal temperature for cooked chicken according to our food safety policy?`
    *   **Expected Behavior**: The `Onboarding_Supervisor_Agent` will identify this as a policy question and route it to the `Policy_Procedures_Agent`. This agent will query the `policy_knowledge_base`, find the answer in `Food_Safety_Handling_Policy.docx`, and respond with "165°F (74°C)."

*   **Scenario 3: Complex Procedural Query**
    *   **User Input**: `I'm closing up for the night, what are the food safety steps I need to follow?`
    *   **Expected Behavior**: The `Onboarding_Supervisor_Agent` will route this to the `Policy_Procedures_Agent`. The agent will perform a more complex query against its knowledge base, synthesizing information from both `End_of_Day_Closing_Procedures.html` and `Food_Safety_Handling_Policy.docx` to provide a comprehensive checklist, such as ensuring perishable foods are stored below 40°F and checking refrigerator temperatures.

## Troubleshooting

*   **Agent Routing Failure**: If the supervisor agent picks the wrong collaborator, review its `instructions` in `supervisor_agent.yaml`. Make them more specific. Also, ensure the `description` of each collaborator agent accurately reflects its capabilities, as the supervisor uses this for routing decisions.
*   **Knowledge Base Retrieval Failure**: If an agent responds that it cannot find information that you know is in the documents, first check the knowledge base status with `orchestrate knowledge-bases status --name <knowledge_base_name>`. Ensure it is `Ready`. If it is, the issue may be with the query itself or the document's content. Ensure the mock documents are saved correctly and their paths in the YAML files are accurate relative to where you are running the `orchestrate` commands.
*   **Tool Not Found**: If an agent fails because it can't find a tool, ensure you have run the `orchestrate tools import` command successfully *before* importing the agent that uses it. You can list all available tools with `orchestrate tools list`.

## Best Practices

*   **Descriptive Naming and Descriptions**: Use clear, unique names for agents, tools, and knowledge bases. The descriptions are not just for users; they are critical context for the LLMs that power the agents. A well-written description significantly improves routing accuracy.
*   **Specific Instructions**: Be explicit in your agent instructions. The "Reasoning" pattern (`Use the {{TOOL_NAME}} for {{SCENARIO}}`) is powerful. The more specific your instructions, the more predictable and reliable the agent's behavior will be.
*   **Modular Design**: The supervisor-collaborator pattern is highly effective. Keep agents specialized. An agent should either be a router (supervisor) or an expert with its own tools/knowledge (collaborator), but rarely both. This separation of concerns makes the system easier to build, debug, and scale.
*   **Iterative Development**: Start with a simple agent and add complexity gradually. Test each component (knowledge base, tool, agent) individually before combining them. Use the `orchestrate chat` interface to test and refine agent instructions iteratively.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
