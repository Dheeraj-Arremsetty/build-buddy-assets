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