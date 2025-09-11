# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-11 16:15:49
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Orchestrated Onboarding for New Instructors

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Orchestrated Onboarding for New Instructors" demo using IBM watsonx Orchestrate. The solution is tailored to the client's specific need for a 24/7, automated onboarding assistant. By implementing a multi-agent system, we will demonstrate how watsonx Orchestrate can significantly accelerate new instructor productivity, reduce the administrative burden on HR and IT staff, and create a seamless, modern onboarding experience.

The core of this solution is a supervisor-collaborator agent architecture. A primary "Concierge" agent will interact with the new instructor, intelligently understanding their requests and delegating tasks to specialized collaborator agents. One collaborator will handle question-answering using a knowledge base of onboarding documents (RAG), while another will execute transactional tasks like creating IT tickets and checking HR system statuses. This plan details the creation of all required assets—agents, tools, and knowledge bases—and provides the exact code and commands for a successful deployment, incorporating best practices for project organization and dependency management.

## Prerequisites

Before beginning, ensure your environment is correctly set up. This is crucial for the successful import and execution of the agents and tools.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. Follow the official documentation for installation instructions.
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required to create the custom tools.
3.  **Orchestrate Environment Configuration**: Your ADK must be logged into your watsonx Orchestrate environment. Run the following command and follow the prompts to log in:
    ```bash
    orchestrate login
    ```
4.  **Mock Documents**: The demo requires three synthetic documents. You must create these files before starting the implementation. The content can be placeholder text, but the files must exist for the knowledge base ingestion to succeed.

## Step 1: Prepare the Project Structure and Mock Data

A well-organized project structure is essential for managing the different components of the solution. This revised structure separates knowledge base configurations from agent configurations for improved clarity and scalability.

1.  **Create the Directory Structure**: In your terminal, create the following folders. This structure will house the agent configurations, tools, knowledge base definitions, and mock documents.

    ```bash
    mkdir -p orchestrate_onboarding_demo/{agents,tools,knowledge_bases,mock_data}
    cd orchestrate_onboarding_demo
    ```

2.  **Create Mock Data Files**: Inside the `mock_data` directory, create the three source documents for the knowledge base. For this demo, you can create empty files or add some sample text relevant to each document's purpose.

    ```bash
    # In the mock_data directory
    touch Instructor_Handbook.pdf
    touch Benefits_Enrollment_Guide.docx
    touch IT_Setup_and_Policies.txt
    ```
    *   **Instructor_Handbook.pdf**: This document should contain mock company policies, classroom procedures, and performance expectations.
    *   **Benefits_Enrollment_Guide.docx**: This document should detail mock health plans (PPO, HDHP), retirement options, and enrollment deadlines.
    *   **IT_Setup_and_Policies.txt**: This document should contain instructions for setting up a laptop, accessing internal systems like the LMS, and software usage policies.

## Step 2: Create the Knowledge Base

The knowledge base will provide the `Onboarding Knowledge Agent` with the information it needs to answer instructor questions. We will use the built-in Milvus vector database to ingest our mock documents.

**Business Value**: This component directly addresses the need for 24/7, consistent, and accurate information delivery. It offloads the repetitive task of answering common questions from HR staff and empowers new hires to find information independently.

1.  Create a new file named `onboarding_kb.yaml` inside the `knowledge_bases` directory.
2.  Add the following YAML configuration. This defines the knowledge base, gives it a descriptive name, and points to the documents that need to be ingested.

    ```yaml
    # knowledge_bases/onboarding_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: instructor_onboarding_materials_kb
    description: >
      Contains essential documents for new instructors, including the employee handbook, benefits guide, and IT setup instructions. This knowledge base is the primary source of truth for company policies, procedures, and benefits information.
    documents:
      - "mock_data/Instructor_Handbook.pdf"
      - "mock_data/Benefits_Enrollment_Guide.docx"
      - "mock_data/IT_Setup_and_Policies.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 3: Develop the Custom Python Tools

These tools provide the `HR & IT Services Agent` with the ability to perform actions in external systems. We will create two tools in a single Python file to simulate interactions with IT and HR helpdesks.

1.  Create a file named `hr_it_tools.py` inside the `tools` directory.
2.  Add the following Python code to the file. This file contains the implementation for both the IT support ticket creation and the benefits enrollment status check.

    ```python
    # tools/hr_it_tools.py
    import random
    import datetime
    from typing import Dict, Any

    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    # --- Tool 1: Create IT Support Ticket ---

    @tool(permission=ToolPermission.ADMIN)
    def create_it_support_ticket(issue_description: str) -> str:
        """
        Creates an IT support ticket in the helpdesk system for a new instructor.

        Use this tool when a user reports a technical problem they cannot solve,
        such as being unable to access a system, software issues, or hardware problems.

        Args:
            issue_description (str): A detailed description of the IT issue the user is facing.
                                     This should be captured from the user's request.

        Returns:
            str: A confirmation message including the new, unique ticket number.
        """
        # In a real-world scenario, this would be an API call to a system like ServiceNow or Jira.
        # We simulate this by generating a random ticket number.
        ticket_number = f"INC-{random.randint(10000, 99999)}"
        print(f"--- MOCK API CALL ---")
        print(f"Creating ticket for issue: {issue_description}")
        print(f"Generated Ticket ID: {ticket_number}")
        print(f"--------------------")
        
        return f"Successfully created IT support ticket. Your ticket number is {ticket_number}."

    # --- Tool 2: Check Benefits Enrollment Status ---

    # Mock database of employee enrollment statuses
    MOCK_ENROLLMENT_DATA = {
        "alex.chen": {
            "status": "Completed",
            "confirmation_id": "BEN-8A3B5C",
            "completion_date": (datetime.date.today() - datetime.timedelta(days=2)).isoformat(),
            "plan_selection": "HDHP Plus"
        },
        "brenda.vance": {
            "status": "Not Started",
            "confirmation_id": None,
            "completion_date": None,
            "plan_selection": None
        },
        "charles.ingram": {
            "status": "In Progress",
            "confirmation_id": None,
            "completion_date": None,
            "plan_selection": None
        }
    }

    @tool(permission=ToolPermission.ADMIN)
    def check_benefits_enrollment_status(employee_username: str) -> Dict[str, Any]:
        """
        Checks the status of a new instructor's benefits enrollment in the HR system.

        Use this tool when a user asks about their enrollment status, if they have completed it,
        or where they are in the process.

        Args:
            employee_username (str): The username of the employee (e.g., 'firstname.lastname').
                                     The agent should infer this from the user's identity. For the demo,
                                     we will use one of the mock users: 'alex.chen', 'brenda.vance', 'charles.ingram'.

        Returns:
            dict: A dictionary containing the enrollment status and related details.
                  Returns a not found message if the user does not exist.
        """
        # In a real-world scenario, this would query an HRIS API.
        # We simulate this by looking up the user in our mock dictionary.
        username = employee_username.lower()
        print(f"--- MOCK API CALL ---")
        print(f"Querying benefits status for username: {username}")
        
        status_info = MOCK_ENROLLMENT_DATA.get(username, {
            "status": "User Not Found",
            "details": "Could not find an enrollment record for the specified user."
        })
        
        print(f"Found Status: {status_info}")
        print(f"--------------------")
        
        return status_info
    ```

### Tool Explanations

*   **`create_it_support_ticket`**: This tool provides a direct action to resolve technical issues. Its business value lies in its immediacy; instead of telling an instructor *how* to get help, the agent *gets* them help directly. This reduces user frustration and downtime, creating a more supportive onboarding environment and logging issues in a structured way for the IT department.
*   **`check_benefits_enrollment_status`**: This tool integrates with a core HR process. Its value is providing new hires with self-service access to critical onboarding information. It reduces inquiries to the HR benefits team and gives instructors peace of mind by allowing them to verify the status of this crucial onboarding step at any time.

## Step 4: Define the Agent Architecture (YAML Configuration)

Now we will define the three agents that form our solution. We will start with the collaborators and finish with the supervisor.

### Agent 1: Onboarding Knowledge Agent (Collaborator)

This agent is a specialist in information retrieval. Its sole purpose is to search the knowledge base and provide accurate answers to policy and procedure questions.

1.  Create a file named `onboarding_knowledge_agent.yaml` in the `agents` directory.
2.  Add the following YAML configuration:

    ```yaml
    # agents/onboarding_knowledge_agent.yaml
    spec_version: v1
    kind: native
    name: onboarding_knowledge_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert agent that answers questions about new instructor onboarding. It has access to a knowledge base containing the Instructor Handbook, Benefits Enrollment Guide, and IT policies. Use this agent for any questions related to company policies, procedures, benefits details, or IT setup instructions. It does not perform actions.
    instructions: >
      You are an expert on company policies for new instructors. Your only function is to answer questions based on the documents in your knowledge base. Provide clear, concise answers and cite the source document if possible. Do not answer questions outside the scope of the provided materials.
    tools: []
    knowledge_base:
      - instructor_onboarding_materials_kb
    ```

### Agent 2: HR & IT Services Agent (Collaborator)

This agent is a task execution specialist. It is equipped with the tools we created to interact with mock HR and IT systems.

1.  Create a file named `hr_it_services_agent.yaml` in the `agents` directory.
2.  Add the following YAML configuration:

    ```yaml
    # agents/hr_it_services_agent.yaml
    spec_version: v1
    kind: native
    name: hr_it_services_agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A service agent that performs actions in HR and IT systems. It can create IT support tickets for technical issues and check the status of an employee's benefits enrollment. Use this agent for requests that require taking an action or checking a status in a backend system.
    instructions: >
      You are a service agent that executes tasks.
      - Use the 'create_it_support_ticket' tool when a user describes a technical problem they are facing.
      - Use the 'check_benefits_enrollment_status' tool when a user asks about the status of their benefits enrollment.
      - Clearly confirm the result of the action back to the user.
    tools:
      - create_it_support_ticket
      - check_benefits_enrollment_status
    ```

### Agent 3: Instructor Onboarding Concierge (Supervisor)

This is the main, user-facing agent. It acts as an intelligent router, delegating tasks to its specialist collaborators based on the user's intent.

1.  Create a file named `instructor_onboarding_concierge.yaml` in the `agents` directory.
2.  Add the following YAML configuration:

    ```yaml
    # agents/instructor_onboarding_concierge.yaml
    spec_version: v1
    kind: native
    name: instructor_onboarding_concierge
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A helpful assistant for new instructors. It can answer questions about company policies, benefits, and IT setup by consulting its knowledge expert. It can also create IT tickets and check HR system statuses by collaborating with the services agent. This is the primary agent for all new instructor inquiries.
    instructions: >
      You are the primary contact for a new instructor. Your main role is to understand the user's needs and delegate to the correct collaborator agent to fulfill the request.
      - For any questions about "what is", "how to", "what is the policy", or requests for information from documents, you MUST use the 'onboarding_knowledge_agent'.
      - For any requests that require performing an action like creating a ticket or checking a status in a system, you MUST use the 'hr_it_services_agent'.
      - Manage the full conversation, presenting the results from collaborators back to the user in a helpful, conversational manner.
    collaborators:
      - onboarding_knowledge_agent
      - hr_it_services_agent
    tools: []
    ```

## Step 5: Deploy the Solution using the ADK CLI

With all configuration files in place, we will now use the `orchestrate` CLI to import all assets into the watsonx Orchestrate environment. The order of operations is important to ensure dependencies are met.

**Process Explanation**: We must import assets in a specific order: tools first, as agents depend on them; then the knowledge base; then collaborator agents; and finally, the supervisor agent which depends on the collaborators.

Execute the following commands from the root of your `orchestrate_onboarding_demo` directory:

1.  **Import the Python Tools**:
    ```bash
    orchestrate tools import -f tools/hr_it_tools.py
    ```
2.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/onboarding_kb.yaml
    ```
    *Note: The knowledge base will begin ingesting the documents. This may take a few minutes.*

3.  **Import the Collaborator Agents**:
    ```bash
    orchestrate agents import -f agents/onboarding_knowledge_agent.yaml
    orchestrate agents import -f agents/hr_it_services_agent.yaml
    ```
4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/instructor_onboarding_concierge.yaml
    ```

## Step 6: Verification and Demo Execution

After successfully importing all assets, you can test the complete solution using the interactive chat.

1.  **Start the Chat**: Run the following command to begin a chat session. You will be prompted to select which agent to chat with.
    ```bash
    orchestrate chat start
    ```
2.  **Select the Agent**: At the prompt, choose the `instructor_onboarding_concierge` agent.

3.  **Run Demo Scenarios**: Test the system using the client's specified scenarios.

    *   **Scenario 1: Information Retrieval (Knowledge Agent)**
        *   **User Prompt:** `What is the policy for using personal devices in the classroom?`
        *   **Expected Flow:** The `Concierge` agent will receive the query, identify it as a policy question, and delegate to the `Onboarding Knowledge Agent`. This agent will perform a RAG search on `Instructor_Handbook.pdf` and return a synthesized answer, which the `Concierge` will present to you.

    *   **Scenario 2: Action & Task Execution (HR & IT Services Agent)**
        *   **User Prompt:** `I can't access the LMS. Can you help me?`
        *   **Expected Flow:** The `Concierge` agent will identify this as a request for IT support. It will route the task to the `HR & IT Services Agent`, which will execute the `create_it_support_ticket` tool. The agent will respond with a confirmation message and a unique ticket number.

    *   **Scenario 3: Multi-Step Orchestration (Supervisor & Collaborators)**
        *   **User Prompt:** `I read the benefits guide but I'm confused about the HDHP plan. Can you explain it and then check the status of my enrollment? My username is brenda.vance.`
        *   **Expected Flow:**
            1.  The `Concierge` agent will first delegate the "explain HDHP" part to the `Onboarding Knowledge Agent`, which will summarize the plan from the `Benefits_Enrollment_Guide.docx`.
            2.  After presenting the information, the `Concierge` will delegate the "check my enrollment" part to the `HR & IT Services Agent`.
            3.  This agent will use the `check_benefits_enrollment_status` tool with the username `brenda.vance` and respond with "Not Started", which the `Concierge` will relay to you. This demonstrates seamless task switching and complex query resolution.

