#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"

# Script block 2
orchestrate login

# Script block 3
# Navigate to the root of your project directory
cd /path/to/xerox-it-demo

# Step 1: Import all Python-based tools
echo "Importing User Access tools..."
orchestrate tools import -f tools/user_access_tools.py

echo "Importing Software Provisioning tools..."
orchestrate tools import -f tools/software_provisioning_tools.py

# Step 2: Import the knowledge base
echo "Importing Network Troubleshooting knowledge base..."
orchestrate knowledge-bases import -f knowledge_bases/network_kb.yaml

# Step 3: Import the collaborator agents (these must exist before the supervisor)
echo "Importing Network Troubleshooter agent..."
orchestrate agents import -f agents/network_troubleshooter_agent.yaml

echo "Importing Software Provisioning agent..."
orchestrate agents import -f agents/software_provisioning_agent.yaml

echo "Importing User Access agent..."
orchestrate agents import -f agents/user_access_agent.yaml

# Step 4: Import the supervisor agent last
echo "Importing IT Help Desk Supervisor agent..."
orchestrate agents import -f agents/it_help_desk_supervisor.yaml

# Step 5: Start the interactive chat to begin the demo
echo "All assets imported. Starting chat with the Supervisor agent..."
orchestrate chat start --agent IT_Help_Desk_Supervisor

