# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 12:56:46
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan for Global Finance Corp.

## Overview
This execution plan provides a comprehensive, step-by-step guide for creating a watsonx Orchestrate demonstration tailored for Global Finance Corp. The demo showcases an automated solution to the client's challenge of a slow, manual, and error-prone quarterly financial reporting process. By building a hierarchical system of AI agents, we will demonstrate how watsonx Orchestrate can streamline data collection from disparate systems (ERP, CRM), automate complex data processing and analysis, enforce compliance checks, and generate insightful report summaries. This plan implements the full proposed agent architecture, including a supervisor agent that orchestrates tasks across specialized collaborator agents, each equipped with powerful, domain-specific tools. The result is a powerful digital labor pattern that reduces manual effort, minimizes errors, accelerates reporting cycles, and provides auditable, consistent financial insights.

## Prerequisites
Before beginning, ensure your environment is correctly set up. This is crucial for the successful creation, import, and execution of the agents and tools.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required. It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    # Create a virtual environment
    python -m venv orchestrate_env

    # Activate the virtual environment
    # On Windows:
    # orchestrate_env\Scripts\activate
    # On macOS/Linux:
    source orchestrate_env/bin/activate
    ```
3.  **Orchestrate CLI Login**: You must be logged into your watsonx Orchestrate environment via the CLI. If you are using the Developer Edition, ensure the server is running. For SaaS, configure your environment accordingly.
    ```bash
    # Example for starting the Developer Edition server
    orchestrate server start

    # Example for logging into a SaaS environment
    orchestrate login
    ```
4.  **Project Directory Structure**: Create a dedicated project folder to maintain organization.
    ```bash
    mkdir global_finance_demo
    cd global_finance_demo
    mkdir agents
    mkdir tools
    ```

---

## Step 1: Create the Tools
Tools are the fundamental building blocks that perform actions. We will create a series of Python-based tools that generate realistic synthetic financial data, process it, check for compliance, and format it for reporting. Each tool is designed to be a self-contained, reusable component.

### 1.1. Data Collection Tools
These tools simulate fetching raw data from various enterprise systems.

**File: `tools/collection_tools.py`**
This Python file contains tools for gathering data from simulated ERP, CRM, and Treasury systems. The business value lies in automating the first, most time-consuming step of any reporting process: data aggregation. These tools provide a consistent, structured format for raw data, eliminating manual copy-paste errors and ensuring a reliable starting point for analysis.

```python
# tools/collection_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_erp_sales_data", description="Fetches raw sales transaction data from the ERP system for a given quarter.")
def get_erp_sales_data(quarter: str) -> str:
    """
    Simulates fetching raw sales transaction data from an ERP system.

    Args:
        quarter (str): The financial quarter to fetch data for (e.g., 'Q3 2024').

    Returns:
        str: A JSON string representing a list of sales transactions.
    """
    transactions = []
    for i in range(20):  # Generate 20 sample transactions
        transactions.append({
            "transaction_id": f"ERP-SALE-{1000 + i}",
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            "product_id": f"PROD-{random.choice(['A', 'B', 'C'])}{random.randint(100, 199)}",
            "amount": round(random.uniform(500.0, 10000.0), 2),
            "region": random.choice(["NA", "EMEA", "APAC"]),
            "status": "Completed"
        })
    return json.dumps(transactions)

@tool(name="get_crm_pipeline_data", description="Retrieves sales pipeline and opportunity data from the CRM system.")
def get_crm_pipeline_data(quarter: str) -> str:
    """
    Simulates retrieving sales pipeline data from a CRM system.

    Args:
        quarter (str): The financial quarter for the pipeline data (e.g., 'Q3 2024').

    Returns:
        str: A JSON string representing a list of sales opportunities.
    """
    opportunities = []
    for i in range(15): # Generate 15 sample opportunities
        opportunities.append({
            "opportunity_id": f"CRM-OPP-{2000 + i}",
            "stage": random.choice(["Prospecting", "Qualification", "Proposal", "Closed-Won"]),
            "forecast_value": round(random.uniform(20000.0, 150000.0), 2),
            "close_probability": round(random.random(), 2),
            "account_name": f"Client Corp {i+1}"
        })
    return json.dumps(opportunities)

@tool(name="get_treasury_expense_data", description="Gathers operational expense data from the Treasury management system.")
def get_treasury_expense_data(quarter: str) -> str:
    """
    Simulates fetching operational expense data from a Treasury system.

    Args:
        quarter (str): The financial quarter for the expense data (e.g., 'Q3 2024').

    Returns:
        str: A JSON string representing a list of expenses.
    """
    expenses = []
    for i in range(18): # Generate 18 sample expenses
        expenses.append({
            "expense_id": f"TRSY-EXP-{3000 + i}",
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            "category": random.choice(["Salaries", "Marketing", "R&D", "Office Supplies"]),
            "amount": round(random.uniform(1000.0, 75000.0), 2)
        })
    return json.dumps(expenses)
```

### 1.2. Data Processing Tool
This tool performs calculations and transformations on the raw data.

**File: `tools/processing_tool.py`**
This tool is the computational engine of the workflow. It takes raw, unstructured data and transforms it into meaningful financial metrics like total revenue and profit margins. Its business value is immense, as it automates complex calculations that are often performed in spreadsheets, a major source of business risk. This ensures accuracy, consistency, and traceability in all financial calculations.

```python
# tools/processing_tool.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="process_financial_metrics", description="Processes raw sales and expense data to calculate key financial metrics.")
def process_financial_metrics(sales_data_json: str, expense_data_json: str) -> str:
    """
    Aggregates sales and expenses to calculate total revenue, total expenses, and profit margin.

    Args:
        sales_data_json (str): A JSON string of sales transactions from the ERP.
        expense_data_json (str): A JSON string of operational expenses from Treasury.

    Returns:
        str: A JSON string containing calculated metrics (total_revenue, total_expenses, net_profit, profit_margin).
    """
    try:
        sales = json.loads(sales_data_json)
        expenses = json.loads(expense_data_json)

        total_revenue = sum(item['amount'] for item in sales if item['status'] == 'Completed')
        total_expenses = sum(item['amount'] for item in expenses)
        net_profit = total_revenue - total_expenses
        profit_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0

        processed_metrics = {
            "total_revenue": round(total_revenue, 2),
            "total_expenses": round(total_expenses, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin_percent": round(profit_margin, 2)

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
