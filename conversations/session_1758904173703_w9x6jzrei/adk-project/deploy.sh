#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required to create the custom tools. Ensure `pip` is available for installing dependencies.
3.  **Configured Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves logging in and setting the target namespace for your assets. Use the following command to initialize and configure your environment if you haven't already:
    ```bash
    orchestrate login
    orchestrate env init
    ```
4.  **Project Directory Structure**: To maintain organization, create the following folder structure in your development environment. This plan will assume all commands are run from the `empower-demo` root directory.
    ```
    empower-demo/
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
    └── requirements.txt
    ```

## Step 1: Create Python Tools

Tools are the foundational components that perform actions. We will create two sets of Python-based tools: one for customer care (healthcare) and one for ServiceNow (IT support).

### Customer Care Tools

These tools simulate interactions with a healthcare benefits system.

#### **`get_healthcare_benefits.py`**

This tool retrieves details about different healthcare plans. It demonstrates how Orchestrate can fetch structured data from an API and present it to the user. This is valuable for employees who need to compare plan coverages for specific services or understand their financial responsibilities like deductibles and co-pays.

