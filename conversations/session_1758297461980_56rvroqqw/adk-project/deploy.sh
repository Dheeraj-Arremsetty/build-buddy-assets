#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must be logged into an active watsonx Orchestrate environment.
    *   **For SaaS Environment**: Log in using the CLI.
        ```bash
        orchestrate login
        ```
    *   **For Developer Edition**: Start the local server. You may need to provide the path to your `.env` file.
        ```bash
        orchestrate server start -e <path-to-.env-file>
        ```
4.  **Project Directory Structure**: To maintain a clean and organized project, create the following directory structure. This separation of concerns is a best practice for managing complex agent solutions.

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

## Step 1: Create the Tools

Tools are the building blocks of an agent's capabilities, enabling it to interact with external systems and perform actions. We will create six Python-based tools, divided into `customer_care` and `service_now` categories. Each tool will generate realistic synthetic data to simulate interactions with real enterprise platforms.

### 1.1 Customer Care Tools

These tools simulate interactions with a healthcare benefits and provider system.

#### `get_healthcare_benefits.py`

**Business Value**: This tool provides immediate, on-demand access to detailed health plan information. It empowers employees to self-serve and compare benefits, reducing the number of inquiries to the HR department. For the business, this means faster resolution times and a more informed workforce.

**Technical Implementation**: The tool uses the `requests` library to call a mock API endpoint (provided in the tutorial reference material). It accepts a `Plan` type and an optional `in_network` boolean to filter the results, demonstrating how agents can handle specific user queries. The function returns a list of dictionaries containing the benefits data, which is easily parsed and presented by the agent.

