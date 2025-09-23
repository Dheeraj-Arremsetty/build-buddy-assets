# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 14:47:41
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Employee Lifecycle Orchestrator

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **AI-Powered Employee Lifecycle Orchestrator** demo for the client. This solution is meticulously designed to address the client's core challenges in employee lifecycle management by showcasing a modern, AI-driven approach that leverages automation, integration, and data processing. By implementing a sophisticated multi-agent system using the **Supervisor/Collaborator pattern** in IBM watsonx Orchestrate, this demo will prove the platform's capability to accelerate new hire onboarding, eliminate security risks during offboarding, and unlock significant efficiency gains for HR and IT departments.

The plan details the creation of a central `EmployeeLifecycle_Supervisor` agent that serves as a single, conversational interface. This supervisor will intelligently interpret natural language commands and delegate tasks to a suite of specialized collaborator agents. These collaborators are designed to interact with mock enterprise systems for IT (ServiceNow), Identity Management (Okta), and Learning Management (LMS). Furthermore, we will integrate a knowledge base to handle policy-related inquiries, demonstrating a complete, end-to-end automated workflow that directly aligns with the client's strategic goals of enhancing productivity and reducing operational friction.

## 2. Prerequisites

Before beginning the implementation, ensure your development environment is correctly configured with all necessary components. A proper setup is crucial for a smooth development and deployment process.

*   **Python:** Python version 3.9 or higher is required. The IBM watsonx Orchestrate ADK is built on Python, and its tools are defined as Python functions.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit (ADK) is the core library for this project. If not already installed, run the following command in your terminal:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
*   **Orchestrate Environment:** You must have an active IBM watsonx Orchestrate environment initialized. This can be a local Developer Edition for rapid prototyping or a SaaS environment for a more production-like setup.
*   **Project Directory Structure:** A well-organized directory is essential for managing the various artifacts (agents, tools, documents). Create a root folder for the project and then the following subdirectories. This structure is mandatory for the file paths in the configuration files to work correctly.

    ```
    employee_lifecycle_demo/
    ├── agents/
    │   ├── IT_ServiceNow_Agent.yaml
    │   ├── Identity_Okta_Agent.yaml
    │   ├── LMS_Enrollment_Agent.yaml
    │   └── EmployeeLifecycle_Supervisor.yaml
    ├── tools/
    │   ├── it_tools.py
    │   ├── identity_tools.py
    │   └── lms_tools.py
    ├── knowledge_bases/
    │   └── hr_policy_kb.yaml
    ├── documents/
    │   └── HR_Onboarding_Policy.pdf
    └── requirements.txt
    ```

## 3. Step-by-Step Implementation

This section provides the detailed steps, complete code, and configuration files needed to build the entire demo from the ground up.

### Step 3.1: Create Project Structure and Mock Data

Begin by setting up the project directory as detailed above. Then, create the necessary mock data files and dependencies that will power the demo.

1.  **Create `requirements.txt`:** In the root of your `employee_lifecycle_demo` directory, create this file. It will manage the Python dependencies for our tools.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
2.  **Create `documents/HR_Onboarding_Policy.pdf`:** Create a PDF document containing the following text. This document serves as the "source of truth" for the knowledge base, allowing the supervisor agent to answer policy questions directly.
    ```text
    HR Onboarding and Hardware Policy - v4.0

    Section 1: Standard Hardware Packages by Role

    1.1 Software Engineer:
       - Laptop: 16-inch MacBook Pro M3 (or equivalent high-performance laptop)
       - Monitor: 32-inch 4K Display
       - Peripherals: Mechanical Keyboard, Ergonomic Mouse
       - Access: Full Admin rights on local machine.

    1.2 Marketing Manager:
       - Laptop: 13-inch MacBook Air
       - Monitor: 27-inch external monitor
       - Peripherals: Standard Wireless Keyboard and Mouse
       - Access: Standard user rights.

    1.3 Sales Representative:
       - Laptop: 14-inch Lenovo ThinkPad
       - Monitor: None (Portable monitor available upon request)
       - Peripherals: High-Quality Wireless Headset

    Section 2: Required Training Courses

    2.1 All New Hires (Mandatory within first 30 days):
        - "New Hire Security Awareness Training" (Course ID: SEC101)
        - "Corporate Code of Conduct" (Course ID: CND101)

    2.2 Engineering Department:
        - "Introduction to Engineering Practices" (Course ID: ENG201)

    2.3 Sales Department:
        - "CRM Best Practices and Usage" (Course ID: SLS201)
    ```
3.  **Install Dependencies:** Open your terminal, navigate to the project's root directory, and run the following command to install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

### Step 3.2: Develop Python Tools

Here, we will create the Python tools that our collaborator agents will use to perform actions. These tools simulate interactions with external enterprise systems by generating realistic, structured synthetic data. Each tool's docstring is critically important, as it serves as the description the LLM uses to understand the tool's function, arguments, and return value.

#### **IT ServiceNow Tools (`tools/it_tools.py`)**

This module contains tools for managing IT service requests, simulating a ServiceNow environment. The `IT_ServiceNow_Agent` will use these to provision hardware and track support tickets. This demonstrates how Orchestrate can automate core IT helpdesk functions, reducing manual effort and ensuring consistency. The tools generate structured JSON data, which is a best practice for providing predictable, parsable output to the agent.

```python
# tools/it_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_servicenow_ticket(employee_name: str, department: str, request_type: str, short_description: str) -> str:
    """
    Creates a ServiceNow incident ticket for a new employee request.

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.
        request_type (str): The type of request (e.g., 'Onboarding Hardware', 'Offboarding Asset Recovery').
        short_description (str): A brief summary of the request.

    Returns:
        str: A JSON string containing a confirmation message and the new ServiceNow ticket number and details.
    """
    ticket_id = f"INC{random.randint(10000, 99999)}"
    response = {
        "status": "success",
        "message": f"Successfully created ServiceNow ticket {ticket_id} for {employee_name}.",
        "ticket": {
            "id": ticket_id,
            "request_type": request_type,
            "status": "New",
            "assigned_to": "IT Support",
            "created_at": datetime.now().isoformat(),
            "short_description": short_description
        }
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def assign_hardware_package(employee_name: str, role: str) -> str:
    """
    Assigns and orders a standard hardware package based on the employee's role from the catalog.

    Args:
        employee_name (str): The full name of the employee.
        role (str): The job role of the employee (e.g., 'Software Engineer', 'Marketing Manager').

    Returns:
        str: A JSON string confirming the hardware package that has been ordered.
    """
    packages = {
        "Software Engineer": "16-inch MacBook Pro, 32-inch 4K Display, Mechanical Keyboard",
        "Marketing Manager": "13-inch MacBook Air, 27-inch external monitor",
        "Sales Representative": "14-inch Lenovo ThinkPad, Wireless Headset"
    }
    package_details = packages.get(role, "Standard Employee Laptop Package")
    order_id = f"HW-ORD-{random.randint(100000, 999999)}"
    
    response = {
        "status": "success",
        "message": f"Hardware package for {employee_name} ({role}) has been ordered.",
        "order_id": order_id,
        "package_details": package_details,
        "estimated_delivery": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def get_ticket_status(ticket_id: str) -> str:
    """
    Retrieves the current status and details of a given ServiceNow ticket.

    Args:
        ticket_id (str): The unique identifier for the ServiceNow ticket (e.g., 'INC12345').

    Returns:
        str: A JSON string with the ticket's details, current status, and update history.
    """
    statuses = ["New", "In Progress", "On Hold", "Resolved", "Closed"]
    created_date = datetime.now() - timedelta(days=random.randint(1, 5))
    
    response = {
        "ticket_id": ticket_id,
        "status": random.choice(statuses),
        "created_date": created_date.isoformat(),
        "last_updated": datetime.now().isoformat(),
        "short_description": "Employee Onboarding Request",
        "updates": [
            {"timestamp": (created_date + timedelta(hours=1)).isoformat(), "comment": "Ticket assigned to IT Support."},
            {"timestamp": (created_date + timedelta(days=1)).isoformat(), "comment": "Hardware order placed."}
        ]
    }
    return json.dumps(response)
```

#### **Identity Okta Tools (`tools/identity_tools.py`)**

This module simulates an Okta environment to handle identity and access management tasks. The `Identity_Okta_Agent` uses these tools to create, modify, and deactivate user accounts. This is a critical function that demonstrates Orchestrate's role in maintaining enterprise security and compliance by ensuring access is granted and revoked in a timely and auditable manner.

```python
# tools/identity_tools.py
import json
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_user_account(employee_name: str, department: str, role: str) -> str:
    """
    Creates a new user account in the identity management system (Okta).

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.
        role (str): The job role of the employee.

    Returns:
        str: A JSON string with the new user's ID, username, and account status.
    """
    username = f"{employee_name.lower().replace(' ', '.')}"
    user_id = f"okta-{random.randint(1000000, 9999999)}"
    response = {
        "status": "success",
        "message": f"Okta user account created for {employee_name}.",
        "user": {
            "id": user_id,
            "username": username,
            "email": f"{username}@examplecorp.com",
            "department": department,
            "role": role,
            "account_status": "active"
        }
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def assign_app_access(username: str, role: str) -> str:
    """
    Assigns access to a standard set of applications based on the employee's role.

    Args:
        username (str): The user's system username (e.g., 'jane.doe').
        role (str): The job role of the employee.

    Returns:
        str: A JSON string confirming the applications assigned.
    """
    app_sets = {
        "Software Engineer": ["Jira", "GitHub", "Slack", "AWS Console", "Confluence"],
        "Marketing Manager": ["Salesforce", "Marketo", "Slack", "Google Analytics", "Asana"],
        "Sales Representative": ["Salesforce", "Slack", "Outreach.io", "LinkedIn Sales Navigator"]
    }
    apps = app_sets.get(role, ["Slack", "Microsoft 365"])
    response = {
        "status": "success",
        "message": f"Application access assigned to {username} for the {role} role.",
        "username": username,
        "assigned_apps": apps
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def deactivate_user_account(username: str) -> str:
    """
    Deactivates a user's account and revokes all application access for offboarding. This is a critical security action.

    Args:
        username (str): The user's system username to deactivate.

    Returns:
        str: A JSON string confirming the account deactivation and access revocation.
    """
    response = {
        "status": "success",
        "message": f"User account for {username} has been DEACTIVATED. All system access and application tokens have been revoked.",
        "username": username,
        "account_status": "deactivated",
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(response)
```

#### **LMS Enrollment Tools (`tools/lms_tools.py`)**

This module simulates a Learning Management System (LMS) to manage employee training enrollments. The `LMS_Enrollment_Agent` uses these tools to ensure new hires are assigned required training. This showcases Orchestrate's ability to automate HR compliance and professional development tasks, ensuring a consistent and complete onboarding experience for every employee.

```python
# tools/lms_tools.py
import json
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def enroll_in_onboarding_training(employee_name: str, department: str) -> str:
    """
    Enrolls a new employee in the standard set of onboarding training courses based on their department.

    Args:
        employee_name (str): The full name of the new employee.
        department (str): The department the employee is joining.

    Returns:
        str: A JSON string confirming the courses the employee has been enrolled in.
    """
    base_courses = [
        {"course_id": "SEC101", "course_name": "New Hire Security Awareness Training"},
        {"course_id": "CND101", "course_name": "Corporate Code of Conduct"}
    ]
    department_courses = {
        "Engineering": [{"course_id": "ENG201", "course_name": "Introduction to Engineering Practices"}],
        "Sales": [{"course_id": "SLS201", "course_name": "CRM Best Practices and Usage"}]
    }
    enrollments = base_courses + department_courses.get(department, [])
    
    response = {
        "status": "success",
        "message": f"{employee_name} has been enrolled in {len(enrollments)} required onboarding courses.",
        "enrolled_courses": enrollments
    }
    return json.dumps(response)

@tool(permission=ToolPermission.ADMIN)
def check_training_completion(employee_name: str) -> str:
    """
    Checks the completion status of required training for a specific employee.

    Args:
        employee_name (str): The full name of the employee.

    Returns:
        str: A JSON string detailing the status of each required training course for the employee.
    """
    courses = [
        {"course_name": "New Hire Security Awareness Training", "status": random.choice(["Completed", "In Progress", "Not Started"]), "due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')},
        {"course_name": "Corporate Code of Conduct", "status": random.choice(["Completed", "In Progress"]), "due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')},
        {"course_name": "Introduction to Engineering Practices", "status": "Not Started", "due_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}
    ]
    response = {
        "employee_name": employee_name,
        "training_status_summary": f"Found {len(courses)} assigned courses.",
        "training_status": courses
    }
    return json.dumps(response)
```

### Step 3.3: Define the Knowledge Base

This YAML file configures a knowledge base. It instructs Orchestrate to ingest the `HR_Onboarding_Policy.pdf` document, process it using an embedding model, and make its content searchable. This enables the supervisor agent to answer policy-related questions accurately and instantly, demonstrating the power of Retrieval-Augmented Generation (RAG) within an automation workflow.

```yaml
# knowledge_bases/hr_policy_kb.yaml
spec_version: v1
kind: knowledge_base
name: hr_policy_kb
description: >
  Contains official company policies and standard operating procedures for HR and IT. This is the primary source for information on hardware packages, required training for new hires, access rights, and other onboarding/offboarding protocols.
documents:
  - "../documents/HR_Onboarding_Policy.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 3.4: Define the Agent Configurations

We will now define the agents using YAML. The `description` and `instructions` fields are the most critical components. The `description` tells the supervisor *what* each collaborator can do, enabling intelligent routing. The `instructions` provide the internal logic and reasoning framework for how each agent should behave and use its tools.

#### **Collaborator Agents**

These specialized agents perform the actual work by executing their assigned tools.

```yaml
# agents/IT_ServiceNow_Agent.yaml
spec_version: v1
kind: native
name: IT_ServiceNow_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent for all IT service management tasks within ServiceNow. Use this agent exclusively for creating and managing IT service tickets related to employee hardware provisioning, software requests, and asset recovery during offboarding. It can also be used to check the status of existing tickets by their ID.
instructions: >
  You are an IT Service Desk specialist. Your persona is efficient and process-oriented.
  - Phase 1: Task Intake. Analyze the request to determine the required ServiceNow action.
  - Phase 2: Tool Execution.
    - For hardware or software requests, use the 'create_servicenow_ticket' tool. Provide a clear short_description.
    - To order a standard hardware kit for a specific role, use the 'assign_hardware_package' tool.
    - If a user asks for an update on a ticket, use the 'get_ticket_status' tool with the provided ticket number.
  - Phase 3: Reporting. Return the structured JSON output from the tool without modification. Do not add conversational filler.
tools:
  - create_servicenow_ticket
  - assign_hardware_package
  - get_ticket_status
```

```yaml
# agents/Identity_Okta_Agent.yaml
spec_version: v1
kind: native
name: Identity_Okta_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  Manages the complete user identity and access lifecycle in Okta. This agent is solely responsible for creating new user accounts, assigning application access based on predefined roles, and, most critically, deactivating accounts for security during employee offboarding.
instructions: >
  You are a security and identity management administrator. Your persona is precise and security-conscious.
  - Phase 1: Task Intake. Identify whether the request is for provisioning, access modification, or de-provisioning.
  - Phase 2: Tool Execution.
    - For new hires, use the 'create_user_account' tool to provision their identity.
    - After creating an account, use the 'assign_app_access' tool to grant access to role-specific applications.
    - For employee offboarding, your highest priority is to use the 'deactivate_user_account' tool IMMEDIATELY to revoke all access. This is a critical security step.
  - Phase 3: Reporting. Return the structured JSON output from the tool. Confirm that security actions have been completed.
tools:
  - create_user_account
  - assign_app_access
  - deactivate_user_account
```

```yaml
# agents/LMS_Enrollment_Agent.yaml
spec_version: v1
kind: native
name: LMS_Enrollment_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  Handles all tasks related to employee training within the corporate Learning Management System (LMS). Use this agent to enroll new hires in required onboarding training courses and to check their completion status.
instructions: >
  You are an HR Learning and Development coordinator. Your persona is helpful and encouraging.
  - Phase 1: Task Intake. Determine if the request is to enroll an employee or check their progress.
  - Phase 2: Tool Execution.
    - When a new employee is onboarded, use the 'enroll_in_onboarding_training' tool to assign them their required courses based on their department.
    - If asked about an employee's training progress, use the 'check_training_completion' tool.
  - Phase 3: Reporting. Return the structured JSON output from the tool. You can add a brief, positive conversational message.
tools:
  - enroll_in_onboarding_training
  - check_training_completion
```

#### **Supervisor Agent**

This is the central orchestrator. Its instructions are the most complex, as they define the logic for delegating to collaborators and using the knowledge base.

```yaml
# agents/EmployeeLifecycle_Supervisor.yaml
spec_version: v1
kind: native
name: EmployeeLifecycle_Supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A master supervisor agent that orchestrates the entire employee lifecycle process, including onboarding and offboarding. It collaborates with specialized agents for IT (ServiceNow), Identity (Okta), and Learning Management (LMS) tasks. It can also answer questions about HR policies by consulting its integrated knowledge base.
instructions: >
  You are a highly efficient AI assistant for HR and IT process orchestration. Your primary goal is to automate complex employee lifecycle workflows by delegating tasks to your specialized collaborator agents.

  **Reasoning Framework:**
  1.  **Policy First:** If the user's query is a question about company policy (e.g., "what is the hardware for...", "what training is required..."), you MUST first use the 'hr_policy_kb' knowledge base to find the answer. Do NOT delegate these questions.
  2.  **Onboarding Workflow:** If the user asks to "onboard" a new employee, you must execute a multi-step process in the following order:
      -   **Step 1:** Delegate to the 'Identity_Okta_Agent' to create a user account and assign app access.
      -   **Step 2:** Delegate to the 'IT_ServiceNow_Agent' to create a ticket for hardware provisioning.
      -   **Step 3:** Delegate to the 'LMS_Enrollment_Agent' to enroll the new hire in training.
      -   **Step 4:** Consolidate the results from all collaborators into a single, comprehensive summary for the user.
  3.  **Offboarding Workflow (Security Priority):** If the user asks to "offboard" an employee, your priority is security. Execute in this order:
      -   **Step 1:** Immediately delegate to the 'Identity_Okta_Agent' to deactivate the user's account. This is the most critical action.
      -   **Step 2:** Delegate to the 'IT_ServiceNow_Agent' to create a ticket for asset recovery.
      -   **Step 3:** Summarize the security actions taken and the ticket number for asset recovery.
  4.  **Single-Task Delegation:** For specific, one-off requests (e.g., "check ticket status INC12345"), identify the correct collaborator based on its description ('IT_ServiceNow_Agent' for tickets) and delegate the task directly.
collaborators:
  - IT_ServiceNow_Agent
  - Identity_Okta_Agent
  - LMS_Enrollment_Agent
knowledge_base:
  - hr_policy_kb
```

### Step 3.5: Deploy the Solution with the ADK CLI

With all files created, you can now import and deploy the entire solution. The order of these commands is critical: tools must be imported before the agents that use them, and collaborators must be imported before the supervisor that uses them.

Execute these commands from the root of your `employee_lifecycle_demo` directory.

1.  **Import all Python tools:** This command registers the Python functions as usable tools within the Orchestrate platform.
    ```bash
    orchestrate tools import -k python -f tools/it_tools.py
    orchestrate tools import -k python -f tools/identity_tools.py
    orchestrate tools import -k python -f tools/lms_tools.py
    ```

2.  **Import the knowledge base:** This command initiates the ingestion process for the PDF document.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/hr_policy_kb.yaml
    ```

3.  **Import the collaborator agents:** This registers the specialized agents and links them to their respective tools.
    ```bash
    orchestrate agents import -f agents/IT_ServiceNow_Agent.yaml
    orchestrate agents import -f agents/Identity_Okta_Agent.yaml
    orchestrate agents import -f agents/LMS_Enrollment_Agent.yaml
    ```

4.  **Import the supervisor agent:** This final step registers the main agent and links it to its collaborators and knowledge base.
    ```bash
    orchestrate agents import -f agents/EmployeeLifecycle_Supervisor.yaml
    ```

## 4. Verification and Demo Scenarios

After successfully importing all assets, start the interactive chat to test the demo scenarios and verify the end-to-end functionality.

**Start the chat environment:**
```bash
orchestrate chat start
```

Use the following prompts to demonstrate the system's capabilities.

#### **Scenario 1: New Hire Onboarding**

This scenario demonstrates the supervisor's ability to orchestrate a complex, multi-agent workflow from a single, high-level command.

