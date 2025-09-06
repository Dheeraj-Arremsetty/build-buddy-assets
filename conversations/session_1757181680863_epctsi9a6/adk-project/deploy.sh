#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate tools import -k python -f faq_responder.py
orchestrate tools import -k python -f document_link_provider.py
orchestrate tools import -k python -f contact_info_provider.py

# Script block 2
orchestrate agents import -f xerox_support_agent.yaml

