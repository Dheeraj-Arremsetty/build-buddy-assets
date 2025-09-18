#!/bin/bash
# Generated deployment script

# Script block 1
mkdir esg_intelligence_engine
    cd esg_intelligence_engine
    mkdir agents
    mkdir tools
    mkdir mock_data

# Script block 2
orchestrate knowledge-bases import -f esg_knowledge_base.yaml

# Script block 3
orchestrate tools import -f tools/esg_briefing_tool.py

# Script block 4
# Import the specialist agents
    orchestrate agents import -f agents/ESG_Report_Analyst.yaml
    orchestrate agents import -f agents/ESG_Briefing_Generator.yaml

    # Import the main supervisor agent
    orchestrate agents import -f agents/ESG_Inquiry_Supervisor.yaml

# Script block 5
orchestrate chat start

