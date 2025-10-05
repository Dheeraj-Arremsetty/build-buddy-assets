# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-10-05 15:39:02
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: FinCorp Compliance Automation

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and demonstrating a sophisticated IBM watsonx Orchestrate solution for **FinCorp**, a financial services client. The primary business challenge is the manual, error-prone, and time-consuming process of quarterly compliance reporting. This demo will showcase how a multi-agent AI workforce can automate the entire workflow, from data aggregation and compliance analysis to final report generation.

The solution architecture consists of a supervisor agent that orchestrates three specialized collaborator agents: a **Data Retrieval Agent** to fetch transaction data, a **Compliance Check Agent** to analyze data against regulatory rules using a knowledge base, and a **Reporting Agent** to synthesize the findings into a structured report. This plan provides all necessary code, configuration files, and commands to build a fully functional and impressive demo that directly addresses FinCorp's key pain points, highlighting the power of watsonx Orchestrate for complex business process automation.

## 2. Prerequisites

Before beginning the implementation, ensure your environment is set up correctly. This is crucial for a smooth development and demo experience.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
*   **Python Environment**: A working Python environment (version 3.9 or later) is required to create the custom tools.
*   **watsonx Orchestrate Instance**: You need access to an active IBM watsonx Orchestrate instance, either a cloud environment or the Developer Edition running locally.
*   **CLI Authentication**: Ensure your `orchestrate` CLI is authenticated and connected to your target environment. You can verify this by running `orchestrate agents list`.
*   **Project Directory Structure**: Create a dedicated folder for this project to keep all artifacts organized.

```bash
# Create the project directory structure
mkdir -p fincorp_demo/{agents,tools,knowledge_base_docs}
cd fincorp_demo
```

*   **Python Dependencies**: Create a `requirements.txt` file in the `fincorp_demo/tools/` directory. While our mock tools are self-contained, a real-world scenario would require external libraries.

    **File: `tools/requirements.txt`**
    ```text
    requests
    python-dotenv
    ```

## 3. Step 1: Create the Knowledge Base

The Compliance Check Agent will use a knowledge base to access up-to-date regulatory guidelines. This demonstrates Retrieval-Augmented Generation (RAG), allowing the agent to answer questions based on proprietary documents.

### 3.1. Create Mock Regulatory Documents

First, create two simple text files containing mock regulatory information.

**File: `knowledge_base_docs/aml_policy_v1.txt`**
```text
Anti-Money Laundering (AML) Policy - Version 1.2

1. Transaction Monitoring Threshold: All transactions exceeding $10,000 USD must be flagged for review.
2. High-Risk Jurisdictions: Transactions originating from or destined for jurisdictions on the 'High-Risk' list require enhanced due diligence. Current list includes: Erewhon, Lilliput.
3. Structuring: Multiple transactions from the same source below the $10,000 threshold within a 24-hour period that aggregate to over $15,000 should be considered suspicious activity.
```

**File: `knowledge_base_docs/fraud_detection_rules.txt`**
```text
Fraud Detection Rulebook - Q2 2024

1. Velocity Check: More than 5 transactions from a single account to new, distinct beneficiaries within a 1-hour window is a potential indicator of account takeover fraud.
2. Geographic Anomaly: A transaction initiated from a geographic location significantly different from the account holder's registered address and recent transaction history requires immediate verification.
3. New Account High-Value Transfer: Any transfer over $5,000 from an account less than 30 days old must be placed on a temporary hold pending manual review.
```

### 3.2. Define the Knowledge Base Configuration

Next, create the YAML file that defines the knowledge base and points to these documents. We will use the built-in Milvus vector store provided by watsonx Orchestrate.

