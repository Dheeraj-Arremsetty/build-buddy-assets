# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-22 15:12:47
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Unified Employee Assistant

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Unified Employee Assistant" for the client. The solution directly addresses the client's need for a single, conversational entry point for employees, reducing friction and improving efficiency. We will construct a multi-agent system featuring a supervisor agent (`Enterprise_Assistant`) that intelligently handles user requests. This agent will use a knowledge base to answer company policy questions and delegate specialized IT support tasks to a collaborator agent (`IT_Support_Agent`), which integrates with a mock ServiceNow system. This plan leverages the full capabilities of the IBM watsonx Orchestrate Agent Development Kit (ADK), demonstrating a scalable and powerful architecture that delivers immediate business value by unifying support channels and automating common tasks.

## Prerequisites
Before beginning, ensure your environment is correctly configured. These prerequisites are essential for the successful creation, deployment, and testing of the agents and tools outlined in this plan.

*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed. This is the core command-line interface (CLI) and library used to build and manage all components. Refer to the official documentation for installation instructions.
*   **Active Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized and configured. This is the target platform where the agents, tools, and knowledge base will be deployed. Use `orchestrate environment list` to see your environments and `orchestrate login` to authenticate.
*   **Python 3.8+:** The ADK and the custom Python tools are built using Python. Ensure you have a compatible version installed and available in your system's PATH.
*   **Project Directory:** A dedicated folder to organize all configuration files, tools, and knowledge base documents. This ensures a clean and manageable project structure.
*   **Text Editor/IDE:** A code editor such as Visual Studio Code is recommended for creating and editing the YAML configuration and Python tool files.

## Step 1: Project Setup and Mock Data Creation
First, we will establish a structured directory for our project. This organization is crucial for managing the different components of our solution. We will also create the mock documents that will populate our knowledge base.

1.  **Create the Directory Structure:**
    Open your terminal and execute the following commands to create the necessary folders.

    ```bash
    # Create the main project folder
    mkdir unified_assistant_demo
    cd unified_assistant_demo

    # Create subdirectories for each component
    mkdir agents
    mkdir tools
    mkdir knowledge_base
    mkdir knowledge_base/mock_docs
    ```

2.  **Create Mock Knowledge Base Documents:**
    These files simulate real company documents. The `Enterprise_Assistant` will use them to answer employee questions.

    *   Create a file named `knowledge_base/mock_docs/Work_From_Home_Guidelines.txt` and add the following content:

        ```text
        Work From Home (WFH) Policy

        All employees are eligible for hybrid work arrangements, subject to manager approval. Employees are expected to maintain a dedicated, safe, and distraction-free workspace. The company will provide necessary equipment, including a laptop and monitor. For IT support related to WFH equipment, please open a ticket with the IT help desk. All standard company policies, including the IT Security Policy, apply to the remote work environment.
        ```

    *   Create a file named `knowledge_base/mock_docs/IT_Security_Policy.pdf`. For this demo, this can be a blank or simple one-page PDF document. The content inside is less important than the system's ability to ingest and reference the file.
    *   Create a file named `knowledge_base/mock_docs/Employee_Handbook.pdf`. Similarly, this can be a simple, placeholder PDF document.

## Step 2: Create the Knowledge Base
This knowledge base will be ingested into the built-in Milvus vector database provided by watsonx Orchestrate. It allows the `Enterprise_Assistant` to perform Retrieval-Augmented Generation (RAG) to answer policy questions accurately.

1.  **Create the Knowledge Base Configuration File:**
    Create a file named `knowledge_base/company_policies_kb.yaml`.

