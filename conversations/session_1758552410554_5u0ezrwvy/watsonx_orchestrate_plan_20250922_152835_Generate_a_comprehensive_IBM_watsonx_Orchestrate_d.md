# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-22 15:28:35
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Unified Enterprise Assistant

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Unified Enterprise Assistant" for the client. The solution directly addresses the client's strategic vision for a single, conversational interface to streamline employee support. By implementing a multi-agent architecture using IBM watsonx Orchestrate, this demo will showcase how a supervisor agent can intelligently answer employee queries using a Retrieval-Augmented Generation (RAG) pattern on an internal knowledge base, while seamlessly delegating complex, domain-specific tasks to a specialized collaborator agent. This approach demonstrates significant business value by increasing employee productivity, reducing L1 support costs, and dramatically improving the overall employee experience through efficient, AI-powered automation. This plan has been refined based on expert feedback to ensure technical accuracy and adherence to the latest IBM best practices.

## Prerequisites
Before beginning, ensure your development environment is properly configured. This is essential for the successful creation and deployment of the watsonx Orchestrate assets.

1.  **Python Environment**: An installation of Python 3.9 or higher is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured with the ADK. This can be a local Developer Edition or a cloud-based SaaS environment. Ensure you have logged in via the CLI.
4.  **Project Directory**: Create a dedicated project folder to organize all the files for this demo. We recommend the following structure. All commands in this plan should be run from the root of this directory.
    ```
    /unified-enterprise-assistant/
    |-- /agents/
    |   |-- Enterprise_Assistant.yaml
    |   |-- IT_Support_Agent.yaml
    |-- /tools/
    |   |-- it_support_tools.py
    |-- /knowledge_base/
    |   |-- company_knowledge_base.yaml
    |-- /mock_docs/
    |   |-- Employee_Onboarding_Guide.txt
    |   |-- IT_Security_Policies.txt
    |   |-- VPN_Setup_Instructions.txt
    |-- requirements.txt
    ```

## Step 1: Create Mock Knowledge Base Documents
The foundation of the RAG capability is the set of internal documents the assistant will use to answer questions. For this demo, we will create placeholder text files to simulate real corporate documents, which is a practical approach for a proof-of-concept.

1.  Navigate to your project directory and create the `mock_docs` folder.
2.  Inside `mock_docs`, create the following three files with sample content:

    *   **`IT_Security_Policies.txt`**:
        ```text
        Company IT Security Policy - Version 3.1

        Section 1: Personal Device Usage (BYOD)
        Employees are permitted to use personal devices for work-related tasks, provided the device is enrolled in the company's Mobile Device Management (MDM) solution. All work-related data must be stored within encrypted containers managed by the company. Access to internal resources from personal devices requires two-factor authentication (2FA). Any loss of a personal device containing company data must be reported to the IT department within 2 hours.
        ```

    *   **`Employee_Onboarding_Guide.txt`**:
        ```text
        Welcome to the Team! - Employee Onboarding Guide

        Your First Week:
        - Day 1: Meet your manager and team. Get your hardware and account credentials.
        - Day 2: Complete HR orientation and benefits enrollment.
        - Day 3: Set up your development environment. Review the IT Security Policies.
        ```

    *   **`VPN_Setup_Instructions.txt`**:
        ```text
        VPN Setup Instructions for Remote Access

        1. Open the "GlobalProtect" VPN client on your laptop.
        2. In the portal address field, enter: vpn.ourcompany.com
        3. Click "Connect". You will be prompted to enter your company username and password.
        4. Approve the connection via the push notification on your registered mobile device.
        5. Once connected, you can access internal network resources.
        ```

## Step 2: Define the Knowledge Base Configuration
This YAML file defines the knowledge base that the `Enterprise_Assistant` will use. It points to the mock documents we just created and configures them to be ingested into the built-in Milvus vector database provided by watsonx Orchestrate.

1.  Inside the `/knowledge_base/` directory, create the file `company_knowledge_base.yaml`.
2.  Add the following content. This configuration specifies the name, description, and paths to the documents that will form the knowledge corpus. The `embeddings_model_name` has been set to the recommended `ibm/slate-125m-english-rtrvr-v2` for optimal performance.

