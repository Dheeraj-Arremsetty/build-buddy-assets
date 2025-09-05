#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f doc_search_tool.py
orchestrate tools import -k python -f policy_checker_tool.py
orchestrate tools import -k python -f troubleshoot_tool.py
orchestrate tools import -k python -f query_router.py

# Script block 2
orchestrate agents import -f documentation_retrieval_agent.yaml
orchestrate agents import -f policy_compliance_agent.yaml
orchestrate agents import -f troubleshooting_agent.yaml
orchestrate agents import -f query_routing_agent.yaml

