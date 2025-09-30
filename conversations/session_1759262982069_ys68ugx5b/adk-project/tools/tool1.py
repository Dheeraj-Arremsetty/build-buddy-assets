# tools/collect_swift_transactions.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="collect_swift_transactions", description="Collects recent SWIFT transaction data for analysis.", permission=ToolPermission.ADMIN)
def collect_swift_transactions(days_ago: int = 1) -> list[dict]:
    """
    Simulates collecting a list of recent SWIFT MT103 transactions from an external system.

    Args:
        days_ago (int): The number of past days to retrieve transactions for. Defaults to 1.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a SWIFT transaction.
    """
    transactions = []
    countries = ["US", "GB", "DE", "SG", "CH", "AE"]
    banks = ["NWBK", "CITI", "HSBC", "DB", "SCBL"]
    
    for i in range(random.randint(10, 20)):
        sender_country = random.choice(countries)
        receiver_country = random.choice(list(set(countries) - {sender_country}))
        
        transaction = {
            "transaction_id": f"SWFT{random.randint(10000000, 99999999)}",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, days_ago * 1440))).isoformat(),
            "amount": round(random.uniform(5000.0, 150000.0), 2),
            "currency": random.choice(["USD", "EUR", "GBP"]),
            "sender_bic": f"{random.choice(banks)}{sender_country}2LXXX",
            "receiver_bic": f"{random.choice(banks)}{receiver_country}2LXXX",
            "status": "COMPLETED",
            "metadata": {"source": "SWIFT_NETWORK", "message_type": "MT103"}
        }
        transactions.append(transaction)
    return transactions