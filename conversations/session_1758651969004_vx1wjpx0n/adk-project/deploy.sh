#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"

# Script block 2
orchestrate knowledge-bases import -f knowledge_bases/company_reports_kb.yaml

# Script block 3
orchestrate tools import -k python -f tools/summarizer_tools.py

# Script block 4
orchestrate tools import -k openapi -f tools/translator_api.yaml

# Script block 5
orchestrate agents import -f agents/summarization_agent.yaml
    orchestrate agents import -f agents/translation_agent.yaml

# Script block 6
orchestrate agents import -f agents/document_orchestrator.yaml

# Script block 7
orchestrate chat start --agent Document_Orchestrator_Agent

