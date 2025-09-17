#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
    ```
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured and logged in via the ADK CLI. To initialize and log in, use:
    ```bash
    orchestrate login -s <environment>
    ```
*   **Text Editor/IDE**: A code editor such as Visual Studio Code is recommended for creating and editing YAML and Python files.
*   **Project Directory**: Create a dedicated folder for this project to keep all files organized.

## 3. Step 1: Project Setup and Mock Data Creation

A well-organized project structure is crucial for managing the different components of our multi-agent system. This step involves creating the necessary directories, the synthetic data files that will fuel our demo scenarios, and a `requirements.txt` file for environment reproducibility.

First, create the following directory structure within your main project folder:

# Script block 2
orchestrate knowledge-bases import -f knowledge-bases/xerox_legal_policy_kb.yaml

# Script block 3
# 1. Import all tools for the specialist agents
echo "Importing tools..."
orchestrate tools import -f tools/document_generator/create_contract_draft.py
orchestrate tools import -f tools/approval_router/approval_api.openapi.json

# 2. Import the specialist collaborator agents (Knowledge Base was already imported in Step 2)
echo "Importing specialist agents..."
orchestrate agents import -f agents/Document_Generation_Agent.yaml
orchestrate agents import -f agents/Compliance_Check_Agent.yaml
orchestrate agents import -f agents/Approval_Routing_Agent.yaml

# 3. Import the master Supervisor Agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/Xerox_Workflow_Supervisor.yaml

echo "Deployment complete! You can now test the supervisor agent."

