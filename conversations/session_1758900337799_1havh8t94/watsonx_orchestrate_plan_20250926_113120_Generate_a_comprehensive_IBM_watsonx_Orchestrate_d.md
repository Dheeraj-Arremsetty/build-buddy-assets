# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-26 11:31:20
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Automating QBR for Global Tech Solutions Inc.

## Overview

This execution plan provides a comprehensive guide for creating a powerful IBM watsonx Orchestrate demo tailored for **Global Tech Solutions Inc.** The demo addresses their primary challenge: the manual, time-consuming, and error-prone process of preparing for Quarterly Business Reviews (QBRs). Currently, their sales operations team manually pulls data from disparate systems like Salesforce (CRM), SAP (ERP), and their marketing platform, leading to inefficiencies and potential data inconsistencies.

This plan will build an automated solution using a multi-agent architecture in watsonx Orchestrate. We will create a supervisor agent, the **QBR Supervisor**, that orchestrates tasks across three specialized collaborator agents: a **Salesforce Agent**, an **SAP Agent**, and a **Marketing Agent**. This system will automatically gather account details, opportunity data, contract statuses, order history, and marketing engagement. Additionally, it will leverage a knowledge base of product documentation to answer specific product-related queries on the fly. The result is a seamless, conversational interface that transforms the QBR preparation process from days of manual work into a single, on-demand request, empowering the sales team with accurate, real-time insights.

## Prerequisites

Before beginning, ensure your environment is set up with the following components. This setup is crucial for the successful development, import, and execution of the agents and tools outlined in this plan.

1.  **IBM watsonx Orchestrate Account**: An active watsonx Orchestrate tenant is required. This demo can be built using either the SaaS version or the watsonx Orchestrate Developer Edition.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. This provides the necessary command-line interface (CLI) to import and manage agents, tools, and knowledge bases. If not installed, follow the official documentation:
    ```bash
    pip install ibm-watsonx-orchestrate-adk
    ```
3.  **Python Environment**: A Python 3.8+ environment is required to create the custom tools. Ensure you have `pip` for package management.
4.  **Project Directory Structure**: To keep the project organized, create the following directory structure. This structure separates agents, tools, and knowledge base documents, simplifying the import process.

    ```
    /wxo-qbr-demo
    |-- /agents
    |   |-- qbr_supervisor_agent.yaml
    |   |-- salesforce_agent.yaml
    |   |-- sap_agent.yaml
    |   |-- marketing_agent.yaml
    |-- /tools
    |   |-- salesforce_tools.py
    |   |-- sap_tools.py
    |   |-- marketing_tools.py
    |-- /knowledge_base
    |   |-- /documents
    |   |   |-- product_catalog.pdf  (Create a dummy PDF file for this)
    |   |-- product_catalog_kb.yaml
    |-- requirements.txt
    ```
5.  **CLI Authentication**: Ensure your Orchestrate CLI is authenticated with your environment. You can initialize and log in using the following commands:
    ```bash
    orchestrate env init
    orchestrate login
    ```

---

## Step 1: Create the Knowledge Base

We will start by creating a knowledge base that the supervisor agent can use to answer questions about the company's products. For this demo, we will use a built-in Milvus knowledge base and upload a sample product catalog PDF.

### 1.1. Create a Dummy Document

In the `/knowledge_base/documents/` directory, create a simple PDF file named `product_catalog.pdf`. This file can contain some basic text about fictional products, for example:
*   **QuantumLeap AI**: An advanced machine learning platform for enterprise data analysis.
*   **FusionDB**: A scalable, multi-model database for hybrid cloud environments.
*   **NexusConnect**: A secure API gateway for microservices integration.

### 1.2. Define the Knowledge Base YAML

This YAML file defines the knowledge base, points to the document to be ingested, and specifies the embedding model.

**File:** `/knowledge_base/product_catalog_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: product_catalog_kb
description: >
  Contains detailed information about Global Tech Solutions Inc.'s product offerings, including product datasheets, feature lists, pricing tiers, and technical specifications. Use this to answer any specific questions about company products.
documents:
  - "documents/product_catalog.pdf"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### 1.3. Import the Knowledge Base

Use the Orchestrate CLI to import the knowledge base configuration. Navigate to the `/wxo-qbr-demo/knowledge_base/` directory in your terminal and run the following command:

```bash
# Ensure you are in the /knowledge_base directory
orchestrate knowledge-bases import -f product_catalog_kb.yaml
```
You will receive a confirmation that the import process has started. You can check the status with `orchestrate knowledge-bases status --name product_catalog_kb`.

---

## Step 2: Create the Python Tools

Next, we will create the Python-based tools that our agents will use to fetch data. These tools simulate API calls to Salesforce, SAP, and a marketing platform by generating realistic synthetic data.

### 2.1. Define Dependencies

Create a `requirements.txt` file in the root directory (`/wxo-qbr-demo`) to list the Python packages needed for our tools.

**File:** `/wxo-qbr-demo/requirements.txt`
```
requests
python-dotenv
```
Install these dependencies in your environment: `pip install -r requirements.txt`.

### 2.2. Salesforce Tools

These tools simulate fetching account and opportunity data from Salesforce.

**Business Value**: These tools provide the agent with direct access to critical CRM data. `get_account_details` retrieves foundational customer information, while `get_open_opportunities` is essential for forecasting revenue and identifying deals that need attention, which are core components of any QBR.

**File:** `/tools/salesforce_tools.py`
```python
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_account_details", description="Retrieves core details for a specific customer account from Salesforce.")
def get_account_details(account_name: str) -> str:
    """
    Retrieves core details for a specific customer account, such as account owner, industry, and annual revenue.

    Args:
        account_name (str): The name of the account to retrieve details for.

    Returns:
        str: A JSON string containing the account details.
    """
    if not account_name:
        return json.dumps({"error": "Account name is required."})

    # Realistic synthetic data generation
    industries = ["Technology", "Finance", "Healthcare", "Manufacturing"]
    account_owners = ["John Smith", "Maria Garcia", "Chen Wei", "Emily Johnson"]
    
    account_data = {
        "account_id": f"ACC{random.randint(1000, 9999)}",
        "account_name": account_name,
        "account_owner": random.choice(account_owners),
        "industry": random.choice(industries),
        "annual_revenue": random.randint(5000000, 50000000),
        "created_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d')
    }
    return json.dumps(account_data)

@tool(name="get_open_opportunities", description="Fetches all open sales opportunities for a given customer account from Salesforce.")
def get_open_opportunities(account_name: str) -> str:
    """
    Fetches a list of all open sales opportunities associated with a customer account.

    Args:
        account_name (str): The name of the account to fetch opportunities for.

    Returns:
        str: A JSON string containing

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
