#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"

# Script block 2
orchestrate knowledge-bases import -f studio_knowledge_base.yaml

