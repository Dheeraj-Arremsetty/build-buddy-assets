# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-10-01 13:21:56
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Store Operations Co-Pilot

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Store Operations Co-Pilot" for the client. This solution is designed to address the core challenges of operational inefficiency and inconsistency at the store level by creating an intelligent assistant that streamlines daily tasks. The Co-Pilot leverages a multi-agent architecture within IBM watsonx Orchestrate, combining information retrieval from a curated knowledge base with actionable task automation.

The final demo will showcase a supervisor agent (`Store_Operations_CoPilot`) that intelligently routes employee requests to specialized collaborator agents for handling HR policy questions (`HR_Policy_Agent`) and logging equipment maintenance tickets (`Maintenance_Request_Agent`). This plan directly implements the client's proposed architecture, demonstrating tangible business value by increasing employee efficiency, ensuring procedural consistency, accelerating new-hire onboarding, and enabling proactive operational management.

## 2. Prerequisites

Before beginning the implementation, ensure your development environment is set up with the following components. This setup is crucial for using the IBM watsonx Orchestrate Agent Development Kit (ADK) to build, import, and test the agents.

*   **Python 3.10 or higher**: The ADK is a Python library. Ensure you have a compatible version of Python installed.
*   **IBM watsonx Orchestrate ADK**: The core toolkit for building agents and tools. Install it using pip:
    ```bash
    pip install "ibm-watsonx-orchestrate[all]"
    ```
*   **watsonx Orchestrate Environment**: You must have access to an IBM watsonx Orchestrate instance and have configured your local environment to connect to it. This is typically done via the `orchestrate login` command.
*   **Mock Data Files**: The three synthetic documents specified in the client context must be created and available locally. The content for these files is provided in Step 4.1.

## 3. Project Structure Setup

To ensure a clean and manageable project, create the following directory structure. This organization separates the different components of the Orchestrate solution, making it easier to build and deploy.

```
store-operations-copilot/
├── agents/
│   ├── store_operations_copilot.yaml
│   ├── maintenance_agent.yaml
│   └── hr_agent.yaml
├── tools/
│   └── maintenance_tools.py
├── mock_data/
│   ├── Mastrena_II_Manual.pdf
│   ├── Q3_Promotional_Playbook.docx
│   └── Employee_Handbook_2024.pdf
├── knowledge_base/
│   └── store_operations_kb.yaml
└── requirements.txt
```

## 4. Step-by-Step Implementation

This section details the creation of every asset required for the demo, from the knowledge base and custom tools to the full agent architecture.

### Step 4.1: Create Mock Data and Knowledge Base

The knowledge base is the foundation for the Co-Pilot's information retrieval capabilities. We will populate it with curated documents that simulate the client's internal operational guides.

**Business Value**: This component directly addresses the need for quick and consistent information access, reducing the time employees spend searching for procedures and allowing them to focus on customer service.

1.  **Create Mock Data Files**: In the `mock_data/` directory, create the following three files. For PDF and DOCX, you can use any standard editor to create a document with the text below and save it in the correct format.

    *   **`Mastrena_II_Manual.pdf`**:
        > **Mastrena II Espresso Machine - Operations Manual**
        >
        > **Section 1: Daily Cleaning Procedure**
        > 1.  Turn off the machine using the main power switch.
        > 2.  Remove the grounds drawer and empty it.
        > 3.  Wipe down the exterior surfaces with a damp cloth.
        > 4.  Run the automated cleaning cycle using one (1) cleaning tablet.
        > 5.  Rinse the portafilter and steam wand thoroughly.
        >
        > **Section 2: Troubleshooting Common Error Codes**
        > -   **Error E-15**: Water flow issue. Check if the main water line is open.
        > -   **Error E-21**: Grinder malfunction. Clear any bean obstructions from the hopper. If the problem persists, log a maintenance ticket.
        > -   **Error E-30**: Overheating. Turn the machine off for 30 minutes to cool down.

    *   **`Q3_Promotional_Playbook.docx`**:
        > **Q3 Promotion: Summer Sunrise Refresher**
        >
        > **Recipe:**
        > -   Venti Cup: 4 pumps Sunrise Syrup, Pineapple Base to the first line, Coconut Milk to the third line, ice.
        >
        > **Marketing Guidelines:**
        > -   Promote with the tagline "Taste the sunrise!"
        > -   Offer a 10% discount when paired with a pastry.
        >
        > **Customer FAQs:**
        > -   Is it dairy-free? Yes, it is made with coconut milk.
        > -   Can I get it without syrup? Yes, but it will alter the intended flavor profile.

    *   **`Employee_Handbook_2024.pdf`**:
        > **Employee Handbook - 2024 Edition**
        >
        > **Section 4.A: Dress Code**
        > -   Employees must wear a company-provided apron and hat.
        > -   Black or khaki pants are required. No jeans or shorts.
        > -   Shoes must be non-slip and closed-toe.
        >
        > **Section 7.B: Handling Customer Complaints**
        > When a customer complains about a mobile order, follow the 4-step "LISTEN" method:
        > 1.  **Listen**: Allow the customer to explain the issue without interruption.
        > 2.  **Inquire**: Ask clarifying questions to understand the problem fully.
        > 3.  **Sympathize**: Acknowledge their frustration with a phrase like, "I understand that must be frustrating."
        > 4.  **Take Action**: Offer a solution, such as remaking the order or providing a recovery coupon.

