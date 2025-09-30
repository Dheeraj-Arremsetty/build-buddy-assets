# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-30 15:45:53
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered New Hire Onboarding Assistant

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building a powerful **AI-Powered New Hire Onboarding Assistant** for the client using IBM watsonx Orchestrate. The solution is designed to address the client's need to streamline and personalize the new hire experience, reducing manual effort for HR and IT teams while providing a seamless journey for new employees.

The demo will showcase a sophisticated multi-agent architecture where a central **Onboarding Supervisor Agent** orchestrates tasks by delegating to specialized agents for HR Information Systems (HRIS), IT Provisioning, and Company Policy inquiries. This approach demonstrates watsonx Orchestrate's core capabilities in complex task decomposition, tool usage, knowledge base retrieval, and inter-agent collaboration, providing a tangible proof-of-concept for automating complex, multi-departmental business processes.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured. This is crucial for the successful creation and deployment of the agents and tools.

*   **Python:** Ensure Python 3.9 or higher is installed on your system.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit is the primary tool for this build. Install it using pip:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate Environment:** You must have an active IBM watsonx Orchestrate environment configured. Initialize your environment and log in using the ADK CLI.
    ```bash
    # Initialize your environment (follow prompts)
    orchestrate env init

    # Log in to your environment
    orchestrate login
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code is recommended for creating and editing the necessary Python and YAML files.
*   **Project Directory Structure:** Create a dedicated folder for this project to keep all assets organized.

    ```bash
    mkdir onboarding_poc
    cd onboarding_poc
    mkdir agents tools knowledge_docs
    ```

## 3. Step-by-Step Instructions

### Step 1: Create the Knowledge Base and Documents

The first step is to create the information source for our policy agent. We will create a knowledge base that ingests plain text documents containing company policies.

**Business Value:** This component provides new hires with instant, accurate answers to common policy questions, reducing the burden on HR staff and empowering employees to find information independently.

1.  **Create Mock Policy Documents:** Inside the `knowledge_docs` directory, create the following text files with sample content.

    *   `knowledge_docs/pto_policy.txt`:
        ```text
        Company Paid Time Off (PTO) Policy:
        All full-time employees are entitled to 20 days of PTO per year, accrued on a bi-weekly basis. PTO can be used for vacation, personal days, or sick leave. New hires begin accruing PTO from their start date. Requests for PTO should be submitted through the HRIS portal at least two weeks in advance, where possible.
        ```
    *   `knowledge_docs/remote_work_policy.txt`:
        ```text
        Company Remote Work Policy:
        Our company supports a hybrid work model. Employees can work remotely up to three days per week, with manager approval. The company will provide standard IT equipment, including a laptop and monitor. Employees are responsible for ensuring they have a secure and reliable internet connection. All company data security protocols must be followed when working remotely.
        ```

2.  **Define the Knowledge Base YAML:** Create a file named `policy_kb.yaml` in the root of your `onboarding_poc` directory.

    **File: `policy_kb.yaml`**
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: policy_kb
    description: >
      Contains official company documents regarding employee policies, including Paid Time Off (PTO), remote work guidelines, and code of conduct. Use this to answer specific questions from new hires about company rules and benefits.
    documents:
      - "knowledge_docs/pto_policy.txt"
      - "knowledge_docs/remote_work_policy.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 2: Create the Python Tools

Next, we will develop the Python-based tools that our HR and IT agents will use to perform actions. These tools will simulate interactions with real enterprise systems by using realistic synthetic data.

#### A. HRIS Tools

**Business Value:** These tools automate the retrieval and management of employee data, ensuring consistency and reducing the risk of manual data entry errors. They form the backbone of the HR onboarding process.

**Technical Implementation:** The `hris_tools.py` file contains three functions decorated with `@tool`. Each function simulates an HRIS action: fetching new hire data, checking their onboarding task status, and updating their profile. The data is hardcoded for demo purposes but structured to mimic a real API response.

Create the file `tools/hris_tools.py`:

**File: `tools/hris_tools.py`**
```python
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock database of new hires
MOCK_NEW_HIRES = {
    "alex ray": {
        "employee_id": "AR78901",
        "full_name": "Alex Ray",
        "role": "Software Engineer",
        "department": "Technology",
        "start_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "manager": "Dana Scully"
    },
    "jane doe": {
        "employee_id": "JD12345",
        "full_name": "Jane Doe",
        "role": "Marketing Specialist",
        "department": "Marketing",
        "start_date": (datetime.now() + timedelta

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
