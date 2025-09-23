# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 19:40:25
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Orchestrated New Hire Onboarding

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and demonstrating an AI-Orchestrated New Hire Onboarding solution using IBM watsonx Orchestrate. The plan is tailored specifically to the client's request for a multi-agent Proof of Concept (POC) that automates the end-to-end onboarding workflow.

The solution addresses the core business challenge of coordinating complex, cross-departmental processes. By implementing a central supervisor agent that intelligently delegates tasks to specialized HR, IT, and Training collaborator agents, the client can significantly reduce manual administrative effort, accelerate time-to-productivity for new hires, and ensure a consistent, high-quality onboarding experience. This plan will build the full agent architecture, create all necessary tools with realistic mock data, configure a knowledge base for HR policies, and provide a script for demonstrating key business scenarios.

## 2. Prerequisites

Before beginning, ensure your development environment is set up with the following components:

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed and configured. If not installed, run:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Python**: A recent version of Python (3.9 or higher) is required.
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized. If not, run `orchestrate env init` and follow the prompts.
*   **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and managing the Python and YAML files.
*   **Mock Documents**: You will need to create placeholder PDF files for the knowledge base. These can be simple, one-page documents.

## 3. Project Structure

To maintain a clean and organized project, create the following directory structure. This structure separates agents, tools, knowledge bases, and mock data, simplifying management and deployment.

```
/new-hire-onboarding-demo
├── agents/
│   ├── onboarding_supervisor_agent.yaml
│   ├── hr_onboarding_agent.yaml
│   ├── it_provisioning_agent.yaml
│   └── training_enrollment_agent.yaml
├── tools/
│   ├── hr_tools.py
│   ├── it_tools.py
│   └── training_tools.py
├── knowledge_bases/
│   └── hr_policy_kb.yaml
├── mock_data/
│   └── docs/
│       ├── Benefits_Guide_PPO.pdf
│       ├── Remote_Work_Policy.pdf
│       └── Code_of_Conduct.pdf
└── requirements.txt
```

**Action:**
1.  Create the main project folder: `mkdir new-hire-onboarding-demo && cd new-hire-onboarding-demo`
2.  Create the subdirectories: `mkdir agents tools knowledge_bases mock_data mock_data/docs`
3.  Create the empty mock PDF files:
    ```bash
    touch mock_data/docs/Benefits_Guide_PPO.pdf
    touch mock_data/docs/Remote_Work_Policy.pdf
    touch mock_data/docs/Code_of_Conduct.pdf
    ```
    *(Note: For the demo, these files can be empty or contain simple text. In a real scenario, they would hold the actual policy documents.)*

## 4. Step 1: Create Python Package Dependencies

Create a `requirements.txt` file to manage any Python libraries your tools might need. For this demo, we will use the `requests` library as a placeholder for potential future API calls, which is a common pattern.

**File:** `requirements.txt`
```text
# This file lists the Python packages required by the custom tools.
# The orchestrate ADK will automatically handle these dependencies.
requests
```

## 5. Step 2: Create Custom Python Tools

The tools are the functional heart of the collaborator agents, performing the actual tasks. We will create three sets of tools, each in its own Python file, to simulate interactions with HR, IT, and Training systems. Each tool generates realistic synthetic data to provide meaningful outputs during the demo.

### 5.1. IT Provisioning Tools

These tools simulate creating user accounts, ordering hardware, and assigning software. They are essential for the `IT_Provisioning_Agent` to fulfill its role in setting up a new hire's technical environment.