2.  **Create Knowledge Base Configuration File**: In the `knowledge_base/` directory, create `store_operations_kb.yaml`. This file tells Orchestrate where to find the documents and how to process them.

    ```yaml
    # knowledge_base/store_operations_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: store_operations_kb
    description: >
       Contains internal documents for store operations, including equipment manuals (Mastrena II),
       seasonal promotional playbooks, and the official employee handbook covering policies like
       dress code and customer complaint procedures.
    documents:
       - "mock_data/Mastrena_II_Manual.pdf"
       - "mock_data/Q3_Promotional_Playbook.docx"
       - "mock_data/Employee_Handbook_2024.pdf"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 4.2: Develop the Custom Python Tool

This tool transforms the Co-Pilot from a passive information source into an active operational assistant. It demonstrates Orchestrate's ability to execute tasks and integrate with external systems.

**Business Value**: The `log_maintenance_ticket` tool provides a direct path from problem identification to resolution. It empowers employees to take immediate action on equipment failures, minimizing downtime, reducing revenue loss, and ensuring a consistent customer experience. This showcases a proactive operational model driven by AI.

1.  **Create the Python Tool File**: In the `tools/` directory, create `maintenance_tools.py`. This script defines the function that will log a maintenance ticket. The function uses the `@tool` decorator to make it discoverable by Orchestrate and includes a detailed docstring that the agent uses to understand its purpose, inputs, and outputs.

    ```python
    # tools/maintenance_tools.py
    import random
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="log_maintenance_ticket", description="Logs a new maintenance ticket in the service system for broken equipment.", permission=ToolPermission.ADMIN)
    def log_maintenance_ticket(equipment_name: str, error_code: str, store_id: str = "SBUX-042") -> str:
        """
        Logs a new maintenance ticket in the service system for broken equipment. This tool should be used
        when troubleshooting steps have failed and a technician is required.

        Args:
            equipment_name (str): The name of the equipment that is broken (e.g., "Mastrena II").
            error_code (str): The error code displayed on the machine, if any.
            store_id (str): The unique identifier for the store location. Defaults to "SBUX-042".

        Returns:
            str: A confirmation message with the newly created ticket number.
        """
        # In a real-world scenario, this would make an API call to a system like ServiceNow or Jira.
        # For this demo, we simulate the API call and return a mock ticket number to demonstrate functionality.
        try:
            print(f"Simulating API call to log ticket for '{equipment_name}' with error '{error_code}' at store '{store_id}'...")
            ticket_number = f"INC{random.randint(700, 999)}89"
            confirmation_message = f"Successfully logged maintenance ticket #{ticket_number}."
            return confirmation_message
        except Exception as e:
            # Basic error handling for a real-world scenario
            return f"Failed to log maintenance ticket. Error: {str(e)}"

    ```

### Step 4.3: Define the Collaborator Agents

Collaborator agents are specialists. By creating them, we demonstrate how to build a scalable and maintainable multi-agent system where each agent has a clear, defined role.

1.  **Create the `Maintenance_Request_Agent`**: This agent is purely action-oriented. Its sole purpose is to use the `log_maintenance_ticket` tool.

    **Business Value**: This demonstrates role specialization. By isolating the maintenance function, you can manage its logic, tools, and connections independently without affecting other parts of the Co-Pilot system.

    ```yaml
    # agents/maintenance_agent.yaml
    spec_version: v1
    kind: native
    name: Maintenance_Request_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialized agent for handling equipment maintenance tasks. Use this agent to log a new
      service or maintenance ticket when a piece of equipment, like an espresso machine, is broken
      and requires a technician. It uses the log_maintenance_ticket tool.
    instructions: >
      Your only purpose is to create maintenance tickets using the log_maintenance_ticket tool.
      When asked to log a ticket, confirm the equipment name and error code with the user.
      Once you have the necessary information, execute the tool and provide the confirmation
      message back to the user. Do not answer any other types of questions.
    tools:
      - log_maintenance_ticket
    ```

2.  **Create the `HR_Policy_Agent`**: This agent is a knowledge specialist with a focused scope. It uses the same knowledge base as the supervisor but is instructed to only answer questions related to HR.

    **Business Value**: This pattern shows how a single source of truth (the knowledge base) can be securely and effectively leveraged by multiple specialized agents. It prevents "knowledge bleed" and ensures that the HR agent only provides answers from the official employee handbook.

    ```yaml
    # agents/hr_agent.yaml
    spec_version: v1
    kind: native
    name: HR_Policy_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialized agent that answers questions about human resources (HR) policies using the
      official Employee Handbook. Use this agent for queries about dress code, time-off policies,
      and official procedures for handling customer complaints.
    instructions: >
      You are an HR Policy expert. Your purpose is to answer questions using ONLY the information
      found in your knowledge base, which contains the Employee Handbook.
      If a question is about something other than HR policies (e.g., equipment, promotions),
      state that you cannot answer and that the query is outside your scope.
    knowledge_base:
      - store_operations_kb
    ```

### Step 4.4: Define the Supervisor Agent

The `Store_Operations_CoPilot` is the "brain" of the operation. It's the primary interface for the user and is responsible for understanding intent and delegating tasks to the correct collaborator.

**Business Value**: The supervisor agent pattern is the key to creating a scalable, intelligent, and user-friendly AI assistant. It provides a single point of interaction for the user while orchestrating a powerful team of specialized agents in the background, showcasing the advanced reasoning and routing capabilities of watsonx Orchestrate.

```yaml
# agents/store_operations_copilot.yaml
spec_version: v1
kind: native
name: Store_Operations_CoPilot
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A helpful AI Co-Pilot for store employees. It answers questions about equipment, promotions, and HR
    policies by searching internal documents. It can delegate tasks like creating maintenance tickets
    for broken equipment or answering specific HR questions to specialized agents.
