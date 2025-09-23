# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 15:45:30
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered New Hire Onboarding Concierge

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an "AI-Powered New Hire Onboarding Concierge" for the client, using IBM watsonx Orchestrate. The solution directly addresses the client's vision to automate complex, cross-functional business processes by creating a multi-agent system that orchestrates the entire new hire onboarding workflow. This plan details the creation of a supervisor agent (`Onboarding_Concierge_Agent`) that intelligently delegates tasks to specialized collaborator agents for HR, IT, and Learning & Development. The plan also incorporates a knowledge base to handle new hire inquiries, demonstrating a powerful combination of orchestration and Retrieval-Augmented Generation (RAG). By following this plan, the client will have a tangible proof-of-concept that showcases a 30-50% reduction in administrative overhead, accelerates new hire time-to-productivity, and improves the overall employee experience.

## Prerequisites

Before beginning, ensure your development environment is set up with the following components. This setup is crucial for building, deploying, and testing the agents and tools outlined in this plan.

1.  **IBM watsonx Orchestrate Account**: An active account is required to deploy and interact with the agents.
2.  **IBM watsonx Orchestrate Agent Development Kit (ADK)**: The ADK must be installed and configured. This includes the `orchestrate` CLI. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
3.  **Python Environment**: A working Python environment (version 3.9 or later) is necessary to create the custom tools.
4.  **Project Directory**: Create a root folder for the project to keep all files organized. The recommended structure is:

    ```plaintext
    onboarding_poc/
    ├── agents/
    │   ├── Onboarding_Concierge_Agent.yaml
    │   ├── HR_Specialist_Agent.yaml
    │   ├── IT_Support_Agent.yaml
    │   └── LD_Coordinator_Agent.yaml
    ├── tools/
    │   ├── hr_tools.py
    │   ├── it_tools.py
    │   └── ld_tools.py
    ├── documents/
    │   ├── Employee_Handbook.pdf
    │   ├── IT_Security_Policy.txt
    │   └── First_Week_Checklist.pdf
    ├── knowledge_bases/
    │   └── onboarding_kb.yaml
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Documents

To simulate a realistic environment, we will create mock documents for the knowledge base.

1.  **Create the `documents` directory**: `mkdir -p onboarding_poc/documents`
2.  **Create `Employee_Handbook.pdf`**: For this demo, create a simple text file and save it as a PDF with content like:
    > **Employee Handbook - Excerpt**
    > **Work-from-Home Policy:** Our company supports a flexible hybrid work model. Employees are expected to be in the office on Tuesdays and Thursdays. Specific arrangements can be made with your direct manager. All remote work must be conducted from your primary residence within the country.

3.  **Create `IT_Security_Policy.txt`**: Create a text file with this content:
    > **IT Security Policy**
    > All new employees must complete the mandatory security awareness training within their first week. Company-issued laptops come with pre-installed security software. Do not disable it. Report any suspicious emails to the IT helpdesk immediately.

4.  **Create `First_Week_Checklist.pdf`**: Create another text file and save it as a PDF:
    > **Your First Week!**
    > - Day 1: Meet your manager and team.
    > - Day 2: Set up your development environment.
    > - Day 3: Complete mandatory compliance training.
    > - Day 4: Introductory meeting with your department head.
    > - Day 5: Weekly team sync.

## Step 2: Create Python Tools

The tools provide the actions that the specialist agents will perform. Each tool is a Python function decorated with `@tool` and includes a detailed docstring that the agent uses to understand its purpose and parameters.

### 2.1. HR Specialist Tools

These tools handle employee profile creation and communication, forming the first step in the onboarding process. They ensure that the new hire is officially entered into the company's system of record.

**File:** `onboarding_poc/tools/hr_tools.py`

```python
# hr_tools.py
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_hr_profile(full_name: str, role: str, department: str, manager: str, start_date: str) -> str:
    """
    Creates a new employee profile in the core HR system (e.g., Workday).

    This tool is the first critical step in the onboarding process. It generates a unique employee ID
    and officially records the new hire's information, enabling downstream processes like payroll and benefits enrollment.

    Args:
        full_name (str): The full legal name of the new hire.
        role (str): The official job title of the new hire.
        department (str): The department the new hire will be joining.
        manager (str): The name of the new hire's direct manager.
        start_date (str): The official start date for the new hire (e.g., 'YYYY-MM-DD').

    Returns:
        str: A JSON string containing a confirmation message and the newly created employee ID.
    """
    try:
        employee_id = f"EMP{random.randint(90000, 99999)}"
        confirmation = {
            "status": "Success",
            "message": f"HR profile created for {full_name}.",
            "employee_id": employee_id,
            "details": {
                "role": role,
                "department": department,
                "manager": manager,
                "start_date": start_date
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(confirmation)
    except Exception as e:
        return json.dumps({"status": "Error", "message": str(e)})

@tool(permission=ToolPermission.ADMIN)
def send_welcome_packet(employee_id: str, full_name: str) -> str:
    """
    Sends the official digital welcome packet to the new hire.

    This tool triggers the sending of essential first-day information, company policies, and benefits
    enrollment forms. It helps create a positive first impression and ensures the new hire is well-prepared.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The full name of the new hire to personalize the communication.

    Returns:
        str: A JSON string confirming that the welcome packet has been sent.
    """
    confirmation = {
        "status": "Success",
        "message": f"Digital welcome packet sent to {full_name} (ID: {employee_id}).",
        "timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(confirmation)
```

### 2.2. IT Support Tools

These tools manage the critical provisioning of technology resources. They ensure the new hire has the necessary accounts and hardware to be productive from day one, preventing common IT-related delays.

**File:** `onboarding_poc/tools/it_tools.py`

```python
# it_tools.py
import json
import random
import requests
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# This dictionary simulates a response from a mock API endpoint
MOCK_API_RESPONSES = {
    "order_equipment": lambda pkg: {"ticket_id": f"SNOW-TKT{random.randint(700, 999)}", "package": pkg, "status": "Pending Shipment"},
    "create_accounts": lambda name: {"request_id": f"JIRA-USR{random.randint(1000, 2000)}", "username": f"{name.lower().replace(' ','.')}", "status": "Accounts Provisioning"}
}


@tool(permission=ToolPermission.ADMIN)
def create_user_accounts(employee_id: str, full_name: str) -> str:
    """
    Creates standard user accounts (Email, Slack, VPN) for a new employee.

    This tool automates the creation of essential communication and access accounts. It reduces manual
    work for the IT team and ensures the new hire can connect with colleagues and systems immediately.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The full name of the new hire, used to generate a username.

    Returns:
        str: A JSON string containing the service desk request ID and the generated username.
    """
    # In a real scenario, this would make an API call. We simulate it here.
    # response = requests.post("http://mock-it-api/create_accounts", json={"id": employee_id, "name": full_name})
    # response.raise_for_status()
    # return json.dumps(response.json())
    
    response_data = MOCK_API_RESPONSES["create_accounts"](full_name)
    return json.dumps(response_data)


@tool(permission=ToolPermission.ADMIN)
def order_equipment(employee_id: str, package_type: str) -> str:
    """
    Orders standard IT equipment (laptop, monitor) for a new employee based on their role.

    This tool streamlines hardware procurement by creating a ticket in the IT service management system (e.g., ServiceNow).
    It ensures equipment is ordered promptly based on pre-defined packages, avoiding configuration errors.

    Args:
        employee_id (str): The unique ID of the new employee.
        package_type (str): The type of equipment package (e.g., 'Standard', 'Developer').

    Returns:
        str: A JSON string with the IT service ticket number for tracking.
    """
    # In a real scenario, this would make an API call. We simulate it here.
    # response = requests.post("http://mock-it-api/order_equipment", json={"id": employee_id, "pkg": package_type})
    # response.raise_for_status()
    # return json.dumps(response.json())

    response_data = MOCK_API_RESPONSES["order_equipment"](package_type)
    return json.dumps(response_data)
```

### 2.3. Learning & Development Tools

These tools focus on integrating the new hire into the company culture and workflow. They automate scheduling and training enrollment, ensuring a structured and welcoming first week.

**File:** `onboarding_poc/tools/ld_tools.py`

```python
# ld_tools.py
import json
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def enroll_in_training(employee_id: str, role: str) -> str:
    """
    Enrolls a new hire in mandatory company and role-specific training courses.

    This tool automates a key compliance and development step. It checks the new hire's role and
    assigns them to the correct learning paths, such as 'Compliance 101' and 'Intro to Engineering Practices'.

    Args:
        employee_id (str): The unique ID of the new employee.
        role (str): The job title of the new hire to determine relevant training.

    Returns:
        str: A JSON string confirming the list of enrolled courses.
    """
    courses = ["Company Onboarding", "IT Security Awareness", "Code of Conduct"]
    if "developer" in role.lower() or "engineer" in role.lower():
        courses.append("Secure Coding Practices")
    
    confirmation = {
        "status": "Success",
        "employee_id": employee_id,
        "enrolled_courses": courses
    }
    return json.dumps(confirmation)

@tool(permission=ToolPermission.ADMIN)
def schedule_intro_meetings(employee_id: str, full_name: str, manager: str) -> str:
    """
    Schedules introductory meetings for the new hire with key team members.

    This tool facilitates team integration by automatically setting up crucial initial meetings. It simulates
    checking calendar availability to schedule a 'Welcome Lunch' and a '1-on-1 with Manager'.

    Args:
        employee_id (str): The unique ID of the new employee.
        full_name (str): The name of the new hire.
        manager (str): The name of the direct manager.

    Returns:
        str: A JSON string confirming the scheduled meetings.
    """
    today = datetime.utcnow()
    meetings = [
        {
            "title": f"Welcome Meeting: {full_name} & Team",
            "attendees": [full_name, manager, "Team DL"],
            "time": (today + timedelta(days=2)).strftime('%Y-%m-%d %H:%M UTC')
        },
        {
            "title": f"1-on-1: {full_name} & {manager}",
            "attendees": [full_name, manager],
            "time": (today + timedelta(days=3)).strftime('%Y-%m-%d %H:%M UTC')
        }
    ]
    confirmation = {
        "status": "Success",
        "employee_id": employee_id,
        "scheduled_meetings": meetings
    }
    return json.dumps(confirmation)
```

### 2.4. Create `requirements.txt`

This file lists the Python packages needed for the tools.

**File:** `onboarding_poc/requirements.txt`

```
requests
```

## Step 3: Create Knowledge Base and Agent Configurations

With the tools defined, we now configure the knowledge base and the agents using YAML files.

### 3.1. Knowledge Base Configuration

This file defines the knowledge base that the `Onboarding_Concierge_Agent` will use to answer questions.

**File:** `onboarding_poc/knowledge_bases/onboarding_kb.yaml`

```yaml
spec_version: v1
kind: knowledge_base
name: onboarding_knowledge_base
description: >
   Contains company policies, employee handbooks, and FAQs for new hires. 
   Use this to answer general questions about work-from-home policies, IT security, and first-week checklists.
documents:
   - "documents/Employee_Handbook.pdf"
   - "documents/IT_Security_Policy.txt"
   - "documents/First_Week_Checklist.pdf"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### 3.2. Agent Configurations

#### HR Specialist Agent

**File:** `onboarding_poc/agents/HR_Specialist_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: HR_Specialist_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    Specializes in Human Resources (HR) system interactions. Its primary functions are to create new employee profiles
    in the core HR system and to initiate the sending of official company welcome materials.
    This agent is the first point of contact for establishing a new hire's official presence in the company.
instructions: >
    Your purpose is to handle HR-related onboarding tasks.
    1. When asked to create a profile, use the `create_hr_profile` tool with all required information.
    2. After a profile is created, use the `send_welcome_packet` tool to send the welcome information.
    3. Only perform actions directly related to HR profile management and communication. Do not handle IT or scheduling requests.
tools:
  - create_hr_profile
  - send_welcome_packet
```

#### IT Support Agent

**File:** `onboarding_poc/agents/IT_Support_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: IT_Support_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    Manages all IT provisioning tasks for new hires. This agent is responsible for creating necessary system accounts
    (like email and Slack) and ordering standard hardware (laptops, monitors) based on the new hire's role.
    It interacts with IT service management systems to fulfill these requests.
instructions: >
    Your purpose is to provision IT resources for new employees.
    1. Use the `create_user_accounts` tool to set up standard system access.
    2. Use the `order_equipment` tool to procure hardware. Ensure you use the correct package type, such as 'Developer' for technical roles or 'Standard' for others.
    3. You only handle IT provisioning. Do not create HR profiles or schedule meetings.
tools:
  - create_user_accounts
  - order_equipment
```

#### L&D Coordinator Agent

**File:** `onboarding_poc/agents/LD_Coordinator_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: LD_Coordinator_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    Organizes all learning, development, and scheduling activities for new hires. Its responsibilities include enrolling
    the new hire in mandatory training courses and setting up introductory meetings with key team members and managers.
instructions: >
    Your purpose is to coordinate a new hire's initial training and meetings.
    1. Use the `enroll_in_training` tool to assign mandatory compliance and role-based courses.
    2. Use the `schedule_intro_meetings` tool to set up welcome meetings and manager 1-on-1s.
    3. Only handle training and scheduling tasks. Do not order hardware or create HR profiles.
tools:
  - enroll_in_training
  - schedule_intro_meetings
```

#### Onboarding Concierge (Supervisor) Agent

**File:** `onboarding_poc/agents/Onboarding_Concierge_Agent.yaml`

```yaml
spec_version: v1
kind: native
name: Onboarding_Concierge_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    A supervisor agent that orchestrates the entire new hire onboarding process. It acts as the primary point of contact,
    interprets onboarding requests, and delegates tasks to specialized HR, IT, and L&D agents. It can also answer
    general questions about company policies using its knowledge base.
instructions: >
    You are the master orchestrator for employee onboarding.
    
    Reasoning:
    - When asked to onboard a new hire, first confirm the new hire's name, role, manager, and start date.
    - Then, execute the onboarding plan in the following sequence:
    1. Use the `HR_Specialist_Agent` to create the employee's official profile and send the welcome packet.
    2. Once the HR step is complete and you have an employee ID, use the `IT_Support_Agent` to provision user accounts and order the correct equipment package.
    3. Finally, use the `LD_Coordinator_Agent` to enroll the new hire in training and schedule their introductory meetings.
    - If asked a general policy question (e.g., about work from home, IT security), use your knowledge base to find and provide the answer.
    - Provide a consolidated status update at the end of the process.
collaborators:
  - HR_Specialist_Agent
  - IT_Support_Agent
  - LD_Coordinator_Agent
knowledge_base:
  - onboarding_knowledge_base
```

## Step 4: Import and Deploy the Solution

Use the `orchestrate` CLI to import all the components into your watsonx Orchestrate environment. The order of operations is important: tools first, then knowledge bases, then collaborator agents, and finally the supervisor agent.

Execute these commands from the root of your `onboarding_poc` directory.

1.  **Import All Tools**:

    ```bash
    # Import HR tools
    orchestrate tools import -f tools/hr_tools.py
    
    # Import IT tools
    orchestrate tools import -f tools/it_tools.py
    
    # Import L&D tools
    orchestrate tools import -f tools/ld_tools.py
    ```

2.  **Import the Knowledge Base**:

    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/onboarding_kb.yaml
    ```
    You can check the import status with: `orchestrate knowledge-bases status --name onboarding_knowledge_base`

3.  **Import All Agents**:

    ```bash
    # Import collaborator agents first
    orchestrate agents import -f agents/HR_Specialist_Agent.yaml
    orchestrate agents import -f agents/IT_Support_Agent.yaml
    orchestrate agents import -f agents/LD_Coordinator_Agent.yaml
    
    # Finally, import the supervisor agent
    orchestrate agents import -f agents/Onboarding_Concierge_Agent.yaml
    ```

## Step 5: Verification and Demo Scenarios

After successful deployment, you can test the entire workflow using the `orchestrate chat` command.

```bash
orchestrate chat start --agent Onboarding_Concierge_Agent
```

### Scenario 1: End-to-End Onboarding Orchestration

**User Prompt:**
> "Onboard our new hire, Jane Doe, as a Senior Developer starting next Monday. Her manager is John Smith."

**Expected Agent Behavior:**
1.  The `Onboarding_Concierge_Agent` will acknowledge the request and confirm the plan.
2.  It will first invoke the `HR_Specialist_Agent`, which will use its tools to create a profile and send a welcome packet. You will see output like: `{"status": "Success", "message": "HR profile created for Jane Doe.", "employee_id": "EMP98765", ...}`.
3.  Next, it will invoke the `IT_Support_Agent`, passing the new employee ID. You will see output like: `{"ticket_id": "SNOW-TKT789", "package": "Developer", ...}`.
4.  Finally, it will invoke the `LD_Coordinator_Agent`. You will see output confirming training enrollment and scheduled meetings.
5.  The concierge agent will provide a final summary of all actions taken.

### Scenario 2: Mid-Process Status Inquiry

**User Prompt:**
> "What is the status of Jane Doe's onboarding?"

**Expected Agent Behavior:**
The `Onboarding_Concierge_Agent`, using its memory of the conversation, should provide a consolidated update. (Note: A true status tool would be needed for real-time checks, but for the demo, it can summarize the completed steps from the current conversation.) The response should be something like: "Jane's HR profile is complete (ID: EMP98765). Her developer laptop has been ordered (Ticket: SNOW-TKT789), and her introductory meetings are scheduled for next week."

### Scenario 3: New Hire Q&A via Knowledge Base

**User Prompt:**
> "What is the company's policy on work-from-home days?"

**Expected Agent Behavior:**
The `Onboarding_Concierge_Agent` will identify this as a general policy question. It will not delegate to any collaborator. Instead, it will query the `onboarding_knowledge_base`, find the relevant information in the `Employee_Handbook.pdf`, and synthesize an answer like: "Our company supports a flexible hybrid work model. Employees are generally expected to be in the office on Tuesdays and Thursdays, but you can make specific arrangements with your manager."

## Troubleshooting

-   **Tool Import Fails**: Ensure all Python packages in `requirements.txt` are installed in your environment (`pip install -r requirements.txt`). Check for syntax errors in the Python files.
-   **Agent Import Fails**: The most common issue is a dependency failure. Ensure all tools and collaborator agents listed in a YAML file have been successfully imported *before* importing the agent itself. Verify that the names in the `tools` and `collaborators` lists exactly match the names defined in their respective files.
-   **Knowledge Base Not Ready**: After importing, the knowledge base needs time to ingest and index documents. Use `orchestrate knowledge-bases status --name onboarding_knowledge_base` to check if the `Ready` property is `true`.
-   **Agent Doesn't Use the Right Tool/Collaborator**: This is often a prompt engineering issue. Refine the `description` and `instructions` in the agent's YAML file to be more explicit about which component to use for specific scenarios. The examples in this plan are designed to be clear and directive.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
