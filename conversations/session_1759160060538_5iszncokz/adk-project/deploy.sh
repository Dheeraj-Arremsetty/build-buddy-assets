#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A Python version of 3.9 or higher is required. It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    # Create a virtual environment
    python -m venv venv
    # Activate the virtual environment
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
3.  **Project Directory Structure**: Create a dedicated folder for the demo to keep all assets organized.
    ```bash
    mkdir partner-pro-demo
    cd partner-pro-demo
    mkdir agents tools knowledge_bases knowledge_bases/documents
    ```
4.  **Orchestrate Environment Initialization**: You must have an active watsonx Orchestrate environment configured. This involves logging into your IBM Cloud account and setting up the Orchestrate environment.
    ```bash
    # Log in to your IBM Cloud account
    orchestrate login --username <your_email> --sso

    # Initialize your environment (follow the prompts)
    orchestrate environments init
    ```
5.  **Required Python Packages**: A `requirements.txt` file should be created to list all necessary Python libraries for the custom tools.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
    Install these packages using:
    ```bash
    pip install -r requirements.txt
    ```

## Step 1: Create Domain-Specific Knowledge Bases

To empower our specialized agents, we will create three distinct knowledge bases, each corresponding to a core business domain: Operations, Promotions, and HR. This separation ensures that information retrieval is fast, accurate, and contextually relevant, preventing "knowledge contamination" between different functional areas. This directly addresses the client's need for reliable, domain-specific information.

First, create placeholder source documents.

**1.1. Create Mock Source Documents**

In the `knowledge_bases/documents/` directory, create the following text files with sample content:

*   `operations_guide.txt`:
    ```text
    Store Opening Procedure:
    1. Disable alarm system using code 1234.
    2. Turn on all lights.
    3. Boot up all POS terminals.
    4. Verify cash float in each register is $200.

    Cash Handling Policy:
    All cash deposits must be reconciled at the end of the day.
    Two staff members must be present during final cash count.
    Deposits must be secured in the time-locked safe.
    ```
*   `promo_playbook.txt`:
    ```text
    Summer Sale Promotion (June 1 - August 31):
    - 20% off all summer apparel.
    - BOGO on select footwear.
    - Display standard: Front-of-store mannequin must feature the flagship summer dress.
    - Signage Kit #SUM2024 must be used.

    Back-to-School Event (August 15 - September 15):
    - 30% off backpacks and stationery.
    - Display standard: Aisle 4 endcap must be dedicated to this promotion.
    ```
*   `hr_manual.txt`:
    ```text
    Leave Policy:
    Employees are entitled to 10 paid vacation days and 5 sick days per year.
    Leave requests must be submitted through the HR portal at least two weeks in advance.

    Payroll Schedule:
    Payday is bi-weekly, on every other Friday.
    Pay stubs are available electronically via the employee self-service portal.
    ```

**1.2. Define Knowledge Base Configurations**

In the `knowledge_bases/` directory, create the following YAML files. These files instruct Orchestrate to create built-in knowledge bases by ingesting our source documents.

*   `operations_kb.yaml`:
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: partner_pro_operations_kb
    description: >
      Contains official documentation and standard operating procedures (SOPs) for store operations.
      This includes cash handling policies, store opening and closing checklists, security protocols, and inventory management guidelines.
    documents:
      - "documents/operations_guide.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```
*   `promotions_kb.yaml`:
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: partner_pro_promotions_kb
    description: >
      A comprehensive repository of all current and upcoming marketing promotions.
      It includes details on discount structures, promotional periods, product eligibility, and visual merchandising standards.
    documents:
      - "documents/promo_playbook.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```
*   `hr_kb.yaml`:
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: partner_pro_hr_kb
    description: >
      The authoritative source for all Human Resources policies and procedures.
      This covers topics such as payroll schedules, employee leave policies, dress code, and performance management processes.
    documents:
      - "documents/hr_manual.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 2: Create Python Tools for Actionable Tasks

While knowledge bases provide answers from documents, tools allow agents to perform actions or retrieve dynamic, structured data. We will create a set of Python-based tools for each specialized domain. These tools will generate realistic synthetic data, simulating interactions with live business systems like a POS or HR information system.

In the `tools/` directory, create the following Python files:

**2.1. Operations Tools (`operations_tools.py`)**

This toolset provides access to structured operational data and procedures. It helps managers execute daily tasks correctly, ensuring compliance and reducing errors, which directly contributes to the goal of "Operational Excellence".

