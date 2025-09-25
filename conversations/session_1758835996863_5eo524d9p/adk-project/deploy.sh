#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate-adk
    ```
2.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized. This connects your local ADK to your Orchestrate instance. If you haven't already, run:
    ```bash
    orchestrate login
    orchestrate env init
    ```
3.  **Python 3.9+**: A modern version of Python is required to create the custom tools.
4.  **Project Structure**: Create the following directory structure to organize your files. This plan will assume this structure is in place.

    ```
    empower_demo/
    ├── agents/
    │   ├── customer_care_agent.yaml
    │   ├── service_now_agent.yaml
    │   └── empower_agent.yaml
    ├── tools/
    │   ├── customer_care/
    │   │   ├── get_healthcare_benefits.py
    │   │   ├── get_my_claims.py
    │   │   └── search_healthcare_providers.py
    │   └── service_now/
    │       ├── create_service_now_incident.py
    │       ├── get_my_service_now_incidents.py
    │       └── get_service_now_incident_by_number.py
    ├── knowledge_base/
    │   ├── empower_kb.yaml
    │   └── documents/
    │       └── employee_faq.txt
    └── requirements.txt
    ```

## Step 1: Create the Python Tools

Tools are the building blocks of an agent's capabilities, allowing it to interact with systems and perform actions. We will create six distinct tools, divided into two domains: Customer Care (for HR/benefits) and ServiceNow (for IT support). Each tool will generate realistic synthetic data to simulate interactions with live enterprise systems.

### 1.1 Customer Care Tools

These tools simulate interactions with a healthcare benefits and provider system.

#### `get_healthcare_benefits.py`

**Business Value**: This tool provides immediate, on-demand access to detailed health plan information. It eliminates the need for employees to search through complex documents or contact HR for common questions, thereby improving employee self-service and reducing the burden on HR staff. It empowers employees to make informed decisions about their healthcare.

**Technical Implementation**: The Python function uses the `@tool` decorator to register it with Orchestrate. It takes a health plan type as input and returns a structured list of dictionaries containing benefits information. We use the `requests` library to simulate fetching data from an external API endpoint.

