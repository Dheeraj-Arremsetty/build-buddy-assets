# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-26 16:29:44
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy Demo

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building the "Barista Buddy," an AI-powered onboarding assistant for a coffee company client, using IBM watsonx Orchestrate. This solution directly addresses the client's need to streamline new hire onboarding by providing an intelligent, conversational interface for answering policy questions and initiating HR actions.

The plan implements the specified multi-agent architecture, featuring a **Supervisor Agent** (`Barista_Buddy_Agent`) that intelligently routes user requests to specialized **Collaborator Agents**. The `Onboarding_Knowledge_Agent` leverages a built-in Milvus knowledge base for Retrieval-Augmented Generation (RAG) to answer questions from company documents. The `HR_Actions_Agent` uses custom Python-based tools to perform transactional tasks. This approach demonstrates a powerful, scalable, and automated solution that reduces manager workload, accelerates new employee ramp-up time, and significantly improves the onboarding experience.

## 2. Prerequisites

Before starting, ensure your environment is correctly set up.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. Follow the official documentation for installation:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Authenticated Environment**: You must be logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```
*   **Python 3.9+**: A compatible Python version is required to create custom tools.
*   **Project Directory Structure**: Create the following folder structure to organize all demo assets.

    ```
    barista-buddy-demo/
    ├── agents/
    │   ├── barista_buddy_agent.yaml
    │   ├── onboarding_knowledge_agent.yaml
    │   └── hr_actions_agent.yaml
    ├── tools/
    │   └── hr_actions.py
    ├── knowledge_base/
    │   ├── barista_employee_handbook.pdf
    │   ├── benefits_enrollment_guide.docx
    │   └── new_hire_training_schedule.csv
    │   └── onboarding_kb.yaml
    └── requirements.txt
    ```
*   **Mock Data Files**: Create the three mock documents inside the `knowledge_base/` directory. You can create empty files for now, but for a full demo, populate them with relevant synthetic data as described in the client context.

## 3. Step-by-Step Instructions

### Step 1: Create Python Tools for the HR Actions Agent

First, we will develop the custom Python tools that the `HR_Actions_Agent` will use to perform tasks. These tools simulate sending an email with a form and creating a support ticket in an IT service management system.

Create a file named `hr_actions.py` inside the `tools/` directory and add the following code.

**File: `tools/hr_actions.py`**
```python
import json
import uuid
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="send_form_by_email", permission=ToolPermission.ADMIN)
def send_form_by_email(email_address: str, form_type: str) -> str:
    """
    Sends a specified HR form to an employee's email address.

    This tool is used to initiate simple HR processes by delivering the necessary
    documentation directly to the employee. It's essential for tasks like direct deposit
    setup, benefits enrollment, or tax form completion. The tool validates the email format
    and form type before simulating the email dispatch, ensuring reliable delivery of
    critical documents.

    Args:
        email_address (str): The valid email address of the employee receiving the form.
        form_type (str): The type of form to send. Supported values: 'Direct Deposit', 'W-4', 'Benefits Enrollment'.

    Returns:
        str: A JSON string confirming the action, including the form type and recipient email.
    """
    supported_forms = ['direct deposit', 'w-4', 'benefits enrollment']
    if form_type.lower() not in supported_forms:
        return json.dumps({"status": "error", "message": f"Form type '{form_type}' is not supported."})

    print(f"SIMULATING: Sending '{form_type}' form to {email_address}...")

    response = {
        "status": "success",
        "message": f"The '{form_type}' form has been successfully sent to {email_address}.",
        "timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(response)

@tool(name="create_support_ticket", permission=ToolPermission.ADMIN)
def create_support_ticket(employee_id: str, issue_description: str) -> str:
    """
    Creates a new support ticket for issues that require human intervention.

    When an employee's request cannot be fully resolved through automated actions or
    knowledge base queries, this tool escalates the issue by creating a formal support
    ticket. It captures essential details and generates a unique ticket ID, providing a clear
    audit trail and ensuring that the employee's issue is routed to the correct HR or IT support team
    for resolution.

    Args:
        employee_id (str): The unique identifier for the employee raising the issue.
        issue_description (str): A detailed description of the problem or request.

    Returns:
        str: A JSON string confirming ticket creation, including a unique ticket ID.
    """
    if not employee_id or not issue_description:
        return json.dumps({"status": "error", "message": "Employee ID and issue description are required."})
        
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    print(f"SIMULATING: Creating support ticket for Employee ID {employee_id}...")
    
    response = {
        "status": "success",
        "message": "A support ticket has been created. A team member will reach out shortly.",
        "ticket_id": ticket_id,
        "submitted_at": datetime.utcnow().isoformat()
    }
    return json.dumps(response)
```

### Step 2: Define the Knowledge Base

Next, we will define the knowledge base. This configuration tells watsonx Orchestrate to ingest the mock documents using its built-in Milvus vector database, making their content searchable for the `Onboarding_Knowledge_Agent`.

Create a file named `onboarding_kb.yaml` inside the `knowledge_base/` directory.

**File: `knowledge_base/onboarding_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: onboarding_kb
description: >
   Contains comprehensive information for new baristas, including the employee handbook,
   benefits enrollment guide, and the initial training schedule. Use this to answer
   questions about company policies, dress code, benefits plans, and training modules.
documents:
   - "knowledge_base/barista_employee_handbook.pdf"
   - "knowledge_base/benefits_enrollment_guide.docx"
   - "knowledge_base/new_hire_training_schedule.csv"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 3: Configure the Collaborator Agents

Now, we will define the two specialist collaborator agents. These agents are not directly invoked by the user but are called upon by the supervisor agent to handle specific types of tasks.

#### Onboarding Knowledge Agent
This agent is responsible for answering questions using the knowledge base we just defined.

Create a file named `onboarding_knowledge_agent.yaml` inside the `agents/` directory.

**File: `agents/onboarding_knowledge_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Onboarding_Knowledge_Agent
description: >
    A specialist agent that answers questions from new hires about company policies,
    HR information, benefits, and training schedules. It has access to a knowledge
    base containing the Barista Employee Handbook, the Benefits Enrollment Guide, and
    the New Hire Training Schedule.
instructions: >
    Your primary function is to provide accurate and detailed answers based on the
    content within your

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
