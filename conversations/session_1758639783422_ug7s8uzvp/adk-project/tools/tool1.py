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