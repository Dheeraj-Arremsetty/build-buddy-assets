# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 16:05:00
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Intelligent Financial Insights Engine

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying the "Intelligent Financial Insights Engine" for the client. This solution leverages a multi-agent architecture within IBM watsonx Orchestrate to address the critical business need for rapid, on-demand financial analysis. The engine will transform static financial reports into a dynamic, conversational intelligence source, empowering executives to make faster, data-driven decisions by asking natural language questions.

The architecture consists of a supervisor agent, the `Executive_Financial_Assistant`, which intelligently delegates tasks to two specialized collaborator agents: the `Financial_Document_Analyst` for data retrieval from a secure knowledge base, and the `Performance_Summarizer` for data synthesis and summary generation. This plan details the creation of all required components—knowledge bases, tools, and agents—using the IBM watsonx Orchestrate Agent Development Kit (ADK), complete with full code examples and deployment commands.

## 2. Prerequisites

Before beginning, ensure your development environment is correctly configured.

*   **IBM watsonx Orchestrate ADK**: The ADK must be installed and configured. If you haven't installed it, run:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python**: Python 3.9 or higher is required.
*   **Project Structure**: Create a dedicated project directory to organize your files.
    ```bash
    mkdir financial_insights_engine
    cd financial_insights_engine
    mkdir -p agents tools knowledge_base/documents
    ```
*   **Orchestrate Environment**: You must be logged into your IBM watsonx Orchestrate environment via the CLI.
    ```bash
    # Log in to your Orchestrate environment (follow the prompts)
    orchestrate login

    # Set the active environment for your project
    orchestrate env set <your_environment_name>
    ```
*   **Text Editor**: A code editor like Visual Studio Code is recommended for editing Python and YAML files.

## 3. Step-by-Step Instructions

### Step 1: Create the Knowledge Base and Mock Financial Documents

The foundation of our RAG (Retrieval-Augmented Generation) pattern is a secure knowledge base containing the client's financial documents. We will create mock documents and a knowledge base definition to ingest them.

**A. Create Mock Financial Documents**

First, we will create two sample text files representing quarterly financial reports. Place these files in the `knowledge_base/documents/` directory.

**File: `knowledge_base/documents/Q1_2024_Financial_Report.txt`**
```text
Q1 2024 Financial Performance Report - For Internal Use Only

Executive Summary:
In the first quarter of 2024, our company demonstrated strong performance with significant growth in key areas. Total revenue reached $150 million, a 15% increase year-over-year. Net income stood at $25 million, with an Earnings Per Share (EPS) of $1.25. This growth was driven by strong sales in our Cloud Services division and successful cost-management initiatives.

Key Financial Metrics:
- Total Revenue: $150,000,000
- Cost of Goods Sold (COGS): $60,000,000
- Gross Profit: $90,000,000
- Operating Expenses: $55,000,000
- Net Income: $25,000,000
- Earnings Per Share (EPS): $1.25
- Cash Flow from Operations: $40,000,000

Divisional Performance:
- Cloud Services Revenue: $85 million
- Enterprise Software Revenue: $65 million
```

**File: `knowledge_base/documents/Q2_2024_Financial_Report.txt`**
```text
Q2 2024 Financial Performance Report - Confidential

Executive Summary:
The second quarter of 2024 continued the positive momentum from Q1. Total revenue grew to $165 million, up 18% compared to the prior year's quarter. Net income was robust at $30 million, resulting in an EPS of $1.50. Market expansion and the launch of our new AI platform were key contributors to this success.

Key Financial Metrics:
- Total Revenue: $165,000,000
- Cost of Goods Sold (COGS): $65,000,000
- Gross Profit: $100,000,000
- Operating Expenses: $60,000,000
- Net Income: $30,000,000
- Earnings Per Share (EPS): $1.50
- Cash Flow from Operations: $45,000,000

Divisional Performance:
- Cloud Services Revenue: $95 million
- Enterprise Software Revenue: $70 million
```

**B. Define the Knowledge Base in YAML**

Now, create the YAML configuration file that tells Orchestrate how to build the knowledge base from these documents.

**File: `knowledge_base/corporate_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: Corporate_Financial_Reports_KB
description: >
   A secure and comprehensive knowledge base containing quarterly financial reports, earnings call transcripts, and performance summaries. Use this to answer specific questions about financial metrics like revenue, net income, and EPS for given time periods.
documents:
   - "knowledge_base/documents/Q1_2024_Financial_Report.txt"
   - "knowledge_base/documents/Q2_2024_Financial_Report.txt"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 2: Develop the Python Tools

Next, we will create the Python functions that our agents will use to perform specific tasks: querying structured data and summarizing it. These tools encapsulate business logic and can be reused across different agents.

Create a single Python file for all financial tools.

**File: `tools/financial_tools.py`**
```python
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Dict, List, Any

@tool(name="query_financial_documents", description="Queries a structured data source for specific financial metrics like revenue, net income, or EPS for a given quarter.", permission=ToolPermission.ADMIN)
def query_financial_documents(quarter: str) -> str:
    """
    Retrieves key financial metrics for a specified quarter from a structured data source.
    This tool simulates accessing a financial database to pull high-level figures.

    Args:
        quarter (str): The financial quarter to query, in the format 'Q# YYYY' (e.g., 'Q1 2024').

    Returns:
        str: A JSON string containing the financial data for the specified quarter, or an error message if the quarter is not found.
    """
    #
    # Business Value: This tool provides a standardized way for an agent to retrieve specific, structured financial data points.
    # It abstracts the complexity of database queries, ensuring that the agent receives clean, reliable data for further analysis or
    # direct answers, which accelerates the process of responding to precise executive queries.
    #
    # Technical Implementation: This function simulates a database lookup using a hardcoded Python dictionary.
    # In a real-world scenario, this would contain logic to connect to a database (e.g., DB2, Oracle) via an API,
    # execute a SQL query, and format the results into a JSON object. The use of a JSON string

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
