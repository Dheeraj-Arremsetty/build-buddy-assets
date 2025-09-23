#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"

# Script block 2
pip install Flask requests

# Script block 3
python mock_sap_api.py

# Script block 4
orchestrate knowledge-bases import -f knowledge_base/vendor_policy_kb.yaml

# Script block 5
orchestrate tools import -k python -f tools/invoice_tools.py

# Script block 6
orchestrate agents import -f agents/invoice_automation_agent.yaml

# Script block 7
orchestrate chat start

