#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
*   **ADK Authentication:** You must be logged into your watsonx Orchestrate environment via the CLI. If you are not logged in, run:
    ```bash
    orchestrate login
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## 3. Project Setup

To maintain a clean and organized project structure, create the following directory and file layout. This structure separates agent configurations from their underlying tools, simplifying management and deployment.

1.  Create a main project folder:
    ```bash
    mkdir hr-orchestrator-demo
    cd hr-orchestrator-demo
    ```

2.  Create subdirectories for agents and tools:
    ```bash
    mkdir agents
    mkdir tools
    ```

3.  Your final project structure will look like this:
    ```
    hr-orchestrator-demo/
    ├── agents/
    │   ├── 1_onboarding_agent.yaml
    │   ├── 2_benefits_agent.yaml
    │   ├── 3_payroll_agent.yaml
    │   └── 4_employee_orchestrator.yaml
    ├── tools/
    │   ├── onboarding_tools.py
    │   ├── benefits_tools.py
    │   └── payroll_tools.py
    └── requirements.txt
    ```

## 4. Step-by-Step Instructions

This section details the creation of all components, from the foundational tools to the final supervisor agent.

### Phase 1: Tool Development (The Foundation)

First, we will create the Python tools that provide the functional capabilities for our specialized agents. Each tool simulates a real-world HR action and returns structured data.

#### 4.1 Onboarding Tools

These tools handle the initial phase of bringing a new employee into the company. They manage record creation, asset provisioning, and scheduling.

**Business Value:** Automating these initial steps ensures a consistent and efficient onboarding experience, reducing the time it takes for a new hire to become productive and minimizing the risk of manual errors in setting up critical accounts and equipment.

**Create the file `tools/onboarding_tools.py` and add the following code:**

