#!/bin/bash
# Generated deployment script

# Script block 1
pip install --upgrade ibm-watsonx-orchestrate
    ```
2.  **Authenticated Environment**: You must be logged into your watsonx Orchestrate instance and have an active development environment.
    ```bash
    # Log in to your watsonx Orchestrate instance
    orchestrate login

    # List available environments
    orchestrate env list

    # Activate your development environment (replace <your_env_name>)
    orchestrate env activate <your_env_name>
    ```
3.  **Project Directory Structure**: Create a dedicated folder for this project with a structured layout to organize your files. This is crucial for managing the different components.
    ```bash
    mkdir empower_demo
    cd empower_demo
    mkdir agents
    mkdir tools
    mkdir tools/servicenow
    mkdir tools/customercare
    mkdir knowledge_docs
    ```
4.  **Python Environment**: A working Python 3.9+ environment is required. Create a `requirements.txt` file in the root `empower_demo` directory to manage dependencies.
    ```text
    # empower_demo/requirements.txt
    requests
    pydantic
    ```
    Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Step 1: Create the Tools for Collaborator Agents

Tools are the building blocks that allow agents to perform actions. We will create Python-based tools that generate realistic, synthetic data to simulate interactions with backend systems like ServiceNow and a healthcare benefits portal.

### 1.1. Customer Care Tools

These tools simulate fetching data related to healthcare benefits, claims, and providers.

**File: `tools/customercare/benefits_tools.py`**
This file contains tools for getting plan benefits and checking claim status. The `get_healthcare_benefits` tool provides a detailed breakdown of different insurance plans, allowing employees to compare options. The `get_my_claims` tool generates a realistic list of medical claims, giving employees immediate insight into their status and financial details, reducing calls to the benefits hotline.

