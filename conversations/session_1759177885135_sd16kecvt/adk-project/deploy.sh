#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.
5.  **watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured with the ADK. Follow the official documentation to run `orchestrate login` and set up your connection.

## Step 1: Project Setup
A well-organized project structure is crucial for managing the different components of your Orchestrate solution.

1.  Create a main directory for the demo project:
    ```bash
    mkdir wxo_enterprise_demo
    cd wxo_enterprise_demo
    ```

2.  Inside the main directory, create subdirectories for agents and tools:
    ```bash
    mkdir agents
    mkdir tools
    ```

Your project structure should now look like this:

