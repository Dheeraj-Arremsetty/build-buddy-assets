# tools/data_processing_tools.py

import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="collect_transaction_data", description="Collects raw transaction data from the past quarter for a specified department.", permission=ToolPermission.ADMIN)
def collect_transaction_data(department: str) -> str:
    """
    Gathers raw transaction data from the past quarter for a specified department.
    This tool simulates fetching data from a core business system like a financial database or ERP.

    Args:
        department (str): The department to collect data for (e.g., 'Sales', 'Marketing', 'R&D').

    Returns:
        str: A JSON string representing a list of raw transaction records.
    """
    try:
        transactions = []
        today = datetime.now()
        for i in range(20): # Generate 20 realistic records
            transaction_date = today - timedelta(days=random.randint(1, 90))
            status = random.choice(['Completed', 'Pending', 'Failed', 'Refunded'])
            transactions.append({
                "transaction_id": f"TXN-{random.randint(10000, 99999)}-{i}",
                "date": transaction_date.isoformat(),
                "department": department,
                "amount": round(random.uniform(100.0, 5000.0), 2),
                "currency": "USD",
                "status": status,
                "vendor": f"Vendor_{chr(65 + random.randint(0, 4))}",
                "metadata": {
                    "source_system": "ERP_System_A",
                    "data_quality_score": round(random.uniform(0.85, 0.99), 2)
                }
            })
        return json.dumps(transactions)
    except Exception as e:
        return json.dumps({"error": f"Failed to collect data: {str(e)}"})

@tool(name="process_data", description="Cleans, aggregates, and transforms raw transaction data.", permission=ToolPermission.ADMIN)
def process_data(raw_data_json: str) -> str:
    """
    Takes a JSON string of raw transaction data, filters for completed transactions,
    and calculates key summary statistics.

    Args:
        raw_data_json (str): A JSON string containing a list of raw transaction records.

    Returns:
        str: A JSON string with processed data, including total revenue and transaction counts.
    """
    try:
        raw_data = json.loads(raw_data_json)
        completed_transactions = [t for t in raw_data if t.get('status') == 'Completed']
        
        if not completed_transactions:
            return json.dumps({"summary": "No completed transactions found.", "processed_records": []})

        total_revenue = sum(t['amount'] for t in completed_transactions)
        average_transaction_value = total_revenue / len(completed_transactions)

        processed_summary = {
            "processing_timestamp": datetime.now().isoformat(),
            "total_raw_records": len(raw_data),
            "total_completed_records": len(completed_transactions),
            "total_revenue": round(total_revenue, 2),
            "average_transaction_value": round(average_transaction_value, 2)
        }
        return json.dumps({"summary": processed_summary, "processed_records": completed_transactions})
    except Exception as e:
        return json.dumps({"error": f"Failed to process data: {str(e)}"})