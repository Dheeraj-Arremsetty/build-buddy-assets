#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. If you haven't done so, run:
    ```bash
    orchestrate login
    orchestrate env init
    ```
*   **Project Structure:** A dedicated directory for the project is required. All commands and file paths in this plan assume they are run from the root of this project directory.

## 3. Project Setup and File Structure

To ensure a clean and organized build, create the following directory and file structure. This structure separates agents, tools, mock data, and knowledge base assets.

# Script block 2
# 1. Import all Python tools
echo "Importing tools..."
orchestrate tools import -f tools/sales_tool.py
orchestrate tools import -f tools/inventory_tool.py
orchestrate tools import -f tools/hr_tool.py

# 2. Import the Knowledge Base
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/starbucks_sop_kb.yaml

# 3. Import the collaborator agents
echo "Importing collaborator agents..."
orchestrate agents import -f agents/sales_analytics_agent.yaml
orchestrate agents import -f agents/inventory_management_agent.yaml
orchestrate agents import -f agents/hr_shift_coordinator_agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/store_manager_copilot.yaml

echo "Deployment complete. You can now start the chat."

# Script block 3
orchestrate chat start

