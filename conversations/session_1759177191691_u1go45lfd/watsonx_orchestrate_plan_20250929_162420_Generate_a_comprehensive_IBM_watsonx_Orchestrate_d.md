# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 16:24:20
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Comprehensive Demo Execution Plan

## Overview

This execution plan provides a detailed, step-by-step guide for creating a comprehensive IBM watsonx Orchestrate demo for a financial services client. The demo showcases a sophisticated multi-agent system designed to automate the quarterly financial risk assessment and reporting process. This addresses the client's need to transform a manual, error-prone workflow into an efficient, reliable, and auditable automated system.

The solution features a supervisor agent that orchestrates several specialized collaborator agents, each responsible for a distinct phase of the process: data ingestion, risk analysis, compliance verification, and report generation. By leveraging custom Python tools that simulate interactions with enterprise systems and a knowledge base for regulatory policies, this demo effectively illustrates the power of watsonx Orchestrate to handle complex, multi-step business processes, enhance operational efficiency, and improve decision-making through AI-driven automation.

## Prerequisites

Before beginning, ensure your environment is set up with the following components. This setup is crucial for the successful development, deployment, and execution of the watsonx Orchestrate agents and tools.

1.  **IBM watsonx Orchestrate Account**: An active watsonx Orchestrate account with access to the Agent Builder and ADK (Agent Development Kit).
2.  **Python Environment**: Python 3.10 or later installed on your local machine.
3.  **IBM watsonx Orchestrate ADK**: The ADK must be installed and configured. If not installed, run the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
4.  **ADK Authentication**: You must be authenticated to your watsonx Orchestrate environment. Run the login command and follow the prompts:
    ```bash
    orchestrate login
    ```
5.  **Project Directory Structure**: Create a dedicated project folder to organize all artifacts. This structure is essential for managing the different components of the solution.

    ```
    /financial_risk_demo
    |-- /agents
    |   |-- 01_data_ingestion_agent.yaml
    |   |-- 02_risk_analysis_agent.yaml
    |   |-- 03_compliance_check_agent.yaml
    |   |-- 04_report_generation_agent.yaml
    |   |-- 05_risk_supervisor_agent.yaml
    |-- /tools
    |   |-- data_collection_tools.py
    |   |-- data_analysis_tools.py
    |   |-- compliance_tools.py
    |   |-- reporting_tools.py
    |-- /knowledge_base
    |   |-- docs
    |   |   |-- Global_Finance_Corp_Compliance_Policies.txt
    |   |-- compliance_kb.yaml
    |-- requirements.txt
    ```

## Step 1: Create the Knowledge Base and Supporting Documents

The `compliance_check_agent` will use a knowledge base to cross-reference financial activities against the latest internal policies. This demonstrates how Orchestrate can ground its reasoning in your organization's specific documentation.

### 1.1. Create the Compliance Policy Document

Create a text file containing mock compliance policies.

**File:** `financial_risk_demo/knowledge_base/docs/Global_Finance_Corp_Compliance_Policies.txt`
```text
Global Finance Corp - Official Compliance Policies (Q3 2024 Update)

Document ID: GFC-COMP-2024-Q3-v1.2

Section 1: Transaction Monitoring Thresholds
1.1: Any single transaction exceeding $500,000 USD must be flagged for manual review by the Senior Compliance Officer.
1.2: A series of transactions from a single entity totaling over $1,000,000 USD within a 30-day period requires an enhanced due diligence check.
1.3: Transactions involving entities from high-risk jurisdictions (as defined in Appendix A) above $10,000 USD must be reported immediately.

Section 2: Market Position Limits
2.1: The firm's total exposure to any single non-investment-grade security shall not exceed 5% of the total portfolio value.
2.2: The daily trading volume in any single equity shall not exceed 15% of the 30-day average daily volume for that equity.

Section 3: Data Privacy and Handling (GDPR & CCPA)
3.1: All client data used in risk models must be anonymized unless explicit consent is documented.
3.2: Cross-border data transfers for analysis require pre-approval from the Data Privacy Office.

Appendix A: High-Risk Jurisdictions
- List of jurisdictions is updated quarterly and maintained by the International Compliance Division. For the purpose of this document, assume any transaction with "offshore" in its description is high-risk.
```

### 1.2. Create the Knowledge Base YAML Configuration

This YAML file defines the knowledge base, pointing to the document you just created. Orchestrate will ingest this document into its built-in vector store.

**File:** `financial_risk_demo/knowledge_base/compliance_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: gfc_compliance_policies_kb
description: >
  Contains the official internal compliance policies and regulatory guidelines for Global Finance Corp.
  This knowledge base includes information on transaction monitoring thresholds, market position limits,
  data privacy rules, and lists of high-risk jurisdictions. Use this to verify if financial
  activities adhere to company policy.
documents:
  - "knowledge_base/docs/Global_Finance_Corp_Compliance_Policies.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Create the Python Tools

These tools simulate fetching, processing, and analyzing data from various enterprise systems. Each tool is defined in a Python file using the `@tool` decorator and generates realistic synthetic data to make the demo self-contained and robust.

### 2.1. Create `requirements.txt`

This file lists the Python dependencies for our tools.

**File:** `financial_risk_demo/requirements.txt`
```
requests
python-dotenv
```

### 2.2. Data Collection Tools

This module simulates fetching raw data from market data providers and internal transaction systems. It represents the first step in any data-driven workflow: gathering the necessary information.

**File:** `financial_risk_demo/tools/data_collection_tools.py`
```python
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def get_market_data(symbols: list[str]) -> str:
    """
    Fetches the latest market data for a list of financial symbols (e.g., stocks, bonds).
    This tool simulates a call to a market data provider API like Bloomberg or Refinitiv.

    Args:
        symbols (list[str]): A list of ticker symbols to fetch data for (e.g., ["IBM", "AAPL", "GOOG"]).

    Returns:
        str: A JSON string containing a list of market data objects, each with symbol, price, volume, and a 52-week high/low.
    """
    market_data = []
    for symbol in symbols:
        price = round(random.uniform(100.0, 500.0), 2)
        market_data.append({
            "symbol": symbol,
            "price": price,
            "volume": random.randint(1_000_000, 10_000_000),
            "52_week_high": round(price * random.uniform(1.1, 1.5), 2),
            "52_week_low": round(price * random.uniform(0.7, 0.9), 2),
            "timestamp": datetime.utcnow().isoformat()
        })
    return json.dumps(market_data, indent=2)

@tool(permission=ToolPermission.ADMIN)
def get_internal_transactions(days: int) -> str:
    """
    Retrieves a list of internal financial transactions from the last specified number of days.
    This simulates querying an internal transaction database or data warehouse (e.g., SAP S/4HANA).

    Args:
        days (int):

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
