#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
    ```
3.  **watsonx Orchestrate Environment**: You must have an active IBM watsonx Orchestrate environment initialized and configured with the ADK. Ensure you have logged in and set the target environment.
4.  **Required Python Packages**: The tools in this plan require external Python libraries. You will create a `requirements.txt` file and install them to ensure the tools function correctly.
5.  **Text Editor**: A code editor such as Visual Studio Code is highly recommended for creating and editing the Python and YAML files required for this project.

## Step 1: Prepare the Project Structure and Mock Data

A well-organized project structure is essential for managing the different components of the solution and ensuring scalability.

### 1.1. Create the Directory Structure

Create the following folder structure in your development environment. This separates agents, tools, knowledge bases, and data, making the project easy to navigate and maintain.

# Script block 2
pip install -r requirements.txt

# Script block 3
cd path/to/data_steward_demo
    ```

2.  **Import All Tools**: Import the Python tools first, as the agents depend on them.
    ```bash
    orchestrate tools import -f tools/ingestion_tools.py
    orchestrate tools import -f tools/validation_tools.py
    orchestrate tools import -f tools/reporting_tools.py
    ```

3.  **Import the Knowledge Base**: Deploy the knowledge base so it can begin ingesting the document.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/data_quality_kb.yaml
    ```
    You can check its status with `orchestrate knowledge-bases status --name data_quality_kb`. Wait for it to be `Ready`.

4.  **Import the Collaborator Agents**: Import the specialized agents.
    ```bash
    orchestrate agents import -f agents/data_ingestion_agent.yaml
    orchestrate agents import -f agents/data_validation_agent.yaml
    orchestrate agents import -f agents/reporting_agent.yaml
    ```

5.  **Import the Supervisor Agent**: Finally, import the supervisor agent, which depends on all other components.
    ```bash
    orchestrate agents import -f agents/data_steward_supervisor.yaml
    ```

## Step 6: Verification and Demo Scenarios

After successful deployment, you can interact with your multi-agent system.

### 6.1. Start the Chat

Launch the interactive chat interface, specifying the `data_steward_supervisor` as the entry point.

