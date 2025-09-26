#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
    ```
*   **Python Environment**: A working Python environment (version 3.10 or higher) is required.
*   **watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This includes logging in via the CLI and initializing the environment.
    ```bash
    # Log in to your IBM Cloud account
    orchestrate login

    # Initialize your environment (follow the prompts)
    orchestrate env init
    ```
*   **watsonx.ai Account**: An account with access to watsonx.ai is necessary to power the Large Language Models (LLMs) and embedding models used by the agents. Ensure your environment is configured with the appropriate API keys.

## 3. Project Structure Setup

To keep the project organized, we will create a structured directory. This ensures that all configuration files, tools, and documents are easy to locate and manage.

1.  Create a main project folder named `barista-buddy-demo`.
2.  Inside this folder, create the following subdirectories:
    *   `agents`: To store the YAML configuration files for our three agents.
    *   `tools`: To store the Python file containing our custom tools.
    *   `knowledge_base_docs`: To store the mock PDF and TXT files for our knowledge base.

Your project structure should look like this:

