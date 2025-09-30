# tools/collect_internal_ledger_data.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="collect_internal_ledger_data", description="Collects internal ledger transaction data.", permission=ToolPermission.ADMIN)
def collect_internal_ledger_data(days_ago: int = 1) -> list[dict]:
    """
    Simulates collecting a list of recent transactions from an internal ledger system.

    Args:
        days_ago (int): The number of past days to retrieve transactions for. Defaults to 1.

    Returns:
        list[dict]: A list of dictionaries, each representing an internal ledger entry.
    """
    ledger_entries = []
    for i in range(random.randint(15, 25)):
        entry = {
            "entry_id": f"LEDG{random.randint(100000, 999999)}",
            "transaction_date": (datetime.now() - timedelta(hours=random.randint(1, days_ago * 24))).isoformat(),
            "debit_account": f"ACC{random.randint(10000, 20000)}",
            "credit_account": f"ACC{random.randint(20001, 30000)}",
            "amount": round(random.uniform(100.0, 75000.0), 2),
            "currency": "USD",
            "description": random.choice(["Invoice Payment", "Service Fee", "Payroll Deposit", "Inter-account Transfer"]),
            "status": "POSTED",
            "metadata": {"source": "INTERNAL_LEDGER", "system": "SAP_FICO"}
        }
        ledger_entries.append(entry)
    return ledger_entries