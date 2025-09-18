#!/bin/bash
# Generated deployment script

# Script block 1
mkdir financial_insights_demo
cd financial_insights_demo
mkdir agents tools kb mock_data

# Script block 2
orchestrate knowledge-bases import -f kb/semiconductor_kb.yaml

# Script block 3
# Import Python-based tools
orchestrate tools import -f tools/ingestion_tools.py
orchestrate tools import -f tools/nlp_tools.py

# Import OpenAPI-based tools
orchestrate tools import -f tools/datalinker_api.yaml

# Script block 4
# Import collaborator agents
orchestrate agents import -f agents/DocumentIngestionAgent.yaml
orchestrate agents import -f agents/NLPAnalysisAgent.yaml
orchestrate agents import -f agents/DataLinkerAgent.yaml

# Import the supervisor agent
orchestrate agents import -f agents/FinancialSupervisorAgent.yaml

# Script block 5
orchestrate chat start

