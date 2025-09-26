#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate-adk
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This could be a cloud instance or the local Developer Edition. Ensure you have initialized your environment using the CLI:
    ```bash
    orchestrate environment init
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing the Python (`.py`) and YAML (`.yaml`) files.

## Step 1: Project Setup
First, we'll create a structured directory for our project. This organization helps in managing agents, tools, and dependencies cleanly.

1.  Create a main project folder named `financial_compliance_demo`.
2.  Inside `financial_compliance_demo`, create two subdirectories: `agents` and `tools`.

Your project structure should look like this:

