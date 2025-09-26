#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
        ```
2.  **Python Environment**: A Python version of 3.10 or higher is required. It is highly recommended to use a virtual environment to manage dependencies.
    *   **Command (to create a virtual environment)**:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
3.  **Orchestrate CLI Login**: You must be logged into your watsonx Orchestrate environment via the CLI.
    *   **Command**:
        ```bash
        orchestrate login
        ```
4.  **Project Directory Structure**: Create a dedicated directory to organize all the demo assets. This structure is essential for the relative paths used in the configuration files.
    *   **Command**:
        ```bash
        mkdir -p finsecure_demo/{agents,tools,knowledge_base/documents}
        ```
    *   **Final Structure**:
        ```
        /finsecure_demo
        |-- /agents
        |   |-- 01_transaction_data_collector_agent.yaml
        |   |-- 02_risk_analysis_agent.yaml
        |   |-- 03_compliance_verification_agent.yaml
        |   |-- 04_audit_reporting_agent.yaml
        |-- /tools
        |   |-- data_collection_tools.py
        |   |-- risk_analysis_tools.py
        |   |-- compliance_verification_tools.py
        |   |-- reporting_tools.py
        |-- /knowledge_base
        |   |-- aml_policy_kb.yaml
        |   |-- /documents
        |       |-- FinSecure_AML_Policy_Guide.pdf
        |-- requirements.txt
        ```

## Step 1: Create the Knowledge Base

We will begin by creating a knowledge base containing FinSecure Analytics' internal Anti-Money Laundering (AML) policies. This allows the `Compliance Verification Agent` to answer questions and validate procedures using Retrieval-Augmented Generation (RAG), demonstrating how Orchestrate can be grounded in enterprise-specific knowledge.

### 1.1. Create a Mock Policy Document

First, create a mock PDF document. For this demo, you can create a simple text file and save it as a PDF named `FinSecure_AML_Policy_Guide.pdf` inside the `finsecure_demo/knowledge_base/documents/` directory.

**Content for `FinSecure_AML_Policy_Guide.pdf`:**

> **FinSecure Analytics - Global Anti-Money Laundering (AML) Policy Guide v2.1**
>
> **1. Transaction Monitoring:** All transactions exceeding $10,000 USD must be flagged for enhanced due diligence. Transactions involving sanctioned jurisdictions require immediate escalation to the Chief Compliance Officer. Sanctioned jurisdictions include North Korea, Iran, and Syria.
>
> **2. Customer Due Diligence (CDD):** Standard CDD must be performed for all new clients. Enhanced Due Diligence (EDD) is required for Politically Exposed Persons (PEPs) and clients operating in high-risk industries such as casinos or precious metal dealerships.
>
> **3. Sanctions Screening:** All client and transaction counterparties must be screened against the latest OFAC (Office of Foreign Assets Control) and UN sanctions lists on a daily basis. A positive match must result in a frozen transaction and the filing of a Suspicious Activity Report (SAR).
>
> **4. Reporting:** Suspicious Activity Reports (SARs) must be filed with FinCEN within 30 calendar days of detecting suspicious activity. The report must detail the parties involved, transaction amounts, dates, and a narrative explaining the basis for suspicion.

### 1.2. Create the Knowledge Base YAML Configuration

Next, create the YAML file that defines the knowledge base for Orchestrate. This file points to the document we just created and specifies the embedding model to use for vectorizing the content.

**File:** `finsecure_demo/knowledge_base/aml_policy_kb.yaml`

