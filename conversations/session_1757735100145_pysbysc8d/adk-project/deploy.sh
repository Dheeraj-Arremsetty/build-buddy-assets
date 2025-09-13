#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python**: Python 3.10 or later is required.
*   **Environment Initialization**: Your ADK environment must be initialized and connected to your watsonx Orchestrate instance. This command will guide you through logging in and selecting your environment.
    ```bash
    orchestrate env init
    ```
*   **Project Directory**: A dedicated folder to organize all project files.

## 3. Project Directory Structure

To maintain a clean and manageable project, create the following directory structure. This organization separates agents, tools, knowledge bases, and mock data, aligning with ADK best practices.