*   **User Prompt:** `Onboard the new Software Engineer, Jane Doe, starting next Monday.`
*   **Expected Orchestrate Actions:** The `EmployeeLifecycle_Supervisor` follows its instructions: delegates to the Okta agent, then the ServiceNow agent, then the LMS agent, and finally consolidates the results.
*   **Expected Output (example):** "Onboarding for Jane Doe is in progress.
    *   **Identity:** Okta account 'jane.doe' has been created and assigned 5 developer apps.
    *   **IT:** ServiceNow Ticket INC45892 has been opened for hardware provisioning. The hardware package has been ordered.
    *   **Training:** Jane has been enrolled in 3 required training courses."

#### **Scenario 2: Employee Offboarding**

This scenario highlights the system's ability to execute critical, time-sensitive security procedures automatically and correctly.

*   **User Prompt:** `Process the immediate offboarding for John Smith in Sales.`
*   **Expected Orchestrate Actions:** The `Supervisor` follows its security-first offboarding workflow, delegating to the Okta agent first for immediate access revocation, followed by the ServiceNow agent for asset recovery.
*   **Expected Output (example):** "Offboarding for John Smith is complete. All system access has been revoked via Okta as of [current timestamp]. A high-priority ticket (INC98765) has been created for asset recovery."

#### **Scenario 3: Policy Inquiry (Knowledge Base)**

This scenario shows the supervisor's ability to use its integrated knowledge base to answer questions directly, demonstrating the power of RAG.

*   **User Prompt:** `What is the standard laptop for a new Marketing Manager?`
*   **Expected Orchestrate Actions:** The `Supervisor` identifies this as a policy question, queries the `hr_policy_kb` knowledge base, and synthesizes an answer from the PDF content without using any collaborator agents.
*   **Expected Output:** "According to the HR Onboarding Policy, a new Marketing Manager is issued a 13-inch MacBook Air and a 27-inch external monitor."

## 5. Troubleshooting

*   **Issue: Agent fails to delegate or chooses the wrong collaborator.**
    *   **Solution:** This is almost always due to unclear or overlapping agent `description` fields. Ensure each collaborator's description is highly specific and details the unique capabilities and systems it manages (e.g., "manages IT tickets in **ServiceNow**", "handles user accounts in **Okta**"). Also, refine the `instructions` in the supervisor agent to be more explicit about which collaborator to use for which task.
*   **Issue: `Tool not found` error when an agent tries to execute an action.**
    *   **Solution:** Verify two things: 1) The tool was successfully imported *before* the agent using it. Rerun the `orchestrate tools import...` command for the relevant file. 2) The tool name in the agent's YAML `tools` list exactly matches the function name in the Python file. Check for typos.
*   **Issue: Knowledge base does not return an answer.**
    *   **Solution:** 1) Check the file path in `knowledge_bases/hr_policy_kb.yaml` is correct. 2) Run `orchestrate knowledge-bases status --name hr_policy_kb` to check if the status is `Ready`. If not, the document may still be processing. 3) Ensure the question is answerable from the text within the PDF.
*   **Issue: CLI import fails with a YAML parsing error.**
    *   **Solution:** YAML is very sensitive to indentation. Ensure all indentation uses spaces (not tabs) and is consistent. A common error is incorrect indentation under lists (`tools:`, `collaborators:`, etc.).

## 6. Best Practices

*   **Clarity in Descriptions is Paramount:** The quality of routing in a supervisor/collaborator pattern is directly proportional to the quality of the collaborator agent descriptions. Spend time crafting clear, distinct, and keyword-rich descriptions that highlight the unique function of each agent.
*   **Structured Tool Outputs (JSON):** Returning JSON strings from tools is a powerful best practice. It provides structured, predictable data that the LLM can easily parse, summarize, and use in its final response, leading to more consistent and reliable outcomes.
*   **Iterative Instruction Tuning:** The `instructions` for the supervisor agent act as its core logic. After initial deployment, test various prompts and edge cases, then refine the instructions to improve its reasoning, error handling, and decision-making process. Think of it as programming the agent's behavior.
*   **Idempotent Tools:** Where possible, design tools to be idempotent (safe to run multiple times with the same result). For example, a `create_user_account` tool could first check if the user already exists and, if so, return the existing user's information instead of failing. This makes your automations more robust.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
