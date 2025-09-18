#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"

# Script block 2
# Example for initializing a new environment and activating it
    orchestrate env add
    orchestrate env activate <your_env_name>

# Script block 3
mkdir barista-buddy-demo
    cd barista-buddy-demo
    mkdir -p mock_data/recipes
    mkdir -p mock_data/procedures
    touch requirements.txt

# Script block 4
orchestrate tools import -f operations_tools.py

# Script block 5
orchestrate knowledgebases import -f recipe_kb.yaml

# Script block 6
orchestrate agents import -f recipe_expert_agent.yaml
    orchestrate agents import -f operations_support_agent.yaml

# Script block 7
orchestrate agents import -f barista_buddy_assistant.yaml

# Script block 8
orchestrate chat start

