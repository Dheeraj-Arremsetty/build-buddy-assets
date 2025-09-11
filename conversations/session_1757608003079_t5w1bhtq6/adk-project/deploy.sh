#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate-adk"
    ```
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized and configured. This connects your local ADK to your Orchestrate instance. If you haven't done so, run:
    ```bash
    orchestrate environment init
    ```
    Follow the prompts to log in and select your environment.
*   **Project Directory**: Create a dedicated folder for this project to keep all files organized.
*   **Text Editor/IDE**: A code editor such as Visual Studio Code is recommended for editing Python and YAML files.

## Step 1: Project Structure and Dependencies Setup
A well-organized project structure is essential for managing the different components of your solution.

### 1.1. Create Project Directories
Create the following directory and file structure within your main project folder (e.g., `fincorp_demo`).