**File:** `tools/it_tools.py`
```python
import json
import random
import string
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_user_account(full_name: str, role: str, department: str) -> str:
    """
    Creates a new user account in the company's directory (e.g., Active Directory).

    Args:
        full_name (str): The full name of the new hire.
        role (str): The job role of the new hire (e.g., 'Software Engineer').
        department (str): The department the new hire belongs to.

    Returns:
        str: A JSON string confirming the account creation with details.
    """
    try:
        name_parts = full_name.lower().split()
        username = name_parts[0][0] + name_parts[-1]
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        email = f"{username}@example-client-corp.com"
        
        response = {
            "status": "Success",
            "message": f"Account for {full_name} created successfully.",
            "username": username,
            "email": email,
            "temp_password_notice": "A temporary password has been securely sent to the hiring manager.",
            "creation_timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"status": "Error", "message": f"Failed to create user account: {str(e)}"})

@tool(permission=ToolPermission.ADMIN)
def order_hardware(employee_name: str, role: str) -> str:
    """
    Orders standard hardware (laptop, monitor) based on the new hire's role.

    Args:
        employee_name (str): The full name of the new hire.
        role (str): The job role, which determines the hardware kit.

    Returns:
        str: A JSON string with the order confirmation and tracking details.
    """
    # Mock logic to determine hardware based on role
    if "engineer" in role.lower() or "developer" in role.lower():
        kit = "High-Performance Laptop (16GB RAM, 512GB SSD), Dual 24-inch Monitors"
    elif "sales" in role.lower():
        kit = "Business Laptop (16GB RAM, 256GB SSD), Single 27-inch Monitor"
    else:
        kit = "Standard Business Laptop (8GB RAM, 256GB SSD), Single 24-inch Monitor"
        
    order_id = f"HW-{''.join(random.choices(string.digits, k=7))}"
    tracking_number = f"1Z{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}"
    delivery_date = (datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    response = {
        "status": "Success",
        "message": f"Hardware order placed for {employee_name}.",
        "order_id": order_id,
        "hardware_kit": kit,
        "tracking_number": tracking_number,
        "estimated_delivery": delivery_date
    }
    return json.dumps(response, indent=2)

@tool(permission=ToolPermission.ADMIN)
def assign_software_licenses(employee_name: str, role: str) -> str:
    """
    Assigns software licenses from a predefined list based on the new hire's role.

    Args:
        employee_name (str): The full name of the new hire.
        role (str): The job role, which determines the software bundle.

    Returns:
        str: A JSON string confirming which licenses were assigned.
    """
    base_licenses = ["Microsoft 365 E5", "Slack", "Zoom Pro"]
    role_specific = {
        "software engineer": ["JetBrains Ultimate Pack", "Docker Desktop", "Postman Pro"],
        "sales associate": ["Salesforce Enterprise", "LinkedIn Sales Navigator", "DocuSign"],
        "hr specialist": ["Workday HCM", "Greenhouse Recruiting"]
    }
    
    assigned_licenses = base_licenses + role_specific.get(role.lower(), ["Jira Standard"])
    
    response = {
        "status": "Success",
        "message": f"Software licenses assigned to {employee_name} for the role of {role}.",
        "assigned_licenses": assigned_licenses,
        "assignment_date": datetime.utcnow().isoformat()
    }
    return json.dumps(response, indent=2)

```

### 5.2. HR Onboarding Tools

These tools simulate critical HR functions like setting up payroll and sending benefits information. They are used by the `HR_Onboarding_Agent` to handle the administrative side of onboarding.

**File:** `tools/hr_tools.py`
```python
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def setup_payroll(employee_name: str, employee_id: str, start_date: str) -> str:
    """
    Sets up the new hire in the payroll system.

    Args:
        employee_name (str): The full name of the new hire.
        employee_id (str): The unique employee ID number.
        start_date (str): The official start date of the new hire (YYYY-MM-DD).

    Returns:
        str: A JSON string confirming payroll setup and next steps.
    """
    confirmation_id = f"PAY-{''.join(random.choices('0123456789', k=8))}"
    response = {
        "status": "Success",
        "message": f"Payroll profile for {employee_name} (ID: {employee_id}) has been created.",
        "confirmation_id": confirmation_id,
        "start_date_registered": start_date,
        "next_steps": "New hire will receive an email to complete direct deposit and tax withholding forms."
    }
    return json.dumps(response, indent=2)

@tool(permission=ToolPermission.ADMIN)
def send_benefits_enrollment_package(employee_name: str, email: str) -> str:
    """
    Sends the benefits enrollment package and instructions to the new hire's email.

    Args:
        employee_name (str): The full name of the new hire.
        email (str): The new hire's company email address.

    Returns:
        str: A JSON string confirming that the package was sent.
    """
    tracking_id = f"BEN-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))}"
    response = {
        "status": "Success",
        "message": f"Benefits enrollment package sent to {employee_name} at {email}.",
        "tracking_id": tracking_id,
        "sent_timestamp": datetime.utcnow().isoformat(),
        "enrollment_deadline_notice": "The new hire has 30 days from their start date to complete enrollment."
    }
    return json.dumps(response, indent=2)

```

