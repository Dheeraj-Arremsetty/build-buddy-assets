#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate login

# Script block 3
mkdir corepower-yoga-demo
cd corepower-yoga-demo
mkdir agents tools mock_data

# Script block 4
orchestrate knowledge-bases import -f corepower_kb.yaml

# Script block 5
orchestrate tools import -k python -f tools/account_tools.py
    orchestrate tools import -k python -f tools/scheduler_tools.py

# Script block 6
orchestrate agents import -f agents/membership_policy_agent.yaml
    orchestrate agents import -f agents/account_management_agent.yaml
    orchestrate agents import -f agents/class_scheduler_agent.yaml

# Script block 7
orchestrate agents import -f agents/corepower_member_concierge.yaml

# Script block 8
orchestrate chat start --agent CorePower_Member_Concierge

