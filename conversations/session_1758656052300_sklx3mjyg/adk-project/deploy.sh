#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
touch mock_data/docs/Benefits_Guide_PPO.pdf
    touch mock_data/docs/Remote_Work_Policy.pdf
    touch mock_data/docs/Code_of_Conduct.pdf

# Script block 3
# 1. Import all Python-based tools
echo "Importing IT tools..."
orchestrate tools import -f tools/it_tools.py

echo "Importing HR tools..."
orchestrate tools import -f tools/hr_tools.py

echo "Importing Training tools..."
orchestrate tools import -f tools/training_tools.py

# 2. Import the knowledge base
echo "Importing HR knowledge base..."
orchestrate knowledge-bases import -f knowledge_bases/hr_policy_kb.yaml

# 3. Import the collaborator agents
echo "Importing HR Onboarding Agent..."
orchestrate agents import -f agents/hr_onboarding_agent.yaml

echo "Importing IT Provisioning Agent..."
orchestrate agents import -f agents/it_provisioning_agent.yaml

echo "Importing Training Enrollment Agent..."
orchestrate agents import -f agents/training_enrollment_agent.yaml

# 4. Import the supervisor agent (last)
echo "Importing Onboarding Supervisor Agent..."
orchestrate agents import -f agents/onboarding_supervisor_agent.yaml

# 5. Start the chat interface to run the demo
echo "All assets imported. Starting chat..."
orchestrate chat start

