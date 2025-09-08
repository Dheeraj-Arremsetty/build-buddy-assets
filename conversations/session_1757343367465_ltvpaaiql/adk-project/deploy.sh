#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f faq_responder.py
orchestrate tools import -k python -f order_status_checker.py
orchestrate tools import -k python -f support_ticket_creator.py
orchestrate tools import -k python -f product_info_provider.py

# Script block 2
orchestrate agents import -f master_template_agent.yaml
orchestrate agents import -f customization_agent.yaml
orchestrate agents import -f escalation_agent.yaml

