#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Active watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This could be the SaaS version or the local Developer Edition. Activate your environment using the CLI:
    ```bash
    orchestrate login
    orchestrate env activate <your_env_name>
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing the required Python and YAML files.

## Step 1: Project Setup

First, create a structured directory to organize all the assets for the Nespresso Launchpad demo. This organization is crucial for managing the different components as the project scales.

Open your terminal and execute the following commands:

