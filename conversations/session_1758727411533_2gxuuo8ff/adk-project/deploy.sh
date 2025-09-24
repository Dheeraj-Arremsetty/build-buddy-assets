#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"

# Script block 2
# Set up your environment (follow interactive prompts)
    orchestrate env add
    
    # Set the current environment as active
    orchestrate env use <your_env_name>

# Script block 3
# 1. Import the Knowledge Bases
echo "Importing Knowledge Bases..."
orchestrate knowledge-bases import -f maintenance_kb.yaml
orchestrate knowledge-bases import -f flight_ops_kb.yaml

# 2. Import the Python Tools
echo "Importing Tools..."
orchestrate tools import -f maintenance_tools.py
orchestrate tools import -f flight_crew_tools.py

# 3. Import the Collaborator Agents
echo "Importing Collaborator Agents..."
orchestrate agents import -f maintenance_agent.yaml
orchestrate agents import -f flight_crew_agent.yaml

# 4. Import the Supervisor Agent
echo "Importing Supervisor Agent..."
orchestrate agents import -f supervisor_agent.yaml

echo "Deployment complete. You can now start the chat."

# Script block 4
orchestrate chat start --agent AeroAssist_Supervisor