2.  **Add the following YAML configuration:**
    This file defines the knowledge base, points to our mock documents, and specifies the embedding model to use for vectorization.

    ```yaml
    # knowledge_base/company_policies_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: company_policies_kb
    description: >
      Contains official company documents including the employee handbook, IT security policies, and remote work guidelines. Use this to answer questions about company policies and procedures.
    documents:
      - "./knowledge_base/mock_docs/Employee_Handbook.pdf"
      - "./knowledge_base/mock_docs/IT_Security_Policy.pdf"
      - "./knowledge_base/mock_docs/Work_From_Home_Guidelines.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 3: Develop the IT Support Tools
Here, we will create the Python tools that the `IT_Support_Agent` will use to interact with the mock ServiceNow system. All three tools will be in a single Python file for simplicity. These tools generate realistic synthetic data to simulate a live enterprise system.

1.  **Create the Python Tool File:**
    Create a file named `tools/it_support_tools.py`.

2.  **Add the following Python code:**
    This file contains the three tools specified in the demo concept. Each tool uses the `@tool` decorator and has a detailed docstring, which is critical for the agent's ability to understand and use it correctly.

    ```python
    # tools/it_support_tools.py
    import random
    import datetime
    from typing import List, Dict, Any

    from ibm_watsonx_orchestrate.agent_builder.tools import tool

    # --- Mock Database ---
    # A simple in-memory list to simulate a ServiceNow incident database.
    MOCK_DB = [
        {
            "incident_id": "INC001001",
            "status": "In Progress",
            "short_description": "Email client not syncing on mobile device.",
            "opened_by": "Jane Doe",
            "opened_at": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
        },
        {
            "incident_id": "INC001002",
            "status": "On Hold",
            "short_description": "Request for new software license (Adobe Photoshop).",
            "opened_by": "Jane Doe",
            "opened_at": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat()
        }
    ]

    @tool
    def create_service_now_incident(short_description: str) -> str:
        """
        Creates a new IT support incident in ServiceNow for the current user. Use this when an employee reports a new issue that requires IT intervention.

        Args:
            short_description (str): A brief, one-sentence summary of the employee's IT issue.

        Returns:
            str: A confirmation message containing the incident number of the newly created ticket.
        """
        ticket_id = f"INC{random.randint(1003, 9999)}"
        new_incident = {
            "incident_id": ticket_id,
            "status": "New",
            "short_description": short_description,
            "opened_by": "Jane Doe", # Hardcoded for demo purposes
            "opened_at": datetime.datetime.now().isoformat()
        }
        MOCK_DB.append(new_incident)
        print(f"Mock DB updated: Creating ticket {ticket_id} for: {short_description}")
        return f"I have successfully created incident ticket {ticket_id} for you."

    @tool
    def get_incident_status_by_number(incident_id: str) -> Dict[str, Any]:
        """
        Retrieves the current status and details of a specific IT support incident from ServiceNow using its unique incident number.

        Args:
            incident_id (str): The incident number to query (e.g., "INC001001").

        Returns:
            dict: A dictionary containing the incident's details, including status, description, and open date, or an error message if not found.
        """
        for incident in MOCK_DB:
            if incident["incident_id"] == incident_id:
                return incident
        return {"error": f"Incident {incident_id} not found."}

    @tool
    def list_my_open_incidents() -> List[Dict[str, Any]]:
        """
        Lists all open IT support incidents currently assigned to the user 'Jane Doe'. Use this when the user asks for a list of their tickets.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents an open incident. Returns an empty list if no open incidents are found.
        """
        # In a real scenario, this would use the authenticated user's ID.
        # For this demo, we are hardcoding the user as 'Jane Doe'.
        user_incidents = [
            incident for incident in MOCK_DB if incident["opened_by"] == "Jane Doe"
        ]
        return user_incidents
    ```

## Step 4: Create Agent Definitions (YAML)
Now we define our two agents using YAML configuration files. The separation of concerns between the collaborator and supervisor is key to this architecture.

1.  **Create the Collaborator Agent (`IT_Support_Agent`):**
    This agent is a specialist. Its description is crucial because the `Enterprise_Assistant` will use it to decide when to delegate tasks.
    *   Create a file named `agents/it_support_agent.yaml`.
    *   Add the following configuration:

    ```yaml
    # agents/it_support_agent.yaml
    spec_version: v1
    kind: native
    name: IT_Support_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialized agent for handling IT support tasks. Use this agent to create new IT incidents in ServiceNow, check the status of existing incidents by number, or list all of a user's open incidents. This agent directly interacts with the IT ticketing system.
    instructions: >
      You are an expert IT Support assistant. Your purpose is to manage ServiceNow incidents.
      - When asked to create a ticket, use the `create_service_now_incident` tool.
      - When asked for the status of a specific ticket number, use the `get_incident_status_by_number` tool.
      - When asked for a list of tickets, use the `list_my_open_incidents` tool.
      - Respond clearly and concisely with the information returned by the tools. Format lists of tickets as a markdown table for readability.
    tools:
      - create_service_now_incident
      - get_incident_status_by_number
      - list_my_open_incidents
    ```

2.  **Create the Supervisor Agent (`Enterprise_Assistant`):**
    This is the primary, user-facing agent. Its instructions are written to guide its reasoning process—first check the knowledge base, and if that's not a match and the intent is IT-related, delegate to the `IT_Support_Agent`.
    *   Create a file named `agents/enterprise_assistant.yaml`.
    *   Add the following configuration:

    ```yaml
    # agents/enterprise_assistant.yaml
    spec_version: v1
    kind: native
    name: Enterprise_Assistant
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A unified assistant for all employee needs. Answers general questions about company policies from its knowledge base and can delegate tasks to specialized agents like IT Support. This is the primary agent for employees to interact with.
    instructions: >
      You are the Enterprise Assistant, a helpful and friendly resource for all employees. Your primary role is to understand the employee's request and take the most appropriate action.
      
      REASONING:
      1. First, analyze the user's query. Determine if they are asking a general question about company policy, rules, or guidelines (e.g., "what is the policy on...", "how do I..."). If so, use your knowledge base to find the answer.
      2. If the user is reporting an IT problem (e.g., "my VPN is broken", "I can't connect to email"), needs to create an IT ticket, or is asking about the status of an existing IT ticket, you MUST delegate the task to the `IT_Support_Agent`. Do not try to answer IT questions yourself.
      3. Greet the user and handle conversational pleasantries, but always follow the reasoning steps above to fulfill their request.
    collaborators:
      - IT_Support_Agent
    knowledge_base:
      - company_policies_kb
    ```

## Step 5: Deploy the Solution using the ADK CLI
With all the artifacts created, we will now use the `orchestrate` CLI to import them into the watsonx Orchestrate environment. The order of operations is important—we must import dependencies (knowledge bases, tools) before the components that use them (agents).

Execute these commands from the root of your `unified_assistant_demo` directory.

1.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f ./knowledge_base/company_policies_kb.yaml
    ```
    *You can check the ingestion status with `orchestrate knowledge-bases status --name company_policies_kb`.*

