#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"

# Script block 2
mkdir -p market_intelligence_poc/{agents,tools,knowledge_bases,documents}
    cd market_intelligence_poc

# Script block 3
pip install -r tools/requirements.txt

# Script block 4
orchestrate tools import -k python -f tools/market_tools.py

# Script block 5
orchestrate knowledge-bases import -f knowledge_bases/internal_analyst_briefs.yaml

# Script block 6
orchestrate agents import -f agents/news_harvester_agent.yaml
    orchestrate agents import -f agents/market_data_agent.yaml

# Script block 7
orchestrate agents import -f agents/market_insight_agent.yaml

# Script block 8
orchestrate chat start

