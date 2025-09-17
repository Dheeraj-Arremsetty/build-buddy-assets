# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 20:03:25
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Enterprise Process Orchestration Hub

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building the "Xerox Enterprise Process Orchestration Hub" demo using IBM watsonx Orchestrate. The plan directly addresses Xerox's strategic goal of creating a central orchestration layer for its specialized AI agents. By implementing a multi-agent system for a complex employee onboarding workflow, this demo will showcase how watsonx Orchestrate can act as a "supervisor" to intelligently coordinate tasks across different business functions (HR, IT, Document Management). This proves the platform's value in automating end-to-end enterprise processes, reducing manual effort, minimizing errors, and ultimately accelerating time-to-productivity for new employees, thereby maximizing the return on Xerox's existing AI investments. This revised plan incorporates best practices for tool development, including simulating realistic API interactions to create a more robust and representative proof of concept.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured. This is essential for the successful creation and deployment of the agents and tools outlined in this plan.

*   **Python:** A recent version of Python (3.9 or later) must be installed.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit (ADK) must be installed and configured. This is the primary tool for building, importing, and managing agents.
    ```bash
    pip install --upgrade ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have access to an IBM watsonx Orchestrate environment and have logged in via the ADK CLI.
    ```bash
    orchestrate login
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## 3. Project Setup

A well-organized project structure is critical for managing the multiple artifacts (agents, tools, knowledge bases) in this demo. Create the following directory structure in your local development environment.

```
xerox_onboarding_demo/
├── agents/
│   ├── Onboarding_Supervisor_Agent.yaml
│   ├── HR_Services_Agent.yaml
│   ├── IT_Provisioning_Agent.yaml
│   └── Document_Management_Agent.yaml
├── tools/
│   ├── hr_tools.py
│   ├── it_tools.py
│   └── doc_management_tools.py
├── knowledge_base/
│   ├── Xerox_HR_Policies.yaml
│   └── mock_data/
│       ├── Remote_Work_Policy.pdf
│       ├── IT_Acceptable_Use.pdf
│       └── Benefits_Overview.pdf
└── requirements.txt
```

**Action:** Create these folders and empty files before proceeding to the next steps. For the PDF files, create simple placeholder documents with relevant titles and a few paragraphs of text.

## 4. Step-by-Step Implementation

This section details the creation of all components of the agent architecture, from the underlying data and tools to the collaborator and supervisor agents.

### Step 4.1: Create the Knowledge Base

The `HR_Services_Agent` will use a knowledge base to answer policy questions, demonstrating the powerful Retrieval-Augmented Generation (RAG) pattern. This allows the agent to provide accurate answers based on Xerox's official documentation.

**Business Value:** This capability reduces the burden on human HR staff by providing new hires and employees with instant, accurate answers to common policy questions, ensuring consistency and compliance.

**1. Create Mock PDF Documents:**
Inside the `knowledge_base/mock_data/` directory, create three simple PDF files with some sample text: `Remote_Work_Policy.pdf`, `IT_Acceptable_Use.pdf`, and `Benefits_Overview.pdf`.

**2. Create the Knowledge Base Configuration File:**
This YAML file defines the knowledge base, names it, and points to the source documents for ingestion into the built-in Milvus vector database.