## Troubleshooting

*   **Agent Import Fails**: If an agent import fails, check for dependencies. For example, the `instructor_onboarding_concierge` will fail to import if its collaborators (`onboarding_knowledge_agent`, `hr_it_services_agent`) do not exist yet. Ensure you import assets in the correct order.
*   **Incorrect Agent Routing**: If the `Concierge` agent routes a task to the wrong collaborator (e.g., sends an IT request to the knowledge agent), refine the `description` and `instructions` in the agent YAML files. The supervisor relies heavily on these fields to make routing decisions. Make them more explicit about which agent handles which type of task.
*   **Tool Not Found**: If an agent reports it cannot find a tool, ensure the tool was imported successfully using `orchestrate tools list`. Also, verify the tool name in the agent's YAML file exactly matches the function name in the Python file.
*   **Knowledge Base Not Ready**: If the `Onboarding Knowledge Agent` cannot find information, check the status of the knowledge base with `orchestrate knowledge-bases status --name instructor_onboarding_materials_kb`. Ensure the `Ready` property is `true`.

## Best Practices

*   **Descriptive Naming and Descriptions**: As demonstrated in this plan, use clear, unique names for all assets. The `description` fields are not just for users; they are critical for the supervisor agent's reasoning process. The more descriptive you are, the better the routing will be.
*   **Modular Asset Organization**: Keep different asset types (agents, tools, knowledge bases) in separate directories. This practice, implemented in this plan, enhances project clarity and is crucial for managing larger, more complex solutions.
*   **Explicit Instructions**: In the supervisor agent's `instructions`, be very direct about which collaborator to use for specific scenarios (e.g., "For questions about policies, you MUST use..."). This reduces ambiguity and improves the reliability of task delegation.
*   **Iterative Testing**: After making changes to any agent's description or instructions, re-import the agent and test all demo scenarios again to ensure the changes haven't caused regressions in behavior.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
