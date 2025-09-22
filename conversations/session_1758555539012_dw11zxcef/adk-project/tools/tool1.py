import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_daily_sales_report", permission=ToolPermission.ADMIN)
def get_daily_sales_report() -> dict:
    """
    Retrieves the sales report for the previous day.

    The report includes total revenue, number of transactions, and a list of the top-selling items.
    This tool is used to get a quick summary of the store's financial performance.

    Returns:
        dict: A dictionary containing the sales report details.
    """
    try:
        with open('data/sales_data.json', 'r') as f:
            sales_data = json.load(f)
        return sales_data
    except FileNotFoundError:
        return {"error": "Sales data file not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding sales data JSON."}