### 5.3. Training Enrollment Tools

These tools simulate interactions with a Learning Management System (LMS) to find and enroll new hires in required training. They are crucial for the `Training_Enrollment_Agent`.

**File:** `tools/training_tools.py`
```python
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def get_role_based_training_plan(role: str) -> str:
    """
    Retrieves the mandatory training plan for a specific job role.

    Args:
        role (str): The job role of the new hire.

    Returns:
        str: A JSON string listing the required courses for the role.
    """
    # Mock data for training plans
    plans = {
        "software engineer": [
            {"course_id": "SEC101", "course_name": "Secure Software Development Lifecycle", "duration_hours": 8},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "GIT300", "course_name": "Advanced Git Workflow", "duration_hours": 4}
        ],
        "sales associate": [
            {"course_id": "CRM100", "course_name": "Introduction to Salesforce", "duration_hours": 16},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "SALES210", "course_name": "Consultative Selling Techniques", "duration_hours": 8}
        ],
        "default": [
            {"course_id": "HR001", "course_name": "New Hire Orientation", "duration_hours": 2},
            {"course_id": "CMP205", "course_name": "Company Code of Conduct", "duration_hours": 1},
            {"course_id": "ITSEC099", "course_name": "Cybersecurity Awareness", "duration_hours": 1.5}
        ]
    }
    
    training_plan = plans.get(role.lower(), plans["default"])
    response = {
        "role": role,
        "training_plan": training_plan
    }
    return json.dumps(response, indent=2)


@tool(permission=ToolPermission.ADMIN)
def enroll_in_course(employee_name: str, course_id: str, course_name: str) -> str:
    """
    Enrolls a new hire into a specific training course in the LMS.

    Args:
        employee_name (str): The full name of the new hire.
        course_id (str): The unique ID of the course.
        course_name (str): The name of the course.

    Returns:
        str: A JSON string confirming the enrollment.
    """
    enrollment_id = f"ENRL-{''.join(random.choices('0123456789', k=9))}"
    response = {
        "status": "Success",
        "message": f"{employee_name} has been successfully enrolled in '{course_name}'.",
        "enrollment_id": enrollment_id,
        "course_id": course_id,
        "enrollment_timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(response, indent=2)
```

## 6. Step 3: Create the Knowledge Base

The knowledge base will be used by the `HR_Onboarding_Agent` to answer policy-related questions. This demonstrates the Retrieval-Augmented Generation (RAG) pattern, where the agent retrieves information from a trusted source to formulate its answer.

**File:** `knowledge_bases/hr_policy_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: hr_policy_kb
description: >
  Contains all official company HR policies, including benefits guides, code of conduct, and remote work policies. This is the primary source for answering employee questions about company policies.
documents:
  - "mock_data/docs/Benefits_Guide_PPO.pdf"
  - "mock_data/docs/Remote_Work_Policy.pdf"
  - "mock_data/docs/Code_of_Conduct.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## 7. Step 4: Create the Agent Definitions

With the tools and knowledge base defined, we can now create the YAML definitions for our four agents. We will start with the collaborator agents and finish with the supervisor.

### 7.1. IT Provisioning Agent

This agent is a specialist focused solely on IT tasks. Its description and instructions guide it to use its tools effectively when called upon by the supervisor.

**File:** `agents/it_provisioning_agent.yaml`
```yaml
spec_version: v1
kind: native
name: IT_Provisioning_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent specializing in IT resource provisioning for new hires. It handles creating user accounts, ordering standard company hardware like laptops and monitors, and assigning necessary software licenses based on job role.
instructions: >
  You are an IT Provisioning specialist. Your tasks are transactional and precise.
  - Use the 'create_user_account' tool to set up a new network and email account.
  - Use the 'order_hardware' tool to procure the correct hardware package for the new hire's role.
  - Use the 'assign_software_licenses' tool to grant access to required applications.
  - Report the status of each action clearly and concisely, including any confirmation numbers or tracking IDs.
