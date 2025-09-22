#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate knowledge-bases import -f ./knowledge_base/company_knowledge_base.yaml

# Script block 3
orchestrate tools import -k python -f ./tools/it_support_tools.py

# Script block 4
orchestrate agents import -f ./agents/IT_Support_Agent.yaml

# Script block 5
orchestrate agents import -f ./agents/Enterprise_Assistant.yaml

# Script block 6
orchestrate chat start

