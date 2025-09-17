#!/bin/bash
# Generated deployment script

# Script block 1
orchestrate knowledge-bases import -f knowledge/recipe_kb.yaml
        orchestrate knowledge-bases import -f knowledge/policy_kb.yaml
        ```
    *   **Explanation**: These commands register the knowledge bases with Orchestrate and begin the process of ingesting and indexing the associated documents. You can check the status with `orchestrate knowledge-bases status --name <kb_name>`.

2.  **Import Custom Tool**:
    *   **Command**:
        ```bash
        orchestrate tools import -f tools/recipe_tools.py
        ```
    *   **Explanation**: This command parses the Python file, identifies the function with the `@tool` decorator, and registers it as an available tool within your Orchestrate environment.

3.  **Import Collaborator Agents**:
    *   **Command**:
        ```bash
        orchestrate agents import -f agents/recipe_expert_agent.yaml
        orchestrate agents import -f agents/policy_procedures_agent.yaml
        ```
    *   **Explanation**: These commands import the specialist agents. Orchestrate will validate that their declared knowledge bases and tools (`recipe_knowledge_base`, `unit_converter_tool`, etc.) exist in the environment.

4.  **Import the Supervisor Agent**:
    *   **Command**:
        ```bash
        orchestrate agents import -f agents/supervisor_agent.yaml
        ```
    *   **Explanation**: This final agent import registers the main user-facing agent. Orchestrate validates that its declared collaborators (`Recipe_Expert_Agent`, `Policy_Procedures_Agent`) are available.

## Step 7: Verification and Demo Scenarios

Now, you can interact with your AI assistant and run the demo scenarios.

**Action:** Start the interactive chat interface.

