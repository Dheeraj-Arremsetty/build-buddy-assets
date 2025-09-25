# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-25 16:02:57
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy Demo

## Overview
This execution plan provides a comprehensive, step-by-step guide for building and deploying the "Barista Buddy," an AI-powered onboarding and operations assistant for your client. This solution, built on IBM watsonx Orchestrate, directly addresses the client's key challenges of accelerating new hire training and ensuring operational consistency across all locations. The "Barista Buddy" leverages a sophisticated multi-agent architecture where a central supervisor agent intelligently routes employee queries to specialized collaborator agents. This design ensures that baristas receive instant, accurate, and consistent information on drink recipes, operational procedures, and company policies, thereby reducing the training load on senior staff and improving overall service quality.

The plan details the creation of four distinct agents: the user-facing `barista_buddy` supervisor and three specialist collaborators: `recipe_master`, `operations_guru`, and `policy_pal`. We will build and connect knowledge bases from mock company documents and develop a custom Python tool for logging maintenance requests. This mirrors a real-world enterprise scenario, demonstrating the full power of watsonx Orchestrate to create robust, scalable, and valuable AI assistants.

## Prerequisites
Before beginning, ensure your development environment is properly configured.

1.  **Python:** Python 3.10 or later installed on your system.
2.  **IBM watsonx Orchestrate ADK:** The Agent Development Kit (ADK) must be installed. If not, install it using pip:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
3.  **ADK Environment:** You must have an active watsonx Orchestrate environment configured. Initialize it if you haven't already:
    ```bash
    orchestrate env init --name my-demo-env
    ```
4.  **Text Editor:** A code editor like Visual Studio Code is recommended for editing Python and YAML files.
5.  **Terminal/Command Line:** A terminal to run the `orchestrate` CLI commands.

## Step 1: Project Setup and Knowledge Base Document Creation
First, we will establish a clean project structure and create the source documents for our knowledge bases. This organization is crucial for managing the different components of our multi-agent application.

1.  **Create Project Directory:**
    ```bash
    mkdir barista-buddy-demo
    cd barista-buddy-demo
    mkdir agents tools knowledge_base_docs
    ```

2.  **Create Mock Knowledge Documents:** We will create simple text files to act as the source of truth for our specialist agents.

    *   **Recipe Document:** Create `knowledge_base_docs/recipes.txt`.
        ```text
        # Barista Recipe Guide

        ## Caramel Macchiato
        - Ingredients: 1 shot Espresso, 1 tbsp Vanilla Syrup, Steamed Milk, Caramel Drizzle.
        - Instructions:
          1. Add vanilla syrup to the bottom of the cup.
          2. Add steamed milk.
          3. Pour espresso shot over the milk.
          4. Top with caramel drizzle in a crosshatch pattern.

        ## Iced Latte
        - Ingredients: 2 shots Espresso, Milk, Ice.
        - Instructions:
          1. Fill a tall glass with ice.
          2. Pour espresso shots over the ice.
          3. Top with cold milk, leaving room to stir.
        ```

    *   **Operations Document:** Create `knowledge_base_docs/operations.txt`.
        ```text
        # Standard Operating Procedures (SOPs)

        ## Morning Opening Checklist
        1. Disarm security system.
        2. Calibrate espresso machines (run 2 blank shots).
        3. Check milk and bean stock levels.
        4. Set up pastry display case.
        5. Count cash drawer and verify float is $150.

        ## Equipment Troubleshooting: Espresso Machine
        - Issue: Leaking water from group head.
        - Action: Check for a worn-out gasket. If worn, log a maintenance request using the Barista Buddy. Do not attempt to replace it yourself.
        ```

    *   **Policy Document:** Create `knowledge_base_docs/policies.txt`.
        ```text
        # Employee Handbook Excerpt

        ## Dress Code
        - All employees must wear the company-provided apron and a black or white shirt.
        - Pants must be black or dark khaki. No rips or tears.
        - Closed-toe, non-slip shoes are mandatory.

        ## Time Off Requests
        - All requests for time off must be submitted through the HR portal at least two weeks in advance.
        - Sick leave must be reported to the shift manager at least 2 hours before the scheduled start time.
        ```

## Step 2: Create Knowledge Base Configurations
With the source documents ready, we will now define the knowledge bases in YAML. These configurations tell Orchestrate to ingest our documents into a built-in vector store, making them searchable for our agents.

1.  **Recipe Knowledge Base:** Create `knowledge_base_docs/recipe_knowledge_base.yaml`.
    ```yaml
    spec_version: v1
    kind: knowledge_base 
    name: recipe_knowledge_base
    description: >
      Contains detailed recipes and preparation instructions for all company-approved beverages. 
      Use this to answer any questions about how to make a drink.
    documents:
      - "knowledge_base_docs/recipes.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

2.  **Operations Knowledge Base:** Create `knowledge_base_docs/operations_knowledge_base.yaml`.
    ```yaml
    spec_version: v1
    kind: knowledge_base 
    name: operations_knowledge_base
    description: >
      Contains standard operating procedures (SOPs), including daily checklists, 
      equipment troubleshooting guides, and maintenance protocols.
    documents:
      - "knowledge_base_docs/operations.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

3.  **Policy Knowledge Base:** Create `knowledge_base_docs/policy_knowledge_base.yaml`.
    ```yaml
    spec_version: v1
    kind: knowledge_base 
    name: policy_knowledge_base
    description: >
      Contains information from the employee handbook, covering company policies, 
      HR procedures, dress code, and time off requests.
    documents:
      - "knowledge_base_docs/policies.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 3: Create the Custom Tool
The `Operations Guru` agent needs the ability to perform an action: logging a maintenance request. We'll create this as a Python tool.

*   **Business Value:** This tool demonstrates how Orchestrate can move beyond just answering questions (RAG) to taking action and integrating with other business systems (like a ticketing or maintenance system). It empowers employees to resolve issues directly from the chat interface, improving operational uptime and efficiency.
*   **Technical Implementation:** The tool uses the `@tool` decorator to be recognizable by the ADK. It simulates an API call to a maintenance system, generating a realistic synthetic ticket with a unique ID, timestamp, and status. It returns a simple JSON object, which is easily interpreted by the agent and presented to the user.

1.  Create the tool file at `tools/maintenance_tool.py`.
    ```python
    # tools/maintenance_tool.py
    import json
    import random
    from datetime import datetime
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="log_maintenance_request", permission=ToolPermission.ADMIN)
    def log_maintenance_request(equipment_name: str, issue_description: str) -> str:
        """
        Logs a maintenance request for a piece of equipment and returns a ticket number.

        Args:
            equipment_name (str): The name of the equipment that needs maintenance (e.g., 'Espresso Machine Model X').
            issue_description (str): A detailed description of the problem.

        Returns:
            str: A JSON string

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
