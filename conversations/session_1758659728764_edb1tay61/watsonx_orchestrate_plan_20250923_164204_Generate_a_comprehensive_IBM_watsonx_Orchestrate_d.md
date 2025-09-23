# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 16:42:04
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered HR Employee Lifecycle Orchestrator

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building the "AI-Powered HR Employee Lifecycle Orchestrator" demo for the client. The plan directly addresses the client's need to create a unified, automated, and conversational HR process. We will construct a multi-agent system where a primary supervisor agent, the `EmployeeOrchestrator`, intelligently delegates tasks to specialized collaborator agents responsible for distinct phases of the employee journey: onboarding, benefits enrollment, and payroll setup.

This solution is designed to showcase the power of IBM watsonx Orchestrate in eliminating manual handoffs, reducing administrative errors, and significantly accelerating the end-to-end onboarding-to-payroll cycle. By following this plan, you will create a tangible Proof of Concept (POC) that demonstrates a transformative approach to HR operations, directly aligning with the client's strategic goals.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured. You will need the following tools and access:

*   **Python:** Version 3.9 or higher.
*   **pip:** Python's package installer, used to install the ADK.
*   **IBM watsonx Orchestrate Account:** An active account with access to the Agent Builder.
*   **watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured. If not installed, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **ADK Authentication:** You must be logged into your watsonx Orchestrate environment via the CLI. If you are not logged in, run:
    ```bash
    orchestrate login
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## 3. Project Setup

To maintain a clean and organized project structure, create the following directory and file layout. This structure separates agent configurations from their underlying tools, simplifying management and deployment.

1.  Create a main project folder:
    ```bash
    mkdir hr-orchestrator-demo
    cd hr-orchestrator-demo
    ```

2.  Create subdirectories for agents and tools:
    ```bash
    mkdir agents
    mkdir tools
    ```

3.  Your final project structure will look like this:
    ```
    hr-orchestrator-demo/
    ├── agents/
    │   ├── 1_onboarding_agent.yaml
    │   ├── 2_benefits_agent.yaml
    │   ├── 3_payroll_agent.yaml
    │   └── 4_employee_orchestrator.yaml
    ├── tools/
    │   ├── onboarding_tools.py
    │   ├── benefits_tools.py
    │   └── payroll_tools.py
    └── requirements.txt
    ```

## 4. Step-by-Step Instructions

This section details the creation of all components, from the foundational tools to the final supervisor agent.

### Phase 1: Tool Development (The Foundation)

First, we will create the Python tools that provide the functional capabilities for our specialized agents. Each tool simulates a real-world HR action and returns structured data.

#### 4.1 Onboarding Tools

These tools handle the initial phase of bringing a new employee into the company. They manage record creation, asset provisioning, and scheduling.

**Business Value:** Automating these initial steps ensures a consistent and efficient onboarding experience, reducing the time it takes for a new hire to become productive and minimizing the risk of manual errors in setting up critical accounts and equipment.

**Create the file `tools/onboarding_tools.py` and add the following code:**

```python
# tools/onboarding_tools.py
import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="create_new_hire_record", permission=ToolPermission.ADMIN)
def create_new_hire_record(name: str, position: str, start_date: str) -> dict:
    """
    Creates an official record for a new hire in the HR system.

    Args:
        name (str): The full name of the new employee.
        position (str): The job title or position of the new employee.
        start_date (str): The employee's official start date (e.g., 'YYYY-MM-DD').

    Returns:
        dict: A confirmation dictionary containing the new employee ID and status.
    """
    employee_id = f"EMP-{random.randint(10000, 99999)}"
    print(f"Creating record for {name}, Position: {position}, Start Date: {start_date}...")
    return {
        "status": "SUCCESS",
        "message": f"New hire record created successfully for {name}.",
        "employee_id": employee_id,
        "record_creation_timestamp": datetime.datetime.now().isoformat()
    }

@tool(name="provision_it_assets", permission=ToolPermission.ADMIN)
def provision_it_assets(employee_id: str, position: str) -> dict:
    """
    Initiates the IT asset provisioning process for a new employee.

    Args:
        employee_id (str): The unique ID of the employee.
        position (str): The job title, used to determine asset requirements (e.g., 'Software Engineer').

    Returns:
        dict: A dictionary confirming the tickets created for asset provisioning.
    """
    laptop_model = "MacBook Pro 16-inch" if "Engineer" in position else "Lenovo ThinkPad X1"
    ticket_id = f"IT-TKT-{random.randint(100000, 999999)}"
    print(f"Provisioning assets for Employee ID: {employee_id}...")
    return {
        "status": "PENDING",
        "message": "IT asset provisioning tickets have been created.",
        "employee_id": employee_id,
        "tickets": [
            {"ticket_id": ticket_id, "asset": "Laptop", "details": laptop_model, "status": "ASSIGNED"},
            {"ticket_id": f"IT-TKT-{random.randint(100000, 999999)}", "asset": "Email Account", "details": "Standard license", "status": "ASSIGNED"},
            {"ticket_id": f"IT-TKT-{random.randint(100000, 999999)}", "asset": "Software Access", "details": "Standard corporate bundle", "status": "ASSIGNED"}
        ]
    }

@tool(name="schedule_orientation_sessions", permission=ToolPermission.ADMIN)
def schedule_orientation_sessions(employee_id: str, start_date: str) -> dict:
    """
    Schedules the new hire for standard company and HR orientation sessions.

    Args:
        employee_id (str): The unique ID of the employee.
        start_date (str): The employee's start date, used as a basis for scheduling.

    Returns:
        dict: A dictionary confirming the scheduled orientation sessions.
    """
    parsed_start_date = datetime.datetime.fromisoformat(start_

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