collaborators: []
tools:
  - create_user_account
  - order_hardware
  - assign_software_licenses
```

### 7.2. HR Onboarding Agent

This agent handles HR-related administrative tasks and uses the knowledge base to answer questions. This combination of transactional tools and RAG capability makes it a powerful HR assistant.

**File:** `agents/hr_onboarding_agent.yaml`
```yaml
spec_version: v1
kind: native
name: HR_Onboarding_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that manages Human Resources tasks for new employees. It is responsible for setting up payroll, distributing benefits enrollment information, and answering questions about company policies using the HR knowledge base.
instructions: >
  You are an HR Onboarding specialist.
  - Use the 'setup_payroll' tool to register the new hire in the payroll system.
  - Use the 'send_benefits_enrollment_package' tool to email benefits information.
  - For any questions regarding company policies, benefits, or code of conduct, you MUST use the information found in your knowledge base to provide accurate answers. Do not invent answers.
collaborators: []
tools:
  - setup_payroll
  - send_benefits_enrollment_package
knowledge_base:
  - hr_policy_kb
```

### 7.3. Training Enrollment Agent

This agent is responsible for the learning and development aspect of onboarding, ensuring new hires are set up for success with the right training.

**File:** `agents/training_enrollment_agent.yaml`
```yaml
spec_version: v1
kind: native
name: Training_Enrollment_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that manages training and development for new hires. It can identify mandatory training plans based on a new hire's role and enroll them in the required courses through the company's Learning Management System (LMS).
instructions: >
  You are a Training Enrollment coordinator.
  - First, use the 'get_role_based_training_plan' tool to determine the list of required courses for the new hire's role.
  - Then, for each course in the plan, use the 'enroll_in_course' tool to enroll the employee.
  - Confirm all enrollments with the user.
collaborators: []
tools:
  - get_role_based_training_plan
  - enroll_in_course
```

### 7.4. Onboarding Supervisor Agent

This is the central orchestrator. It does not have any tools of its own. Its sole purpose is to understand the user's request, break it down, and delegate tasks to the correct specialist collaborator agent. The `description` and `instructions` are critical for its routing logic.

**File:** `agents/onboarding_supervisor_agent.yaml`
```yaml
spec_version: v1
kind: native
name: Onboarding_Supervisor_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A supervisor agent that manages the entire new hire onboarding process. It coordinates with HR, IT, and Training agents to complete all necessary tasks for a new employee. It is the single point of contact for all onboarding requests.
instructions: >
  Your primary role is to orchestrate the new hire onboarding workflow. You do not perform tasks yourself; you delegate to your specialist collaborators.
  - When a request mentions IT, hardware, accounts, software, laptops, or access, use the IT_Provisioning_Agent.
  - When a request mentions HR, payroll, benefits, policies, or forms, use the HR_Onboarding_Agent.
  - When a request mentions training, courses, learning, or enrollment, use the Training_Enrollment_Agent.
  - For a full onboarding request, coordinate with all three agents to complete the process.
  - Provide a summary of actions taken by your collaborators to the user.
collaborators:
  - HR_Onboarding_Agent
  - IT_Provisioning_Agent
  - Training_Enrollment_Agent
tools: []
```

## 8. Step 5: Import and Deploy the Solution

Now, use the ADK Command Line Interface (CLI) to import all the components into your watsonx Orchestrate environment. The order is important: dependencies (tools, knowledge bases) must be imported before the assets that use them (agents). Collaborator agents must be imported before the supervisor that uses them.

**Execute these commands from the root of your `new-hire-onboarding-demo` directory:**

```bash
# 1. Import all Python-based tools
echo "Importing IT tools..."
orchestrate tools import -f tools/it_tools.py

echo "Importing HR tools..."
orchestrate tools import -f tools/hr_tools.py

echo "Importing Training tools..."
orchestrate tools import -f tools/training_tools.py

# 2. Import the knowledge base
echo "Importing HR knowledge base..."
orchestrate knowledge-bases import -f knowledge_bases/hr_policy_kb.yaml

# 3. Import the collaborator agents
echo "Importing HR Onboarding Agent..."
orchestrate agents import -f agents/hr_onboarding_agent.yaml

