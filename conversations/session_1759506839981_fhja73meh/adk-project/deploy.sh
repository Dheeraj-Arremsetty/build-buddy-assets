#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[all]"
    ```
4.  **ADK Authentication**: You must be logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```
    Follow the prompts to authenticate your session.
5.  **Project Structure**: Create a dedicated directory for this project to keep all files organized.

    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir -p agents tools/customer_care tools/service_now knowledge_base/documents
    ```

## Step 1: Create the Tools

Tools are the foundational components that perform actions. We will create Python-based tools with realistic synthetic data to simulate interactions with backend HR and IT systems.

### 1.1 Customer Care Tools

These tools simulate interactions with a healthcare benefits system.

#### `tools/customer_care/get_healthcare_benefits.py`

This tool retrieves detailed information about various healthcare plans. It's essential for helping employees understand their coverage options, compare plans, and make informed decisions about their health benefits. By automating this data retrieval, the agent reduces the burden on HR staff and provides instant, accurate information to employees.