```yaml
# /knowledge_base/company_knowledge_base.yaml
spec_version: v1
kind: knowledge_base
name: company_knowledge_base
description: >
  Contains internal company documents including IT policies, employee handbooks,
  and technical setup guides for employee questions.
documents:
  - "./mock_docs/Employee_Onboarding_Guide.txt"
  - "./mock_docs/IT_Security_Policies.txt"
  - "./mock_docs/VPN_Setup_Instructions.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Develop the Specialist Agent's Tools
The `IT_Support_Agent` requires tools to perform its specialized functions. We will create these as Python functions decorated with `@tool`. These tools will simulate interactions with a ServiceNow-like ITSM system by returning realistic, hardcoded data structures.

1.  Inside the `/tools/` directory, create the file `it_support_tools.py`.
2.  Add the following Python code.

```python
# /tools/it_support_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# In-memory dictionary to simulate a database of created tickets
# This allows the demo to maintain state between tool calls
MOCK_TICKET_DB = {}

@tool(name="create_service_now_incident", permission=ToolPermission.ADMIN)
def create_service_now_incident(short_description: str) -> str:
    """
    Creates a new incident ticket in the IT Service Management system (e.g., ServiceNow).
    This tool is used when an employee reports a new IT issue that requires tracking.

    Args:
        short_description (str): A brief, one-sentence summary of the user's IT issue.

    Returns:
        str: A JSON string containing a confirmation message and details of the created ticket.
    """
    # Business Value: This tool automates the creation of L1 support tickets, reducing manual
    # entry for both employees and the IT help desk. It ensures that all issues are logged
    # consistently and immediately, accelerating the time to resolution and providing a clear
    # audit trail for every reported problem.
    #
    # Technical Implementation: This function simulates a POST request to an ITSM API. It generates a
    # unique ticket number and a realistic data structure for the new incident, including metadata like
    # timestamps, priority, and category. The ticket is stored in a mock in-memory database to allow
    # for follow-up status checks within the same demo session.
    try:
        ticket_number = f"INC{random.randint(1000000, 9999999)}"
        timestamp = datetime.utcnow().isoformat() + "Z"

        new_ticket = {
            "ticket_number": ticket_number,
            "status": "New",
            "short_description": short_description,
            "category": "Hardware",
            "priority": "3 - Medium",
            "assignment_group": "IT Help Desk",
            "caller_id": "employee@example.com", # Mocked user
            "created_at": timestamp,
            "updated_at": timestamp
        }

        MOCK_TICKET_DB[ticket_number] = new_ticket

        response = {
            "message": f"Successfully created IT support ticket {ticket_number}.",
            "ticket_details": new_ticket
        }
        return json.dumps(response, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to create ticket: {str(e)}"})


@tool(name="get_incident_status_by_number", permission=ToolPermission.ADMIN)
def get_incident_status_by_number(ticket_number: str) -> str:
    """
    Retrieves the current status and details of an existing IT incident ticket by its number.
    Use this tool when an employee asks for an update on a ticket they have already created.

    Args:
        ticket_number (str): The unique identifier of the incident ticket (e.g., "INC1234567").

    Returns:
        str: A JSON string containing the details of the ticket or an error message if not found.
    """
    # Business Value: This tool provides employees with self-service access to the status of their
    # IT tickets, 24/7. This reduces follow-up calls and emails to the help desk, freeing up
    # IT staff to focus on resolving issues rather than providing routine status updates, thus
    # improving overall IT department efficiency and employee satisfaction.
    #
    # Technical Implementation: This function simulates a GET request to an ITSM API endpoint.
    # It looks up the provided ticket_number in our mock in-memory database. If found, it realistically
    # simulates a potential status update (e.g., moving from 'New' to 'In Progress') and returns
    # the ticket's full data structure. Otherwise, it returns a clear "not found" error.
    if ticket_number in MOCK_TICKET_DB:
        ticket_details = MOCK_TICKET_DB[ticket_number]
        
        # Simulate a potential status update for demo purposes
        if ticket_details["status"] == "New" and random.random() > 0.5:
             ticket_details["status"] = "In Progress"
             ticket_details["assignment_group"] = "Network Support Team"
             ticket_details["updated_at"] = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
             MOCK_TICKET_DB[ticket_number] = ticket_details

        return json.dumps(ticket_details, indent=2)
    else:
        return json.dumps({"error": f"Ticket {ticket_number} not found."}, indent=2)

```

3.  Create the `requirements.txt` file in the root of your project directory. While our tools have no external dependencies, it's a best practice to include this file for future scalability.

```
# /requirements.txt
# No external packages are required for these tools.
```

## Step 4: Define the Agent Configurations
With the tools and knowledge base defined, we can now configure the agents themselves using YAML.

### IT Support Agent (Collaborator)
This is the specialist agent, whose sole purpose is to execute IT support tasks using its tools. Its description is critical, as it tells the supervisor agent what it's capable of, enabling effective delegation.

1.  Inside the `/agents/` directory, create `IT_Support_Agent.yaml`.
2.  Add the following configuration:

```yaml
# /agents/IT_Support_Agent.yaml
spec_version: v1
kind: native
name: IT_Support_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent specializing in IT support tasks. Use this agent to create new IT incidents
  in ServiceNow or check the status of existing incidents by number. It is equipped with
  tools to interact directly with the IT Service Management system for ticket creation
  and status retrieval.
instructions: >
  You are an expert IT Support agent. Your only functions are to create new IT tickets
  and check the status of existing ones. Use your tools to perform these actions.
  When a ticket is created, confirm the ticket number back to the user.
  When checking a status, provide the current status and assignment group.
tools:
  - create_service_now_incident
  - get_incident_status_by_number
```

### Enterprise Assistant (Supervisor)
This is the main, user-facing agent. Its configuration defines its role, its connection to the knowledge base, and its ability to collaborate with the `IT_Support_Agent`. The instructions are key to its reasoning process, guiding it on when to use RAG and when to delegate.

1.  Inside the `/agents/` directory, create `Enterprise_Assistant.yaml`.
2.  Add the following configuration:

```yaml
# /agents/Enterprise_Assistant.yaml
spec_version: v1
kind: native
name: Enterprise_Assistant
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A primary assistant for employees. It answers general company policy and procedure
  questions by searching its internal knowledge base. It can also delegate specialized
  tasks, such as creating or checking IT support tickets, to the IT_Support_Agent collaborator.
instructions: >
  Your primary role is to be a helpful and efficient enterprise assistant for employees.
  Follow these reasoning steps meticulously:
  1. First, analyze the user's request to determine their core intent.
  2. If the user is asking a general question about company policies, procedures, or how-to guides (e.g., "what is the policy on...", "how do I set up..."), you MUST use your knowledge base to find the answer and provide a helpful summary.
  3. If the user explicitly asks to create, open, or file an IT ticket, or describes a technical problem with their hardware or software (e.g., "my laptop is broken", "I can't connect to Wi-Fi"), you MUST delegate the task to the IT_Support_Agent. Do not attempt to solve the IT problem yourself.
  4. If the user asks for the status of an existing ticket and provides a ticket number, you MUST delegate the task to the IT_Support_Agent.
  5. Always be polite and professional in your responses. Confirm actions taken, such as ticket creation, with the information provided by the collaborator.
collaborators:
  - IT_Support_Agent
knowledge_base:
  - company_knowledge_base
```

## Step 5: Deploy the Solution with the ADK CLI
Now we will use the `orchestrate` CLI to import all our assets in the correct order. Dependencies (knowledge bases, tools) must be imported before the assets that use them (agents).

Execute these commands from the root of your `/unified-enterprise-assistant/` project directory.

1.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledge-bases import -f ./knowledge_base/company_knowledge_base.yaml
    ```
    *This command reads your YAML configuration, finds the specified documents, chunks and embeds them using the `ibm/slate-125m-english-rtrvr-v2` model, and stores the vectors in the built-in knowledge base, making them available for RAG.*

2.  **Import the Python Tools**:
    ```bash
    orchestrate tools import -k python -f ./tools/it_support_tools.py
    ```
    *This command inspects the Python file, finds the `@tool` decorators, and registers `create_service_now_incident` and `get_incident_status_by_number` as executable actions in your Orchestrate environment.*

3.  **Import the Specialist Agent**:
    ```bash
    orchestrate agents import -f ./agents/IT_Support_Agent.yaml
    ```
    *This command creates the collaborator agent and links it to the tools we just imported. The agent is now available to be called by other agents.*

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f ./agents/Enterprise_Assistant.yaml
    ```
    *This final command creates the main user-facing agent and establishes its connections to both the knowledge base for RAG and its `IT_Support_Agent` collaborator for task delegation.*

## Step 6: Verification and Demo Execution
With all assets deployed, you can now launch the interactive chat to test the demo scenarios.

1.  **Start the Chat**:
    ```bash
    orchestrate chat start
    ```
2.  **Select the Agent**: When prompted, choose the `Enterprise_Assistant` to interact with.

### Demo Scenario 1: Knowledge Retrieval (RAG)
This scenario demonstrates the supervisor agent's ability to answer questions directly using its knowledge base.

*   **User Prompt**:
    ```
    What is the company policy on using personal devices for work?
    ```
*   **Expected Orchestrate Action & Response**: The `Enterprise_Assistant` will identify this as a knowledge query. It will search the `company_knowledge_base`, find the relevant passage in `IT_Security_Policies.txt`, and synthesize a grounded answer. The response should be similar to:
    > "According to our IT Security Policy, you are permitted to use personal devices for work, but they must be enrolled in the company's Mobile Device Management (MDM) solution and use two-factor authentication for accessing internal resources."

### Demo Scenario 2: Task Delegation and Automation
This scenario shows the supervisor delegating a task to the specialist agent.

*   **User Prompt**:
    ```
    My laptop screen is flickering constantly. I need to open a ticket.
    ```
*   **Expected Orchestrate Action & Response**: The `Enterprise_Assistant` will recognize the intent to create a ticket and delegate the request to the `IT_Support_Agent`. The specialist agent will then invoke the `create_service_now_incident` tool. The final response to the user will be a confirmation:
    > "I have created IT support ticket INC1234567 for your flickering laptop screen issue. The IT Help Desk will be in touch shortly."

### Demo Scenario 3: Follow-up and State Tracking
This scenario demonstrates the ability to follow up on a previously created task.

*   **User Prompt** (use the ticket number from the previous response):
    ```
    Can you check the status of ticket INC1234567?
    ```
*   **Expected Orchestrate Action & Response**: The `Enterprise_Assistant` will again delegate to the `IT_Support_Agent`. The specialist will use the `get_incident_status_by_number` tool with the provided ticket number and return the mock status to the user:
    > "Ticket INC1234567 is currently 'In Progress' and has been assigned to the Network Support Team."

## Troubleshooting
If you encounter issues, here are some common problems and their solutions:

*   **Issue**: Agent responds "I can't do that" or fails to delegate.
    *   **Solution**: This is often due to poorly defined descriptions or instructions. Ensure the `IT_Support_Agent`'s `description` clearly states its capabilities (creating/checking tickets). Verify the `Enterprise_Assistant`'s `instructions` explicitly tell it to delegate IT-related tasks.
*   **Issue**: `ToolNotFound` error during agent import or chat.
    *   **Solution**: This means the tool was not imported successfully before the agent that uses it. Re-run the `orchestrate tools import ...` command and then re-import the `IT_Support_Agent`.
*   **Issue**: Knowledge base query returns "I don't know".
    *   **Solution**: Check the file paths in `company_knowledge_base.yaml` to ensure they are correct relative to where you are running the command. Also, ensure the content of the mock documents contains keywords relevant to your test questions.
*   **Issue**: Python `ModuleNotFoundError`.
    *   **Solution**: While our example has no external dependencies, in a real-world scenario this means a required package is not installed. Ensure you have run `pip install -r requirements.txt`.

## Best Practices
This demo plan incorporates several IBM best practices for building robust and scalable agentic solutions with watsonx Orchestrate.

*   **Supervisor/Collaborator Pattern**: The separation of a generalist supervisor (`Enterprise_Assistant`) from a domain specialist (`IT_Support_Agent`) is a powerful design pattern. It makes the system modular, easier to maintain, and scalable. You can add more specialist agents (e.g., `HR_Agent`, `Finance_Agent`) without modifying the supervisor.
*   **Descriptive Naming and Descriptions**: The `description` fields for agents and docstrings for tools are not just for documentation; they are critical inputs for the LLM's reasoning and routing engine. Well-crafted descriptions lead to more accurate and reliable agent behavior.
*   **Declarative Definitions**: Using YAML to define agents and knowledge bases allows for a clear, version-controlled, and environment-agnostic definition of your solution's architecture.
*   **Stateless, Modular Tools**: Tools should be designed as stateless functions that perform one specific task well. This makes them reusable across different agents and simplifies testing and maintenance. The use of a temporary in-memory dictionary is a good pattern for demos that require state.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