instructions: >
    You are the Store Operations Co-Pilot, an AI assistant for store employees. Your primary goal is to
    provide accurate information and delegate tasks effectively. Follow these reasoning steps:

    1.  **Assess User Intent**: First, determine what the user is trying to do. Are they asking for information, or do they need to perform an action?

    2.  **Information Retrieval**: For general questions about procedures, promotions (like the "Summer Sunrise Refresher"), or initial equipment troubleshooting, use your 'store_operations_kb' knowledge base to find the answer.

    3.  **Task Delegation - Maintenance**: If a user wants to report broken equipment, log a service request, or mentions an error code after trying to troubleshoot, you MUST use the 'Maintenance_Request_Agent'. Do not try to log the ticket yourself.

    4.  **Task Delegation - HR**: For specific questions about the employee handbook, dress code, time off, or official procedures for customer complaints, you MUST use the 'HR_Policy_Agent'.
collaborators:
  - Maintenance_Request_Agent
  - HR_Policy_Agent
knowledge_base:
  - store_operations_kb
```

### Step 4.5: Create the `requirements.txt` file

This file lists the Python dependencies required for the custom tools to function correctly.

```text
# requirements.txt
ibm-watsonx-orchestrate
requests
```

## 5. Deployment and Execution Sequence

Follow these CLI commands in precise order from the root directory (`store-operations-copilot/`) to import all assets into your watsonx Orchestrate environment and start the chat interface.

1.  **Import the Custom Tool**:
    ```bash
    orchestrate tools import -f tools/maintenance_tools.py
    ```

2.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledgebases import -f knowledge_base/store_operations_kb.yaml
    ```

3.  **Import the Collaborator Agents**:
    ```bash
    # Import Maintenance Agent
    orchestrate agents import -f agents/maintenance_agent.yaml

    # Import HR Agent
    orchestrate agents import -f agents/hr_agent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/store_operations_copilot.yaml
    ```

5.  **Start the Chat to Begin the Demo**:
    ```bash
    orchestrate chat start
    ```

## 6. Verification and Demo Scenarios

After running `orchestrate chat start`, use the following scenarios to test the Co-Pilot and verify that the entire system is working as designed.

