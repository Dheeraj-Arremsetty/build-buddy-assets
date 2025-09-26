# tools/data_ingestion_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def fetch_market_data(market_sector: str, date_range: int = 7) -> str:
    """
    Fetches synthetic market trend data for a specified sector over a given date range.
    This tool simulates connecting to a market data API to gather context for financial analysis.

    Args:
        market_sector (str): The financial market sector to fetch data for (e.g., 'Technology', 'Healthcare', 'Energy').
        date_range (int): The number of past days to fetch data for. Defaults to 7.

    Returns:
        str: A JSON string containing a list of daily market data points, including dates, sentiment scores, and key news headlines.
    """
    market_data = []
    sentiments = ['positive', 'negative', 'neutral']
    headlines = {
        'Technology': ["New AI Chip Unveiled", "Cloud Division Exceeds Expectations", "Regulatory Scrutiny on Big Tech Increases"],
        'Healthcare': ["Promising Drug Trial Results", "Healthcare Merger Approved", "New Telemedicine Platform Launched"],
        'Energy': ["Oil Prices Surge on Supply Concerns", "Major Investment in Renewable Energy", "Geopolitical Tensions Affect Market"]
    }

    for i in range(date_range):
        day = datetime.now() - timedelta(days=i)
        data_point = {
            "date": day.strftime('%Y-%m-%d'),
            "sector": market_sector,
            "market_sentiment": random.choice(sentiments),
            "sentiment_score": round(random.uniform(0.3, 0.9), 2),
            "key_headline": random.choice(headlines.get(market_sector, ["General market news."]))
        }
        market_data.append(data_point)

    return json.dumps({"status": "success", "data": market_data})

@tool(permission=ToolPermission.ADMIN)
def get_transaction_logs(account_id: str, start_date: str, end_date: str) -> str:
    """
    Retrieves synthetic transaction logs for a specific account within a given date range.
    This simulates querying an internal banking or trading system for customer activity.

    Args:
        account_id (str): The unique identifier for the account being queried.
        start_date (str): The start date for the query in YYYY-MM-DD format.
        end_date (str): The end date for the query in YYYY-MM-DD format.

    Returns:
        str: A JSON string containing a list of transaction records.
    """
    transactions = []
    statuses = ['completed', 'pending', 'flagged_for_review']
    transaction_types = ['deposit', 'withdrawal', 'transfer', 'securities_purchase']
    counterparties = ['Global Corp', 'Innovate Inc.', 'Quantum Solutions', 'Apex Holdings']

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    num_transactions = random.randint(5, 20)

    for _ in range(num_transactions):
        tx_date = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
        transaction = {
            "transaction_id": f"TXN-{random.randint(1000000, 9999999)}",
            "account_id": account_id,
            "timestamp": tx_date.isoformat(),
            "amount": round(random.uniform(100.0, 50000.0), 2),
            "currency": "USD",
            "transaction_type": random.choice(transaction_types),
            "status": random.choice(statuses),
            "counterparty": random.choice(counterparties),
            "location": "USA"
        }
        transactions.append(transaction)

    return json.dumps({"status": "success", "data": transactions})