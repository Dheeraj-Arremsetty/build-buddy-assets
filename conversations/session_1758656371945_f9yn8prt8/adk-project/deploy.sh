#!/bin/bash
# Generated deployment script

# Script block 1
# Import HR tools
    orchestrate tools import -f tools/hr_tools.py
    
    # Import IT tools
    orchestrate tools import -f tools/it_tools.py
    
    # Import L&D tools
    orchestrate tools import -f tools/ld_tools.py
    ```

2.  **Import the Knowledge Base**:

    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/onboarding_kb.yaml
    ```
    You can check the import status with: `orchestrate knowledge-bases status --name onboarding_knowledge_base`

3.  **Import All Agents**:

    ```bash
    # Import collaborator agents first
    orchestrate agents import -f agents/HR_Specialist_Agent.yaml
    orchestrate agents import -f agents/IT_Support_Agent.yaml
    orchestrate agents import -f agents/LD_Coordinator_Agent.yaml
    
    # Finally, import the supervisor agent
    orchestrate agents import -f agents/Onboarding_Concierge_Agent.yaml
    ```

## Step 5: Verification and Demo Scenarios

After successful deployment, you can test the entire workflow using the `orchestrate chat` command.

