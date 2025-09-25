# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-25 16:22:06
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Comprehensive Demo Execution Plan

## Overview

This execution plan provides a detailed, step-by-step guide for creating a comprehensive IBM watsonx Orchestrate demonstration tailored for a client focused on enhancing internal operations. The plan implements a realistic and powerful **"Employee Success & IT Support"** scenario, designed to showcase the full capabilities of watsonx Orchestrate in a relatable enterprise environment.

The demo features a multi-agent architecture with a primary supervisor agent, **`empower_agent`**, acting as a single, intelligent point of contact for employees. This agent will delegate tasks to two specialized collaborator agents: **`customer_care_agent`** for handling HR and healthcare-related queries, and **`service_now_agent`** for managing IT support incidents. Furthermore, the `empower_agent` will leverage a **Knowledge Base** containing company policy documents to provide direct, accurate answers using Retrieval-Augmented Generation (RAG), creating a seamless and efficient employee experience.

## Prerequisites

Before beginning, ensure your environment is properly configured.

1.  **Python Environment**: A working installation of Python (3.9 or higher) and `pip` is required.
2.  **watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Active Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. Verify your setup by running:
    ```bash
    orchestrate env show
    ```
4.  **Required Python Packages**: The custom tools in this demo rely on external packages. A `requirements.txt` file will be created to manage these dependencies.
5.  **Text Editor**: A text editor or IDE (like Visual Studio Code) is needed to create and edit Python and YAML files.

## Step 1: Project Setup

First, create a structured directory for all the demo assets. This organization is crucial for managing agents, tools, and knowledge base documents effectively.

1.  Open your terminal or command prompt.
2.  Create the main project directory and navigate into it.

    ```bash
    mkdir empower-demo
    cd empower-demo
    ```

3.  Create the necessary subdirectories for agents, tools, and knowledge base documents.

    ```bash
    mkdir agents tools knowledge_base_docs
    mkdir tools/customer_care tools/service_now
    ```

4.  Create placeholder documents for the knowledge base. These files will be ingested by Orchestrate to answer policy-related questions.

    ```bash
    # Create a dummy employee handbook
    echo "Our company offers tuition reimbursement up to $5,000 per year for approved courses. To be eligible, employees must be full-time and have completed at least one year of service. All courses must be related to the employee's current role or a potential future role within the company. Approval from the employee's manager is required before enrollment." > knowledge_base_docs/Employee_Handbook.txt

    # Create a dummy IT policy document (can be any format like .pdf, .txt, .docx)
    echo "To reset your password, please open a high-priority ticket with the IT department using the 'create ticket' command. For urgent system-wide outages, please contact the IT helpdesk directly via phone." > knowledge_base_docs/IT_Policy.txt
    ```

5.  Create a `requirements.txt` file to list the Python dependencies for our custom tools.

    ```bash
    touch requirements.txt
    ```
    Open `requirements.txt` and add the following packages:
    ```text
    requests
    pydantic
    ```
6.  Install the dependencies from the project's root directory.
    ```bash
    pip install -r requirements.txt
    ```

Your project structure should now look like this:

```
empower-demo/
├── agents/
├── knowledge_base_docs/
│   ├── Employee_Handbook.txt
│   └── IT_Policy.txt
├── tools/
│   ├── customer_care/
│   └── service_now/
└── requirements.txt
```

## Step 2: Create the Custom Tools

Tools are the functional building blocks that allow agents to perform actions. We will create two sets of Python-based tools: one for IT support (ServiceNow) and one for HR/Customer Care. Each tool will generate realistic synthetic data to simulate real-world API interactions.

### ServiceNow Tools

These tools simulate interactions with an IT service management platform like ServiceNow, handling incident creation and retrieval.

#### 1. Create Service Now Incident Tool
**Business Value:** This tool automates the creation of IT support tickets directly from the chat interface, reducing manual effort for employees and ensuring incidents are logged with the correct initial information. It streamlines the support process and improves response times.

**File:** `tools/service_now/create_service_now_incident.py`
```python
# tools/service_now/create_service_now_incident.py
import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field
from enum import Enum

class Urgency(str, Enum):
    HIGH = '1 - High'
    MEDIUM = '2 - Medium'
    LOW = '3 - Low'

@tool(permission=ToolPermission.ADMIN)
def create_service_now_incident(short_description: str, urgency: Urgency = Urgency.LOW) -> dict:
    """
    Creates a new incident in ServiceNow for IT support.

    Args:
        short_description (str): A brief summary of the user's issue.
        urgency (Urgency, optional): The urgency of the ticket. Can be one of "1 - High", "2 - Medium", or "3 - Low". Defaults to "3 - Low".

    Returns:
        dict: A dictionary containing the details of the newly created incident, including the incident number and status.
    """
    incident_number = f"INC{random.randint(1000000, 9999999)}"
    created_time = datetime.datetime.now().isoformat()

    return {
        "incident_number": incident_number,
        "status": "New",
        "short_description": short_description,
        "urgency": urgency.value,
        "created_at": created_time,
        "confirmation": f"Successfully created incident {incident_number}."
    }
```

#### 2. Get My Service Now Incidents Tool
**Business Value:** This tool empowers employees with self-service capabilities to check the status of their open IT tickets without needing to contact the helpdesk. This increases transparency and reduces the support team's workload from handling status inquiries.

**File:** `tools/service_now/get_my_service_now_incidents.py`
```python
# tools/service_now/get_my_service_now_incidents.py
import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def get_my_service_now_incidents() -> list[dict]:
    """
    Retrieves a list of all open ServiceNow incidents for the current user.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents an open IT incident.
    """
    incidents = [
        {
            "incident_number": f"INC{random.randint(1000000, 9999999)}",
            "status": "In Progress",
            "short_description": "Cannot access shared drive",
            "urgency": "2 - Medium",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
        },
        {
            "incident_number": f"INC{random.randint(1000000, 9999999)}",
            "status": "On Hold",
            "short_description": "New monitor request",
            "urgency": "3 - Low",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat()
        }
    ]
    return incidents
```

#### 3. Get Service Now Incident by Number Tool

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
