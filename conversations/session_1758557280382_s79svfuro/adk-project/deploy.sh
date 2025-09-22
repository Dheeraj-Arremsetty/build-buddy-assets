#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate-adk env init

# Script block 3
orchestrate knowledge-bases import -f knowledge_base/it_sop_kb.yaml

# Script block 4
orchestrate tools import -f tools/logicmonitor_tools.py
    orchestrate tools import -f tools/servicenow_tools.py

# Script block 5
orchestrate agents import -f agents/logicmonitor_observer.yaml
    orchestrate agents import -f agents/servicenow_operator.yaml

# Script block 6
orchestrate agents import -f agents/edwin_ai_orchestrator.yaml

# Script block 7
orchestrate chat start -a edwin_ai_orchestrator