**File:** `knowledge_base/Xerox_HR_Policies.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: Xerox_HR_Policies
description: >
  Contains official Xerox HR policy documents regarding remote work, benefits eligibility, and IT acceptable use policies for all employees, including new hires.
documents:
  - "./knowledge_base/mock_data/Remote_Work_Policy.pdf"
  - "./knowledge_base/mock_data/IT_Acceptable_Use.pdf"
  - "./knowledge_base/mock_data/Benefits_Overview.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 4.2: Develop Python-Based Custom Tools

Custom tools are the foundation of agent capabilities, allowing them to interact with external systems and perform actions. We will create a suite of tools for HR, IT, and Document Management, each simulating an interaction with a corresponding Xerox system via a mock API call.

**1. Create `requirements.txt`:**
This file lists the Python packages needed for our tools to simulate API calls.
**File:** `requirements.txt`
```
requests
```

**2. Create HR Tools (`hr_tools.py`)**

This tool simulates creating a new employee record in an HRIS system like Workday. It's a critical first step in the onboarding process, as it generates a unique identifier used by downstream systems. The implementation now prepares a JSON payload and simulates a POST request, a more realistic representation of enterprise integration.

**File:** `tools/hr_tools.py`
```python
import json
import random
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="create_employee_record", description="Creates a new employee record in the HR system.")
def create_employee_record(full_name: str, title: str, start_date: str, manager: str) -> str:
    """
    Creates a new employee record in the core HR system with essential details.
    This is the first step in the official onboarding process.

    Args:
        full_name (str): The new employee's full legal name.
        title (str): The new employee's official job title.
        start_date (str): The employee's first day of work (e.g., '2024-10-01').
        manager (str): The name of the hiring manager.

    Returns:
        str: A JSON string containing a confirmation message and the newly generated unique employee ID.
    """
    try:
        # Simulate preparing a payload for an internal HRIS API
        payload = {
            "fullName": full_name,
            "jobTitle": title,
            "startDate": start_date,
            "managerName": manager,
            "action": "CREATE_PROFILE"
        }
        
        # Simulate making a POST request to the API endpoint
        # In a real scenario: response = requests.post(api_url, json=payload, headers=headers)
        
        # Generate a mock successful response from the API
        employee_id = f"XEROX-{random.randint(10000, 99999)}"
        mock_api_response = {
            "status": "success",
            "message": f"Employee record created for {full_name}.",
            "employee_id": employee_id,
            "details": payload
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        # Simulate an API error response
        error_response = {
            "status": "error",
            "message": "Failed to connect to HRIS API.",
            "details": str(e)
        }
        return json.dumps(error_response, indent=2)
```

**3. Create IT Tools (`it_tools.py`)**

These tools automate the IT provisioning process. `create_user_account` simulates creating accounts in systems like Active Directory. `provision_hardware` simulates opening a ticket in ServiceNow. Both tools now follow the pattern of creating a request payload and processing a mock API response, making them excellent templates for real-world integrations.

**File:** `tools/it_tools.py`
```python
import json
import random
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="create_user_account", description="Creates system user accounts for a new employee.")
def create_user_account(full_name: str, employee_id: str, title: str) -> str:
    """
    Creates standard user accounts (e.g., Active Directory, email, VPN) for a new employee.

    Args:
        full_name (str): The new employee's full name.
        employee_id (str): The unique employee ID from the HR system.
        title (str): The employee's job title, used to determine access groups.

    Returns:
        str: A JSON string confirming account creation and providing the new username.
    """
    try:
        # Simulate preparing a payload for the Identity Management API
        payload = {"employeeId": employee_id, "fullName": full_name, "title": title}
        
        # Generate a standard username and mock a successful API response
        parts = full_name.lower().split()
        username = parts[0][0] + parts[-1]
        mock_api_response = {
            "status": "success",
            "message": f"Core system accounts provisioned for {employee_id}.",
            "username": f"{username}@xerox.com",
            "systems_provisioned": ["Active Directory", "Microsoft 365", "VPN Access"]
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Identity API Error: {str(e)}"}, indent=2)

@tool(name="provision_hardware", description="Orders standard hardware for a new employee.")
def provision_hardware(employee_id: str, shipping_address: str) -> str:
    """
    Opens a ticket in the IT service management system to order and ship standard hardware (laptop, monitor).

    Args:
        employee_id (str): The new employee's unique ID for tracking.
        shipping_address (str): The address to ship the hardware to.

    Returns:
        str: A JSON string with the IT service ticket number and the asset tag of the provisioned hardware.
    """
    try:
        # Simulate creating a ServiceNow API request payload
        payload = {
            "requested_for_id": employee_id,
            "category": "Hardware",
            "short_description": f"New Hire Standard Hardware Kit for {employee_id}",
            "shipping_details": { "address": shipping_address }
        }
        
        # Generate mock ticket and asset IDs for the response
        ticket_id = f"IT-REQ-{random.randint(100000, 999999)}"
        asset_tag = f"XEROX-LT-{random.randint(10000, 99999)}"

        mock_api_response = {
            "status": "success",
            "message": "Hardware provisioning request submitted.",
            "ticket_id": ticket_id,
            "asset_tag": asset_tag,
            "items_ordered": ["Standard Laptop", "Docking Station", "24-inch Monitor"],
            "shipping_to": shipping_address
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"ServiceNow API Error: {str(e)}"}, indent=2)
```

**4. Create Document Management Tools (`doc_management_tools.py`)**

These tools represent Xerox's core business domain. `process_onboarding_document` simulates an intelligent document processing workflow. `archive_document` simulates moving the processed document into a secure repository. This implementation clearly demonstrates how Orchestrate can integrate with specialized, high-value microservices.

**File:** `tools/doc_management_tools.py`
```python
import json
import random
import string
import datetime
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="process_onboarding_document", description="Processes and classifies a new hire document.")
def process_onboarding_document(employee_id: str, document_type: str, document_source_url: str) -> str:
    """
    Initiates a workflow to process a new hire document, such as an offer letter or I-9 form.

    Args:
        employee_id (str): The employee ID to associate the document with.
        document_type (str): The type of document (e.g., 'Offer Letter', 'I-9 Form', 'W-4').
        document_source_url (str): A placeholder URL for the document location.

    Returns:
        str: A JSON string confirming the document has been ingested and is being processed.
    """
    try:
        # Simulate payload for a document processing microservice
        payload = {
            "employeeId": employee_id,
            "documentType": document_type,
            "sourceUrl": document_source_url
        }
        
        # Mock a response indicating the process has started
        processing_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        mock_api_response = {
            "status": "processing",
            "message": f"Document '{document_type}' for employee {employee_id} has been ingested and is now in the processing queue.",
            "processing_id": processing_id,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Document Ingestion Error: {str(e)}"}, indent=2)

@tool(name="archive_document", description="Archives a processed document into the official repository.")
def archive_document(employee_id: str, processing_id: str) -> str:
    """
    Archives a successfully processed document into the secure, long-term document repository.

    Args:
        employee_id (str): The employee ID the document belongs to.
        processing_id (str): The ID from the initial document processing step.

    Returns:
        str: A JSON string with a confirmation and the final archive location ID.
    """
    try:
        # Simulate payload for the archival service
        payload = { "employeeId": employee_id, "processingId": processing_id }
        
        # Mock a successful archival response
        archive_id = f"ARCH-{random.randint(1000000, 9999999)}"
        mock_api_response = {
            "status": "success",
            "message": f"Document with processing ID {processing_id} has been successfully archived for employee {employee_id}.",
            "archive_id": archive_id,
            "repository": "Xerox Secure Employee Archives",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        return json.dumps(mock_api_response, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Archival Service Error: {str(e)}"}, indent=2)
```

### Step 4.3: Define Collaborator Agents

Collaborator agents are specialized workers that perform specific functions. The supervisor agent will delegate tasks to them based on their described capabilities. We will use the `watsonx/ibm/granite-3-8b-instruct` model for consistency with the client's demo concept.

**1. HR Services Agent:**
This agent handles HR-specific tasks. Its description clearly states its ability to create employee records and answer policy questions, and it is equipped with the `create_employee_record` tool and the `Xerox_HR_Policies` knowledge base to fulfill these duties.

**File:** `agents/HR_Services_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: HR_Services_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent for all Human Resources tasks. It is responsible for creating and managing official employee records in the HRIS system. It can also answer questions about company policies using the Xerox HR Policies knowledge base, covering topics like remote work, benefits, and IT usage.
instructions: >
  Your purpose is to handle HR-related onboarding tasks.
  - When asked to create an employee record, use the 'create_employee_record' tool. Ensure all required information (full name, title, start date, manager) is present before calling the tool.
  - When asked questions about company policies, use the information available in your knowledge base to provide accurate and concise answers.
tools:
  - create_employee_record
knowledge_base:
  - Xerox_HR_Policies
```

**2. IT Provisioning Agent:**
This agent is responsible for all technical aspects of onboarding. Its description highlights its ability to create user accounts and provision hardware, which directly maps to the tools it possesses.

**File:** `agents/IT_Provisioning_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: IT_Provisioning_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent specializing in IT service and hardware provisioning for new employees. It handles the creation of system user accounts (email, VPN, etc.) and orchestrates the ordering and shipping of necessary hardware like laptops and monitors by interfacing with the IT service management system.
instructions: >
  You are an IT provisioning specialist.
  - Use the 'create_user_account' tool to set up a new employee's system access.
  - Use the 'provision_hardware' tool to order a standard set of equipment for a new employee. You will need a shipping address to complete this task.
tools:
  - create_user_account
  - provision_hardware
```

**3. Document Management Agent:**
This agent aligns with Xerox's core business. Its description clearly defines its role in processing and archiving new hire paperwork, making it the clear choice for the supervisor when document-related tasks arise.

**File:** `agents/Document_Management_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Document_Management_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent that manages the processing and archiving of new hire documentation, such as signed offer letters, I-9 forms, and tax forms. It aligns with Xerox's core document handling capabilities to ensure all paperwork is processed, classified, and stored in a compliant and secure manner.
instructions: >
  Your role is to manage the lifecycle of employee documents.
  - When a new document needs to be processed, use the 'process_onboarding_document' tool.
  - Once a document has been processed, use the 'archive_document' tool to move it to the official long-term repository.
tools:
  - process_onboarding_document
  - archive_document
```

### Step 4.4: Define the Supervisor Agent

The supervisor agent is the central orchestrator. It does not have tools of its own; its sole purpose is to understand the user's high-level goal, break it down into steps, and delegate those steps to the appropriate collaborator agent. The `instructions` are critical for guiding its reasoning process and have been enhanced to include a final summary step for a better user experience.

**File:** `agents/Onboarding_Supervisor_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Onboarding_Supervisor_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An enterprise supervisor agent that manages the complete employee onboarding workflow by coordinating with specialized HR, IT, and Document Management agents. It understands the end-to-end process and delegates tasks to the correct collaborator.
instructions: >
  Your primary role is to orchestrate the new hire onboarding process from start to finish. You must understand the user's request and delegate tasks to your specialized collaborators.

  Reasoning:
  - For any tasks related to creating employee records or answering questions about company policies, you MUST use the HR_Services_Agent.
  - For all tasks involving system access, user accounts, or ordering hardware (laptops, monitors), you MUST use the IT_Provisioning_Agent.
  - For processing, classifying, or archiving employee documents (like offer letters or I-9 forms), you MUST use the Document_Management_Agent.
  
  Workflow:
  1. Always start by using the HR_Services_Agent to create the employee record. This generates the essential employee ID.
  2. Once you have the employee ID, use the IT_Provisioning_Agent to create user accounts and provision hardware.
  3. Use the Document_Management_Agent for any paperwork-related tasks.
  4. Provide clear, step-by-step status updates to the user after each task is completed by a collaborator.
  5. Once all steps are complete, provide a final summary to the user confirming that the onboarding for the new employee has been fully initiated. Include the new employee ID, username, and IT ticket number.
collaborators:
  - HR_Services_Agent
  - IT_Provisioning_Agent
  - Document_Management_Agent
```

## 5. Deployment and Execution

With all artifacts created, you can now import them into your watsonx Orchestrate environment using the ADK CLI. The order of operations is important: import dependencies (knowledge bases, tools) before the components that rely on them (agents).

**Run these commands from the root of your `xerox_onboarding_demo/` directory:**

**1. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**2. Import the Knowledge Base:**
```bash
orchestrate knowledge-bases import -f ./knowledge_base/Xerox_HR_Policies.yaml
```

**3. Import All Tools:**
```bash
# Import HR Tools
orchestrate tools import -k python -f ./tools/hr_tools.py

# Import IT Tools
orchestrate tools import -k python -f ./tools/it_tools.py

# Import Document Management Tools
orchestrate tools import -k python -f ./tools/doc_management_tools.py
```

**4. Import the Collaborator Agents:**
```bash
# Import HR Agent
orchestrate agents import -f ./agents/HR_Services_Agent.yaml

# Import IT Agent
orchestrate agents import -f ./agents/IT_Provisioning_Agent.yaml

# Import Document Management Agent
orchestrate agents import -f ./agents/Document_Management_Agent.yaml
```

**5. Import the Supervisor Agent:**
```bash
orchestrate agents import -f ./agents/Onboarding_Supervisor_Agent.yaml
```

## 6. Verification and Demo Scenarios

After successfully importing all components, you can test the entire workflow using the Orchestrate chat interface.

**Start the chat with the supervisor:**
```bash
orchestrate chat Onboarding_Supervisor_Agent
```

Now, run through the planned demo scenarios:

**Scenario 1: Initiate End-to-End Onboarding**
*   **User Prompt:** `Onboard our new Solutions Architect, Jane Doe, who starts on October 1st. Her manager is John Smith. Ship her laptop to 123 Main St, Anytown, USA.`
*   **Expected Behavior:** The `Onboarding_Supervisor_Agent` will execute the workflow in sequence:
    1.  It will state that it is asking the `HR_Services_Agent` to create a record. You will see the JSON output from the `create_employee_record` tool.
    2.  It will then state it is instructing the `IT_Provisioning_Agent` to create accounts and order hardware, using the new employee ID. You will see the JSON output from both IT tools.
    3.  Finally, it will provide a comprehensive summary of the actions taken, including the new employee ID, username, and IT request number, as per its enhanced instructions.

**Scenario 2: Knowledge-Based Policy Question**
*   **User Prompt:** `What is our policy on remote work for new hires?`
*   **Expected Behavior:** The `Onboarding_Supervisor_Agent` will recognize this as an HR query. It will state that it is routing the question to the `HR_Services_Agent`. The `HR_Services_Agent` will then use its knowledge base to provide a synthesized answer based on the content of the `Remote_Work_Policy.pdf` document, likely citing its source.

## 7. Troubleshooting

*   **Error: `Agent '...' not found`:** This typically occurs if you try to import the supervisor before its collaborators. Ensure the collaborator agents are imported first. Also, check for typos between the `name` in the collaborator's YAML and the entry in the supervisor's `collaborators` list.
*   **Error: `Tool '...' not found`:** Ensure all tool scripts (`.py` files) were imported successfully using `orchestrate tools import -k python ...` before importing the agents that use them. Check the agent YAML to confirm the tool name matches the `name` attribute in the `@tool` decorator.
*   **Incorrect Delegation:** If the supervisor chooses the wrong collaborator, the issue is likely in the `instructions` of the supervisor or the `description` of the collaborators. Make the descriptions more distinct and the supervisor's reasoning instructions more explicit (e.g., "For tasks about X, you MUST use agent Y").
*   **Knowledge Base Not Working:** Use the command `orchestrate knowledge-bases status --name Xerox_HR_Policies` to check if the documents have been successfully ingested. Verify that the file paths in the `Xerox_HR_Policies.yaml` are correct relative to where you are running the command.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