2.  **Import the Python Tools:**
    ```bash
    orchestrate tools import -k python -f ./tools/it_support_tools.py
    ```

3.  **Import the Collaborator Agent:**
    We import the collaborator first, as the supervisor depends on it.
    ```bash
    orchestrate agents import -f ./agents/it_support_agent.yaml
    ```

4.  **Import the Supervisor Agent:**
    Finally, import the main, user-facing agent.
    ```bash
    orchestrate agents import -f ./agents/enterprise_assistant.yaml
    ```

## Step 6: Verification and Demo Execution
Now, let's test the complete solution by interacting with the `Enterprise_Assistant`. We will walk through the exact demo scenarios outlined in the client concept.

1.  **Start the Chat:**
    Launch the interactive chat CLI, specifying the `Enterprise_Assistant` as our entry point.
    ```bash
    orchestrate chat start --agent Enterprise_Assistant
    ```

2.  **Execute Demo Scenarios:**
    Type the following prompts into the chat interface and observe the agent's behavior.

    *   **Scenario 1: Knowledge Base Query**
        *   **User Prompt:** `What is the company policy on using personal devices for work?`
        *   **Expected Behavior:** The `Enterprise_Assistant` should identify this as a policy question. It will query the `company_policies_kb`, find relevant information in the mock `IT_Security_Policy.pdf` or other documents, and provide a summarized answer based on that content, citing the source document.

    *   **Scenario 2: Task Delegation and Tool Execution**
        *   **User Prompt:** `My VPN connection keeps dropping. Can you open an IT ticket for me?`
        *   **Expected Behavior:** The `Enterprise_Assistant`'s instructions will cause it to recognize this as an IT issue. It will delegate the request to the `IT_Support_Agent`. The `IT_Support_Agent` will then invoke its `create_service_now_incident` tool. The tool will return a mock ticket number (e.g., "INC001234"), and the agent will relay this confirmation back to you.

    *   **Scenario 3: Follow-up Query and State Awareness**
        *   **User Prompt:** `Can you check the status of my ticket INC001001?`
        *   **Expected Behavior:** The request is again routed to the `IT_Support_Agent`. It will use the `get_incident_status_by_number` tool, passing "INC001001" as the argument. The tool will look up the incident in its mock database and return the details. The agent will then format this information conversationally, stating that the status is "In Progress".

    *   **Scenario 4: Listing Incidents**
        *   **User Prompt:** `Show me all of my open tickets.`
        *   **Expected Behavior:** This request will be delegated to the `IT_Support_Agent`, which will call the `list_my_open_incidents` tool. The tool returns a list of all incidents for "Jane Doe", and the agent will present this list to you, likely in a markdown table as instructed.

## Troubleshooting
If you encounter issues, here are some common problems and their solutions:

*   **Issue: Agent does not delegate to `IT_Support_Agent`.**
    *   **Solution:** The most likely cause is the `description` of the collaborator or the `instructions` of the supervisor. Ensure the `IT_Support_Agent`'s description clearly states its purpose (handling IT tickets). Verify the `Enterprise_Assistant`'s instructions explicitly tell it to delegate IT-related queries. Re-import the agents after making changes.

*   **Issue: "Tool not found" error.**
    *   **Solution:** Confirm that you successfully ran `orchestrate tools import -f ./tools/it_support_tools.py`. Check for typos in the tool names listed in the `it_support_agent.yaml` file. The names must match the Python function names exactly.

*   **Issue: Knowledge base query returns "I don't know".**
    *   **Solution:** Run `orchestrate knowledge-bases status --name company_policies_kb` to check if the `Ready` status is `True`. If not, ingestion may have failed. Also, verify that the file paths in `company_policies_kb.yaml` are correct relative to where you are running the command.

*   **Issue: CLI import command fails.**
    *   **Solution:** Check for YAML syntax errors. Even a small indentation error can cause a failure. Also, ensure you are in the `unified_assistant_demo` root directory when running the `orchestrate` commands so that the relative file paths are correct.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
