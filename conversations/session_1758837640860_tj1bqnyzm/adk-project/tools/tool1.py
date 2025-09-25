import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_trade_data", description="Fetches recent trade transaction data for a given time period.", permission=ToolPermission.ADMIN)
def fetch_trade_data(start_date: str, end_date: str) -> str:
    """
    Retrieves a list of trade transactions within a specified date range. This tool simulates
    accessing a core banking or trading platform to collect raw data for compliance analysis.

    Args:
        start_date (str): The start date of the reporting period in 'YYYY-MM-DD' format.
        end_date (str): The end date of the reporting period in 'YYYY-MM-DD' format.

    Returns:
        str: A JSON string representing a list of trade transactions. Each transaction includes
             an ID, timestamp, amount, currency, counterparty, and jurisdiction.
    """
    try:
        # Generate realistic synthetic data
        transactions = []
        counterparties = ["Global Exports LLC", "Tech Innovators Inc.", "Shadow Syndicate Inc.", "Quantum Solutions"]
        jurisdictions = ["USA", "UK", "Northland", "Singapore"]
        for i in range(15):
            tx_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(0, 90))
            transactions.append({
                "transaction_id": f"TRD{random.randint(10000, 99999)}",
                "timestamp": tx_date.isoformat(),
                "amount": round(random.uniform(500.0, 25000.0), 2),
                "currency": "USD",
                "counterparty": random.choice(counterparties),
                "jurisdiction": random.choice(jurisdictions),
                "status": "completed"
            })
        
        # Add a specific high-value transaction for testing
        transactions.append({
            "transaction_id": "TRD11223",
            "timestamp": (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=10)).isoformat(),
            "amount": 15000.00,
            "currency": "USD",
            "counterparty": "Global Exports LLC",
            "jurisdiction": "USA",
            "status": "completed"
        })

        return json.dumps({"status": "success", "data": transactions})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@tool(name="fetch_account_metadata", description="Fetches metadata for accounts involved in transactions.", permission=ToolPermission.ADMIN)
def fetch_account_metadata(account_ids: list[str]) -> str:
    """
    Retrieves metadata for a list of account IDs, such as the associated industry and risk rating.
    This simulates querying a Customer Relationship Management (CRM) or account management system.

    Args:
        account_ids (list[str]): A list of account IDs to retrieve metadata for.

    Returns:
        str: A JSON string containing a dictionary where keys are account IDs and values are
             their associated metadata, including industry and risk score.
    """
    try:
        metadata = {}
        industries = ["Manufacturing", "Technology", "Precious Metals Trading", "Logistics", "Online Gambling"]
        for acc_id in account_ids:
            metadata[acc_id] = {
                "industry": random.choice(industries),
                "risk_rating": random.choice(["Low", "Medium", "High"]),
                "onboarding_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime('%Y-%m-%d')
            }
        return json.dumps({"status": "success", "data": metadata})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})