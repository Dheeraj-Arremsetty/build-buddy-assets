#!/bin/bash
# Generated deployment script

# Script block 1
pip install --upgrade "ibm-watsonx-orchestrate[all]"

# Script block 2
orchestrate knowledge-bases import -f ./knowledge_base/company_recipe_book_kb.yaml

# Script block 3
orchestrate tools import -f ./tools/store_procedures_tool.py

# Script block 4
# 1. Import the Recipe Expert collaborator
orchestrate agents import -f ./agents/Recipe_Expert_Agent.yaml

# 2. Import the Store Ops collaborator
orchestrate agents import -f ./agents/Store_Ops_Agent.yaml

# 3. Import the Supervisor agent
orchestrate agents import -f ./agents/Barista_Concierge_Agent.yaml

# Script block 5
orchestrate chat start --agent Barista_Concierge_Agent

