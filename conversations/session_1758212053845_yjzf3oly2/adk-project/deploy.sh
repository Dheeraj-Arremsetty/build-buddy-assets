#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate env init

# Script block 3
orchestrate tools import -k python -f tools/reporting_tools.py

# Script block 4
orchestrate knowledge_bases import -f knowledge_base/sec_filings_kb.yaml

# Script block 5
orchestrate agents import -f agents/Filing_Analysis_Agent.yaml
    orchestrate agents import -f agents/Risk_Reporting_Agent.yaml

# Script block 6
orchestrate agents import -f agents/SEC_Risk_Orchestrator_Agent.yaml

# Script block 7
orchestrate chat start

