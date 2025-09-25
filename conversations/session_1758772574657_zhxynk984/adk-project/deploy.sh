#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[all]"

# Script block 2
# Initialize your environment (follow the prompts)
    orchestrate env init

    # Set your newly created environment as the active one
    orchestrate env use <your_env_name>

# Script block 3
# Ensure you are in the root 'incident_command_center' directory

# Step 5.1: Import all Python tools
echo "--- Importing Tools ---"
orchestrate tools import -f tools/triage_tools.py
orchestrate tools import -f tools/rca_tools.py
orchestrate tools import -f tools/communications_tools.py
orchestrate tools import -f tools/incident_commander_tools.py

# Step 5.2: Import the Knowledge Base
echo "--- Importing Knowledge Base ---"
orchestrate knowledge-bases import -f knowledge_bases/past_incident_reports_kb.yaml

# Step 5.3: Import the Collaborator Agents
echo "--- Importing Collaborator Agents ---"
orchestrate agents import -f agents/triage_agent.yaml
orchestrate agents import -f agents/rca_agent.yaml
orchestrate agents import -f agents/communications_agent.yaml

# Step 5.4: Import the Supervisor Agent (last)
echo "--- Importing Supervisor Agent ---"
orchestrate agents import -f agents/supervisor_agent.yaml

echo "--- All assets imported successfully! ---"

# Script block 4
orchestrate chat

