#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves logging in and setting the target environment using the ADK CLI.
    ```bash
    # Log in to your watsonx Orchestrate environment
    orchestrate login

    # List available environments and set your target
    orchestrate env list
    orchestrate env use <your_environment_name>
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing Python, YAML, and other configuration files.

## Step 1: Project Setup and Mock Data Creation
A well-organized project structure is key. We will first create the necessary directories and the synthetic data files that our tools and knowledge base will rely on.

**Action:** Create the following directory structure in your project folder:

