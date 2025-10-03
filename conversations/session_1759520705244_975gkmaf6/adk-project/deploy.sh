#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.10 or later) is required.
3.  **Orchestrate CLI Login**: You must be logged into your watsonx Orchestrate environment via the CLI. If you haven't already, run:
    ```bash
    orchestrate login
    ```
4.  **Project Directory**: Create a dedicated directory for this project to keep all files organized.
    ```bash
    mkdir finsecure_demo
    cd finsecure_demo
    mkdir -p agents tools knowledge_base_docs
    ```

## Step 1: Create the Knowledge Base for Regulatory Guidelines

To ensure all analysis is grounded in current regulations, we will create a knowledge base. This allows the `risk_analysis_agent` to query internal policies and external regulatory documents to validate compliance checks, providing grounded, auditable answers.

First, we'll create a mock regulatory document.

**1.1. Create a Mock Document**

Create a file named `aml_policy_v1.txt` inside the `knowledge_base_docs/` directory.

`knowledge_base_docs/aml_policy_v1.txt`:

# Script block 2
orchestrate knowledge-bases import -f regulatory_kb.yaml

