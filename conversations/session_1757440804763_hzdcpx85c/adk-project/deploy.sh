#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Active Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves initializing the environment and logging in to your account. If you haven't done so, run:
    ```bash
    orchestrate login
    ```
    Follow the prompts to authenticate your session. This ensures that all agents and tools are imported into the correct tenant.
4.  **Project Directory**: Create a dedicated directory for this project to keep all configuration files and code organized. We recommend the following structure:
    ```
    /client-demo-project
    |-- /agents
    |   |-- supervisor_agent.yaml
    |   |-- data_collection_agent.yaml
    |   |-- data_processing_agent.yaml
    |   |-- insight_generation_agent.yaml
    |   |-- compliance_agent.yaml
    |   |-- reporting_agent.yaml
    |-- /tools
    |   |-- data_collection_tools.py
    |   |-- data_processing_tools.py
    |   |-- insight_generation_tools.py
    |   |-- compliance_tools.py
    |   |-- reporting_tools.py
    |-- requirements.txt
    ```

## Step 1: Define the Agent Architecture (YAML Configurations)

This step involves creating the YAML configuration files for each agent in the proposed architecture. These files define the agent's identity, behavior, instructions, and its relationships with tools and other agents.

### 1.1 Reporting Agent

The `reporting_agent` is responsible for the final step of the workflow: consolidating all processed data and generated insights into a clear, structured, and comprehensive summary report. This agent ensures that the final output is easy to understand for business stakeholders, providing a complete picture of the analysis performed.

**File:** `agents/reporting_agent.yaml`

