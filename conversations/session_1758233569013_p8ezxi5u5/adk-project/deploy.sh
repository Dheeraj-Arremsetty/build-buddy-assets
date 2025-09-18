#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate

# Script block 2
orchestrate env init

# Script block 3
echo "Importing market data tools..."
orchestrate tools import -k python -f tools/market_data_tools.py

echo "Importing quantitative analysis tools..."
orchestrate tools import -k python -f tools/quantitative_analysis_tools.py

echo "Importing reporting tools..."
orchestrate tools import -k python -f tools/reporting_tools.py

# Script block 4
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/industry_reports_kb.yaml

# Script block 5
echo "Importing collaborator agents..."
orchestrate agents import -f agents/01_industry_insight_agent.yaml
orchestrate agents import -f agents/02_market_data_agent.yaml
orchestrate agents import -f agents/03_quantitative_analysis_agent.yaml

echo "Importing supervisor agent..."
orchestrate agents import -f agents/04_financial_analyst_copilot.yaml

# Script block 6
orchestrate chat start

