#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f fleet_health_checker.py
orchestrate tools import -k python -f maintenance_predictor.py
orchestrate tools import -k python -f order_trigger.py

# Script block 2
orchestrate agents import -f fleet_monitoring_agent.yaml
orchestrate agents import -f predictive_maintenance_agent.yaml
orchestrate agents import -f supply_chain_automation_agent.yaml

