#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f path/to/station_performance_tool.py
orchestrate tools import -k python -f path/to/maintenance_predictor.py
orchestrate tools import -k python -f path/to/pricing_recommender.py
orchestrate tools import -k python -f path/to/wait_time_predictor.py
orchestrate tools import -k python -f path/to/route_suggester.py

# Script block 2
orchestrate agents import -f path/to/monitoring_agent.yaml
orchestrate agents import -f path/to/maintenance_scheduler_agent.yaml
orchestrate agents import -f path/to/pricing_strategy_agent.yaml
orchestrate agents import -f path/to/routing_notification_agent.yaml

