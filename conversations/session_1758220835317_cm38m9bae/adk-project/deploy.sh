#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"

# Script block 2
pip install pandas

# Script block 3
# Example for initializing a local developer environment
    orchestrate server start -e .env
    orchestrate env init --name local-dev --url http://127.0.0.1:8000
    orchestrate env set local-dev

# Script block 4
mkdir sp_global_demo
    cd sp_global_demo

# Script block 5
orchestrate tools import -f sp_tools.py

# Script block 6
orchestrate agents import -f sp_data_steward_agent.yaml

# Script block 7
orchestrate agents import -f emerging_market_agent.yaml

# Script block 8
orchestrate chat start --agent Emerging_Market_Opportunity_Agent