*   **Scenario 1: Equipment Troubleshooting (Information Retrieval)**
    *   **User Prompt:** `"What are the steps to clean the Mastrena II espresso machine?"`
    *   **Expected Behavior:** The `Store_Operations_CoPilot` agent identifies this as an information request. It queries its own `store_operations_kb`, finds the relevant section in `Mastrena_II_Manual.pdf`.
    *   **Expected Output:** `"Here are the daily cleaning procedures for the Mastrena II: 1. Turn off the machine... 2. Remove the grounds drawer... 3. Wipe down the exterior... 4. Run the automated cleaning cycle... 5. Rinse the portafilter and steam wand."`

*   **Scenario 2: Customer Complaint Handling (Delegation to HR Agent)**
    *   **User Prompt:** `"What is the policy for handling a customer complaint about a mobile order?"`
    *   **Expected Behavior:** The `Store_Operations_CoPilot` recognizes this as an HR policy question based on its instructions. It delegates the query to the `HR_Policy_Agent`. The `HR_Policy_Agent` then searches the knowledge base and extracts the procedure from `Employee_Handbook_2024.pdf`.
    *   **Expected Output:** `"According to the employee handbook, you should follow the 4-step 'LISTEN' method: 1. Listen... 2. Inquire... 3. Sympathize... 4. Take Action..."`

*   **Scenario 3: Equipment Failure (Delegation and Task Automation)**
    *   **User Prompt:** `"The Mastrena II is showing error code E-21 and won't turn on. I've tried the troubleshooting steps."`
    *   **Expected Behavior:**
        1.  The `Store_Operations_CoPilot` recognizes the intent to report a problem and delegates the task to the `Maintenance_Request_Agent`.
        2.  The `Maintenance_Request_Agent` takes over, understands it needs to invoke the `log_maintenance_ticket` tool, and may ask for confirmation.
        3.  The agent might respond: `"I can log a maintenance ticket for the Mastrena II with error code E-21. Is that correct?"`
        4.  User confirms with `"Yes"`.
        5.  The tool executes, simulating the API call.
    *   **Expected Final Output:** `"I have successfully logged maintenance ticket #INC... A technician will be dispatched within 24 hours."`

## 7. Troubleshooting

If you encounter issues during deployment or testing, refer to these common problems and solutions.

*   **Issue: `Agent not found` or `Tool not found` error.**
    *   **Solution:** Ensure the `name` field in your YAML files exactly matches the names used in `collaborators` or `tools` lists. Verify that you have successfully imported all agents and tools using the CLI commands before importing the supervisor. Check for typos.

*   **Issue: Knowledge base returns no answer or an irrelevant one.**
    *   **Solution:** Double-check the file paths in `store_operations_kb.yaml` are correct relative to where you are running the `orchestrate` command. Ensure the content within your mock PDF/DOCX files is clean, searchable text (not images of text).

*   **Issue: Supervisor agent handles a request instead of delegating.**
    *   **Solution:** This is an instruction-tuning issue. Refine the `instructions` in `store_operations_copilot.yaml` to be more explicit. Use strong keywords like "You MUST use the `Maintenance_Request_Agent` for..." to guide the LLM's routing logic more effectively. The description of the collaborator agents is also critical for routing.

*   **Issue: Python tool import fails.**
    *   **Solution:** Check for syntax errors in `maintenance_tools.py`. Ensure all required libraries are listed in `requirements.txt` and installed in your Python environment. Verify the `@tool` decorator and its parameters are correctly formatted.

## 8. Best Practices and Recommendations

*   **Craft Precise Instructions and Descriptions**: The accuracy of agent routing heavily depends on the quality of the `description` and `instructions` for both the supervisor and collaborator agents. Be explicit about each agent's role and when they should be used.
*   **Embrace the Supervisor-Collaborator Pattern**: This architecture is highly scalable. For new functions (e.g., an "Inventory Agent"), you can build a new specialized collaborator and simply add it to the supervisor's `collaborators` list without redesigning the entire system.
*   **Create Atomic, Well-Documented Tools**: Each tool should perform one specific action. The docstring is not just for developers; it's the primary way the agent learns how to use the tool. A detailed docstring with clear `Args` and `Returns` is essential.
*   **Curate Your Knowledge Base**: The principle of "garbage in, garbage out" applies. Use well-structured, clean, and accurate documents in your knowledge base for the best Retrieval-Augmented Generation (RAG) performance.
*   **Iterate and Test**: Use the `orchestrate chat` interface to continuously test your agents with different prompts. If the behavior is not as expected, update the agent's instructions and re-import it. The ADK is designed for this rapid, iterative development cycle.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
