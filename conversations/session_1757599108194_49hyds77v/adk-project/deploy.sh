#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized and selected. This connects your local ADK to your Orchestrate instance. If not yet configured, run:
    ```bash
    # Log in to your IBM account
    orchestrate login
    
    # Select the environment where you will deploy the assets
    orchestrate env select
    ```
4.  **Required Python Libraries**: The tools we will build depend on the `pandas` library for data manipulation. We will create a `requirements.txt` file and install it to manage dependencies effectively.

## Step 1: Project Setup and Mock Data Creation

First, we will establish a clean project structure and create the synthetic data files that our tools will use to simulate real-world systems. This approach allows for a robust and realistic demonstration without needing direct integration with the client's backend systems, a key aspect of a successful Proof of Concept.

**1. Create the Directory Structure:**

Open your terminal and create the following directories. This organization separates our agents, tools, knowledge base definitions, and mock data for clarity, maintainability, and adherence to best practices.

# Script block 2
# 1. Install Python dependencies from the requirements file
pip install -r requirements.txt

# 2. Import all tools for the collaborator agents. The ADK will register these tools
# and make them available for agents to use.
echo "Importing tools..."
orchestrate tools import -f ./tools/store_data_tools.py
orchestrate tools import -f ./tools/partner_support_tools.py

# 3. Import the knowledge base. This command uploads the documents and starts the
# ingestion process in the background.
echo "Importing knowledge base... this may take a few minutes for ingestion."
orchestrate knowledge-bases import -f ./kbs/store_operations_kb.yaml

# 4. Check the knowledge base status to ensure it's ready. Ingestion can take
# a few minutes. You may need to run this command a few times until the status is "Ready: True".
echo "Checking knowledge base status..."
orchestrate knowledge-bases status --name Store_Operations_KB

# 5. Import the collaborator agents. These must be imported before the supervisor
# so that the supervisor can find them when it is imported.
echo "Importing collaborator agents..."
orchestrate agents import -f ./agents/store_data_agent.yaml
orchestrate agents import -f ./agents/partner_support_agent.yaml

# 6. Import the main supervisor agent. This agent links to the collaborators.
echo "Importing supervisor agent..."
orchestrate agents import -f ./agents/partner_ops_assistant_agent.yaml

echo "Deployment complete! All agents, tools, and knowledge bases are now available."

# Script block 3
orchestrate chat start

