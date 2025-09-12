#!/bin/bash
# Generated deployment script

# Script block 1
pip install --upgrade ibm-watsonx-orchestrate
    ```
*   **Python**: Python 3.9 or higher is required.
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. Initialize it using the CLI if you haven't already.
    ```bash
    # Log in to your IBM Cloud account
    ibmcloud login
    # Initialize your Orchestrate environment
    orchestrate environment init
    ```
*   **Required Python Libraries**: Create a `requirements.txt` file in your project's root directory with the following content. These libraries are used by the custom tools.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
    Install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
*   **Project Structure**: Create the following directory structure to organize your assets. This structure is critical for the import commands to work correctly.
    ```
    innovatehealth-demo/
    ├── agents/
    │   ├── 01_service_now_agent.yaml
    │   ├── 02_customer_care_agent.yaml
    │   ├── 03_hr_agent.yaml
    │   └── 04_innovate_health_assistant.yaml
    ├── tools/
    │   ├── customer_care/
    │   │   ├── get_healthcare_benefits.py
    │   │   ├── get_my_claims.py
    │   │   └── search_healthcare_providers.py
    │   └── service_now/
    │       ├── create_service_now_incident.py
    │       └── get_my_service_now_incidents.py
    ├── knowledge_base/
    │   └── hr_policy_kb.yaml
    ├── knowledge_base_docs/
    │   ├── tuition_reimbursement.txt
    │   └── employee_handbook.txt
    └── requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Create Mock Knowledge Base Documents

First, we will create simple text files that will be ingested into a knowledge base. This knowledge base will be used by the `hr_agent` to provide accurate, document-grounded answers to employee questions about company policies, demonstrating the powerful RAG (Retrieval-Augmented Generation) capabilities of watsonx Orchestrate.

**File: `knowledge_base_docs/tuition_reimbursement.txt`**

