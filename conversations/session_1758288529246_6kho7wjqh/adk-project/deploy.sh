#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"

# Script block 2
python3 -m venv .venv
    source .venv/bin/activate

# Script block 3
orchestrate env init my_env
    orchestrate env use my_env

# Script block 4
# Navigate to the root of your project directory
cd starbucks_copilot

# Install dependencies
pip install -r requirements.txt

# 1. Import all Python tools
echo "Importing Operations tools..."
orchestrate tools import -f tools/operations_tools.py

echo "Importing HR tools..."
orchestrate tools import -f tools/hr_tools.py

echo "Importing Customer Insights tools..."
orchestrate tools import -f tools/customer_insights_tools.py

# 2. Import the Knowledge Base
echo "Importing Knowledge Base..."
orchestrate knowledge-bases import -f knowledge_base.yaml

# 3. Import the Collaborator (specialist) Agents
echo "Importing Operations Agent..."
orchestrate agents import -f agents/operations_agent.yaml

echo "Importing HR Agent..."
orchestrate agents import -f agents/hr_agent.yaml

echo "Importing Customer Insights Agent..."
orchestrate agents import -f agents/customer_insights_agent.yaml

# 4. Import the Supervisor Agent
echo "Importing Store Manager Copilot (Supervisor)..."
orchestrate agents import -f agents/store_manager_copilot.yaml

echo "All assets imported successfully."

# Script block 5
orchestrate chat start

