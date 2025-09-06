#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f path_to_tool/diagnostic_questionnaire.py
orchestrate tools import -k python -f path_to_tool/solution_finder.py
orchestrate tools import -k python -f path_to_tool/escalation_tracker.py

# Script block 2
orchestrate agents import -f diagnostic_agent.yaml
orchestrate agents import -f device_knowledge_agent.yaml
orchestrate agents import -f solution_retrieval_agent.yaml
orchestrate agents import -f escalation_agent.yaml

