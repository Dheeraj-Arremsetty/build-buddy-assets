#!/bin/bash
# Generated deployment script

# Script block 1
pip install --upgrade ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have access to an IBM watsonx Orchestrate environment and have logged in via the ADK CLI.
    ```bash
    orchestrate login
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## 3. Project Setup

A well-organized project structure is critical for managing the multiple artifacts (agents, tools, knowledge bases) in this demo. Create the following directory structure in your local development environment.

# Script block 2
pip install -r requirements.txt

# Script block 3
orchestrate knowledge-bases import -f ./knowledge_base/Xerox_HR_Policies.yaml

# Script block 4
# Import HR Tools
orchestrate tools import -k python -f ./tools/hr_tools.py

# Import IT Tools
orchestrate tools import -k python -f ./tools/it_tools.py

# Import Document Management Tools
orchestrate tools import -k python -f ./tools/doc_management_tools.py

# Script block 5
# Import HR Agent
orchestrate agents import -f ./agents/HR_Services_Agent.yaml

# Import IT Agent
orchestrate agents import -f ./agents/IT_Provisioning_Agent.yaml

# Import Document Management Agent
orchestrate agents import -f ./agents/Document_Management_Agent.yaml

# Script block 6
orchestrate agents import -f ./agents/Onboarding_Supervisor_Agent.yaml

# Script block 7
orchestrate chat Onboarding_Supervisor_Agent

