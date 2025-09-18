#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate knowledgebases import -f knowledge_base/device_error_code_kb.yaml

# Script block 3
orchestrate tools import -k python -f tools/servicenow_tools.py
orchestrate tools import -k python -f tools/supply_chain_tools.py
orchestrate tools import -k python -f tools/device_monitor_tool.py

# Script block 4
# Import collaborator agents
orchestrate agents import -f agents/ServiceNow_Agent.yaml
orchestrate agents import -f agents/Supply_Chain_Agent.yaml

# Import the main supervisor agent
orchestrate agents import -f agents/MPS_Fleet_Monitor.yaml

# Script block 5
orchestrate chat start

