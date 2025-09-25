#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have an active IBM watsonx Orchestrate environment configured. If you have not logged in, run `orchestrate login` and follow the prompts.
*   **Text Editor:** A text editor like Visual Studio Code is recommended for creating and editing Python, YAML, and JSON files.

## 3. Step-by-Step Instructions

### Step 1: Project Setup

First, create a structured directory for all the project assets. This organization simplifies management and deployment.

Open your terminal and run the following commands:

# Script block 2
# 1. Import the Python and OpenAPI tools for the operations agent
echo "Importing tools..."
orchestrate tools import -k python -f tools/maintenance_reporter.py
orchestrate tools import -k openapi -f tools/Mock_Inventory_API.json

# 2. Import the knowledge base. This may take a few minutes as documents are ingested.
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/starbucks_kb.yaml

# 3. Import the collaborator agents (Recipe and Operations)
echo "Importing collaborator agents..."
orchestrate agents import -f agents/recipe_policy_agent.yaml
orchestrate agents import -f agents/store_operations_agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/barista_buddy_agent.yaml

echo "Deployment complete!"

