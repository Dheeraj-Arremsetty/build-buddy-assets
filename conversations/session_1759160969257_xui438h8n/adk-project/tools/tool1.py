# tools/data_aggregation/fetch_trade_data.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_trade_data", description="Fetches recent equity trade data for a specified review period.", permission=ToolPermission.ADMIN)
def fetch_trade_data(review_period: str) -> str:
    """
    Retrieves a list of synthetic equity trades from a mock trading system for a given period.

    Args:
        review_period (str): A description of the review period, e.g., 'Q3 2024'.

    Returns:
        str: A JSON string representing a list of trade data. Each trade includes an ID, timestamp, ticker, type, quantity, and price.
    """
    try:
        trades = []
        base_date = datetime.now()
        tickers = ["IBM", "AAPL", "GOOGL", "MSFT", "AMZN"]
        for i in range(15):
            trade_date = base_date - timedelta(days=random.randint(1, 90))
            trade = {
                "trade_id": f"TRD{1000 + i}",
                "timestamp": trade_date.isoformat(),
                "ticker": random.choice(tickers),
                "trade_type": random.choice(["BUY", "SELL"]),
                "quantity": random.randint(100, 50000),
                "price": round(random.uniform(150.0, 500.0), 2),
                "counterparty_id": f"CP{200 + i % 5}"
            }
            trades.append(trade)
        
        # Add a specific trade for volume limit testing
        trades.append({
            "trade_id": "TRD1015",
            "timestamp": (base_date - timedelta(days=10)).isoformat(),
            "ticker": "IBM",
            "trade_type": "BUY",
            "quantity": 150000, # Exceeds limit
            "price": 175.50,
            "counterparty_id": "CP201"
        })

        return json.dumps({"status": "success", "data": trades})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})