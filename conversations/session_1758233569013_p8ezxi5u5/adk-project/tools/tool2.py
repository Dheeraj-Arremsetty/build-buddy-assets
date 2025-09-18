from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="calculate_financial_ratios", permission=ToolPermission.ADMIN)
def calculate_financial_ratios(total_liabilities: float, shareholder_equity: float, net_income: float, revenue: float, stock_price: float) -> dict:
    """
    Calculates key financial ratios from raw financial data.

    Args:
        total_liabilities (float): The company's total liabilities.
        shareholder_equity (float): The company's total shareholder equity.
        net_income (float): The company's net income.
        revenue (float): The company's total revenue.
        stock_price (float): The current stock price per share.

    Returns:
        dict: A dictionary containing calculated ratios: 'debt_to_equity', 'profit_margin', and 'price_to_earnings'.
    """
    try:
        debt_to_equity = round(total_liabilities / shareholder_equity, 2) if shareholder_equity != 0 else float('inf')
        profit_margin = round((net_income / revenue) * 100, 2) if revenue != 0 else 0.0
            
        # P/E is not meaningful for negative earnings
        if net_income <= 0:
            price_to_earnings = None
        else:
            # This is a simplification; a real calculation uses Earnings Per Share (EPS)
            simulated_shares = shareholder_equity * 0.1 # Simulate share count
            eps = net_income / simulated_shares
            price_to_earnings = round(stock_price / eps, 2) if eps > 0 else None

        return {
            "debt_to_equity_ratio": debt_to_equity,
            "profit_margin_percent": profit_margin,
            "price_to_earnings_ratio": price_to_earnings
        }
    except Exception as e:
        return {"error": f"An error occurred during ratio calculation: {str(e)}"}

@tool(name="summarize_income_statement", permission=ToolPermission.ADMIN)
def summarize_income_statement(income_statement: dict) -> str:
    """
    Generates a brief, human-readable summary of a company's income statement.

    Args:
        income_statement (dict): A dictionary representing the income statement with keys like 'revenue', 'net_income', etc.

    Returns:
        str: A human-readable summary of the income statement.
    """
    revenue = income_statement.get('revenue', 0)
    gross_profit = income_statement.get('gross_profit', 0)
    net_income = income_statement.get('net_income', 0)
    
    summary = (
        f"The company generated ${revenue:,.2f} in revenue, "
        f"resulting in a gross profit of ${gross_profit:,.2f}. "
        f"After all expenses, the net income was ${net_income:,.2f}."
    )
    return summary