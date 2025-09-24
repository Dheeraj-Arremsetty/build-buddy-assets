#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -f tools/maintenance_tools.py

# Script block 2
orchestrate knowledge-bases import -f knowledge_bases/maintenance_kb.yaml
    orchestrate knowledge-bases import -f knowledge_bases/flight_ops_kb.yaml

# Script block 3
orchestrate agents import -f agents/Maintenance_Tech_Agent.yaml
    orchestrate agents import -f agents/Flight_Crew_Agent.yaml

# Script block 4
orchestrate agents import -f agents/AviationOps_Supervisor.yaml

# Script block 5
orchestrate chat start --agent AviationOps_Supervisor