**File: `fincorp_compliance_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: fincorp_compliance_kb
description: >
   Contains FinCorp's internal compliance policies, including Anti-Money Laundering (AML) thresholds, fraud detection rules, and lists of high-risk jurisdictions. Use this to verify if financial transactions adhere to company and regulatory standards.
documents:
   - "knowledge_base_docs/aml_policy_v1.txt"
   - "knowledge_base_docs/fraud_detection_rules.txt"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## 4. Step 2: Create the Python Tools

Tools are the foundational components that perform actions. We will create five distinct Python tools, each in its own file, to handle data retrieval, analysis, and report generation.

### 4.1. Tool 1: Fetch Transaction Data

This tool simulates connecting to a core banking system or data warehouse to retrieve a list of financial transactions for a specified period. It generates realistic synthetic data, which is essential for a compelling demo.

**Business Value:** This tool automates the critical first step of any reporting process: data collection. It replaces manual data extraction, saving significant time and reducing the risk of human error from copy-pasting or incorrect filtering.

**File: `tools/fetch_transaction_data.py`**
```python
import json
import random
from datetime import datetime, timedelta
import uuid

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_transaction_data", description="Fetches financial transaction data for a given date range.", permission=ToolPermission.ADMIN)
def fetch_transaction_data(start_date: str, end_date: str) -> list[dict]:
    """
    Retrieves a list of financial transactions from the core banking system within a specified date range.

    Args:
        start_date (str): The start date of the reporting period in 'YYYY-MM-DD' format.
        end_date (str): The end date of the reporting period in 'YYYY-MM-DD' format.

    Returns:
        list[dict]: A list of transaction records. Each record is a dictionary containing transaction details like ID, timestamp, amount, currency, type, status, and source/destination. Returns an empty list if no data is found.
    """
    transactions = []
    num_transactions = random.randint(15, 25)
    
    # Generate some anomalous data for the compliance agent to find
    special_cases = {
        3: {"amount": 12500.50, "origin_country": "USA", "destination_country": "USA"}, # High value
        7: {"amount": 9500.00, "origin_country": "Erewhon", "destination_country": "USA"}, # High-risk jurisdiction
        11: {"amount": 9000.00, "origin_country": "USA", "destination_country": "Lilliput"}, # High-risk jurisdiction
    }

    for i in range(num_transactions):
        base_date = datetime.strptime(start_date, "%Y-%m-%d")
        random_days = random.randint(0, (datetime.strptime(end_date, "%Y-%m-%d") - base_date).days)
        tx_date = base_date + timedelta(days=random_days)
        
        if i in special_cases:
            amount = special_cases[i]["amount"]
            origin_country = special_cases[i]["origin_country"]
            destination_country = special_cases[i]["destination_country"]
        else:
            amount = round(random.uniform(100.0, 9999.0), 2)
            origin_country = random.choice(["USA", "Canada", "UK", "Germany"])
            destination_country = random.choice(["USA", "Canada", "UK", "Germany", "France"])

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "timestamp": tx_date.isoformat(),
            "amount": amount,
            "currency": "USD",
            "type": random.choice(["WIRE_TRANSFER", "ACH", "INTERNAL_TRANSFER"]),
            "status": "COMPLETED",
            "origin_country": origin_country,
            "destination_country": destination_country
        })
        
    return transactions
```

### 4.2. Tool 2: Analyze Data for Anomalies

This tool performs an initial scan of the transaction data to identify statistical outliers or patterns that deviate from the norm, such as unusually high transaction volumes or values.

**Business Value:** This provides a first layer of automated analysis, flagging potential issues that might be missed by simple rule-based checks. It helps focus the compliance review on the most unusual and potentially risky activities.

**File: `tools/analyze_data_for_anomalies.py`**
```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="analyze_data_for_anomalies", description="Analyzes a list of transactions to detect statistical anomalies.", permission=ToolPermission.ADMIN)
def analyze_data_for_anomalies(transactions: list[dict]) -> dict:
    """
    Performs a statistical analysis on a list of financial transactions to identify anomalies.

    Args:
        transactions (list[dict]): The list of transaction data to analyze.

    Returns:
        dict: A summary of findings, including total transactions processed

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
