# tools/data_aggregation_tool.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="aggregate_financial_data", permission=ToolPermission.ADMIN)
def aggregate_financial_data(reporting_period: str) -> str:
    """
    Aggregates financial transaction data from various source systems for a specified reporting period.

    This tool simulates fetching data from trading, ledger, and payment systems to create a consolidated
    dataset for compliance analysis.

    Args:
        reporting_period (str): The reporting period to aggregate data for (e.g., "Q3 2024").

    Returns:
        str: A JSON string representing a list of aggregated financial transactions.
    """
    transactions = []
    base_date = datetime.now()
    counterparties = [
        {"id": "CPTY-001", "name": "Global Trade Inc.", "risk_region": "High"},
        {"id": "CPTY-002", "name": "Innovate Solutions LLC", "risk_region": "Low"},
        {"id": "CPTY-003", "name": "Quantum Holdings", "risk_region": "Medium"},
        {"id": "CPTY-004", "name": "Apex Minerals Corp", "risk_region": "High"},
        {"id": "CPTY-005", "name": "NextGen Pharma", "risk_region": "Low"},
    ]

    for i in range(10):
        transaction_date = base_date - timedelta(days=random.randint(1, 90))
        amount = round(random.uniform(500.0, 25000.0), 2)
        # Ensure at least one transaction is over the $10,000 AML threshold
        if i == 5:
            amount = 15500.75

        transactions.append({
            "transaction_id": f"TRN-{1000 + i}",
            "timestamp": transaction_date.isoformat(),
            "amount": amount,
            "currency": "USD",
            "status": random.choice(["Completed", "Pending"]),
            "source_system": random.choice(["Trading System Alpha", "Core Ledger", "Payments Gateway"]),
            "counterparty": random.choice(counterparties)
        })

    return json.dumps({"transactions": transactions})