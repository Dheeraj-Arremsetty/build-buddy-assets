import json
import random
from datetime import datetime, timedelta
from uuid import uuid4
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_trade_data", description="Fetches raw trade data for a specific batch ID from the primary trading system.", permission=ToolPermission.ADMIN)
def fetch_trade_data(trade_batch_id: str) -> str:
    """
    Simulates fetching a batch of raw trade data from a core trading system based on a batch ID.

    Args:
        trade_batch_id (str): The unique identifier for the trade batch to be processed.

    Returns:
        str: A JSON string representing a list of trade records. Each record includes details like trade ID, ticker, quantity, price, and trade date.
    """
    try:
        trades = []
        tickers = ["IBM", "AAPL", "GOOGL", "MSFT", "AMZN"]
        for _ in range(random.randint(3, 7)):
            trade_date = datetime.now() - timedelta(days=random.randint(1, 3))
            trades.append({
                "trade_id": f"T{random.randint(10000, 99999)}",
                "trade_batch_id": trade_batch_id,
                "ticker": random.choice(tickers),
                "quantity": random.randint(100, 5000),
                "price": round(random.uniform(150.0, 500.0), 2),
                "trade_type": random.choice(["BUY", "SELL"]),
                "trade_date": trade_date.isoformat(),
                "counterparty_id": f"CP{random.randint(101, 105)}",
                "status": "PENDING_SETTLEMENT"
            })
        return json.dumps({"status": "success", "data": trades, "record_count": len(trades)})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@tool(name="get_counterparty_details", description="Retrieves detailed information for a list of counterparty IDs.", permission=ToolPermission.ADMIN)
def get_counterparty_details(counterparty_ids: list[str]) -> str:
    """
    Simulates fetching detailed information for a list of counterparties from a master database.

    Args:
        counterparty_ids (list[str]): A list of unique counterparty identifiers.

    Returns:
        str: A JSON string containing details for each counterparty, including name, region, and credit rating.
    """
    try:
        counterparties = {
            "CP101": {"name": "Global Investment Bank", "region": "NA", "credit_rating": "AA-"},
            "CP102": {"name": "European Securities", "region": "EMEA", "credit_rating": "A+"},
            "CP103": {"name": "APAC Trading Co.", "region": "APAC", "credit_rating": "A"},
            "CP104": {"name": "Americas Capital", "region": "NA", "credit_rating": "BBB+"},
            "CP105": {"name": "Union Finance Group", "region": "EMEA", "credit_rating": "A-"}
        }
        results = {cp_id: counterparties.get(cp_id, {"error": "Not Found"}) for cp_id in counterparty_ids}
        return json.dumps({"status": "success", "data": results})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})