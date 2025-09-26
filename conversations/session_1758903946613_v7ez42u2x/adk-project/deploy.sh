#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Authenticated Environment**: You must be logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```
*   **Python 3.9+**: A compatible Python version is required to create custom tools.
*   **Project Directory Structure**: Create the following folder structure to organize all demo assets.

    ```
    barista-buddy-demo/
    ├── agents/
    │   ├── barista_buddy_agent.yaml
    │   ├── onboarding_knowledge_agent.yaml
    │   └── hr_actions_agent.yaml
    ├── tools/
    │   └── hr_actions.py
    ├── knowledge_base/
    │   ├── barista_employee_handbook.pdf
    │   ├── benefits_enrollment_guide.docx
    │   └── new_hire_training_schedule.csv
    │   └── onboarding_kb.yaml
    └── requirements.txt
    ```
*   **Mock Data Files**: Create the three mock documents inside the `knowledge_base/` directory. You can create empty files for now, but for a full demo, populate them with relevant synthetic data as described in the client context.

## 3. Step-by-Step Instructions

### Step 1: Create Python Tools for the HR Actions Agent

First, we will develop the custom Python tools that the `HR_Actions_Agent` will use to perform tasks. These tools simulate sending an email with a form and creating a support ticket in an IT service management system.

Create a file named `hr_actions.py` inside the `tools/` directory and add the following code.

**File: `tools/hr_actions.py`**

