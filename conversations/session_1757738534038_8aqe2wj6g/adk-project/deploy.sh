#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"

# Script block 2
pip install Flask requests

# Script block 3
# Navigate to the project root directory
cd market_intelligence_orchestrator

# Start the mock API server
python mock_api/app.py

# Script block 4
orchestrate tools import -f tools/financial_tools.py
    orchestrate tools import -f tools/news_tools.py

# Script block 5
orchestrate knowledge-bases import -f knowledge_base/historical_market_events_kb.yaml

# Script block 6
orchestrate agents import -f agents/financial_data_agent.yaml
    orchestrate agents import -f agents/news_aggregator_agent.yaml
    orchestrate agents import -f agents/historical_precedent_agent.yaml

# Script block 7
orchestrate agents import -f agents/impact_assessment_supervisor_agent.yaml

# Script block 8
orchestrate chat start