echo "Importing IT Provisioning Agent..."
orchestrate agents import -f agents/it_provisioning_agent.yaml

echo "Importing Training Enrollment Agent..."
orchestrate agents import -f agents/training_enrollment_agent.yaml

# 4. Import the supervisor agent (last)
echo "Importing Onboarding Supervisor Agent..."
orchestrate agents import -f agents/onboarding_supervisor_agent.yaml

# 5. Start the chat interface to run the demo
echo "All assets imported. Starting chat..."
orchestrate chat start
```

## 9. Step 6: Verification and Demo Scenarios

Once the chat interface is running, use the following scenarios to demonstrate the solution's capabilities. These scenarios are taken directly from the client's demo concept.

### Scenario 1: Full Onboarding Initiation

This scenario showcases the supervisor's ability to orchestrate a complex, multi-step process involving all three collaborator agents.

*   **User Prompt:** `"Start onboarding for our new Software Engineer, Priya Sharma, starting on August 1st. Her employee ID is 789456."`
*   **Expected Behavior:**
    1.  The `Onboarding_Supervisor_Agent` receives the request.
    2.  It delegates to the `IT_Provisioning_Agent`, which calls `create_user_account`, `order_hardware`, and `assign_software_licenses`.
    3.  It delegates to the `HR_Onboarding_Agent`, which calls `setup_payroll` and `send_benefits_enrollment_package`.
    4.  It delegates to the `Training_Enrollment_Agent`, which calls `get_role_based_training_plan` and then `enroll_in_course` for each required course.
    5.  The supervisor provides a comprehensive summary of all actions taken, including confirmation numbers, tracking details, and enrollment statuses.

### Scenario 2: Ad-hoc Status Check

This demonstrates the supervisor's ability to route a specific query to the correct specialist for a status update.

*   **User Prompt:** `"What is the status of Priya Sharma's hardware order?"`
*   **Expected Behavior:**
    1.  The `Onboarding_Supervisor_Agent` identifies the keyword "hardware" and routes the query to the `IT_Provisioning_Agent`.
    2.  The `IT_Provisioning_Agent` (in a more advanced implementation) would use a tool to look up the order status. In this demo, it will likely re-run the `order_hardware` tool or use its conversational ability to respond based on the previous action's output. The expected response would be similar to: "The hardware order for Priya Sharma (MacBook Pro) has tracking number XYZ123 and is expected to be delivered on July 28th."

### Scenario 3: Knowledge-Based Inquiry

This scenario highlights the RAG pattern, showing how the `HR_Onboarding_Agent` can answer questions using its trusted knowledge base.

*   **User Prompt:** `"What are the details of the PPO health plan?"`
*   **Expected Behavior:**
    1.  The `Onboarding_Supervisor_Agent` identifies the keywords "health plan" and routes the query to the `HR_Onboarding_Agent`.
    2.  The `HR_Onboarding_Agent` queries its `hr_policy_kb` knowledge base, finds relevant information from the `Benefits_Guide_PPO.pdf` document, and synthesizes a detailed, context-aware answer about the PPO plan's coverage, deductibles, and co-pays.

## 10. Troubleshooting

*   **Tool Not Found Error:** If an agent fails to import with a "tool not found" error, ensure you imported the corresponding Python tool file first and that the tool name in the agent's YAML file matches the function name in the Python code exactly.
*   **Collaborator Not Found Error:** If the supervisor agent fails to import, ensure all three collaborator agents (`HR_Onboarding_Agent`, `IT_Provisioning_Agent`, `Training_Enrollment_Agent`) were successfully imported first.
*   **Incorrect Routing:** If the supervisor delegates to the wrong agent, review the `description` and `instructions` in `onboarding_supervisor_agent.yaml`. These texts are crucial for the LLM's routing decisions. Make them more explicit if needed (e.g., "When the user explicitly asks about 'laptops', use the IT_Provisioning_Agent.").
*   **Knowledge Base Issues:** If the RAG scenario fails, verify the file paths in `hr_policy_kb.yaml` are correct relative to where you are running the `orchestrate` command. Ensure the knowledge base was imported successfully.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
