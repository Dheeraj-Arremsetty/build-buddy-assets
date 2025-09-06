#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f nlp_processor.py
orchestrate tools import -k python -f multi_source_query_tool.py
orchestrate tools import -k python -f chart_generator.py

# Script block 2
orchestrate agents import -f query_understanding_agent.yaml
orchestrate agents import -f data_retrieval_agent.yaml
orchestrate agents import -f visualization_agent.yaml

