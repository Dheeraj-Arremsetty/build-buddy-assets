from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="generate_final_report", permission=ToolPermission.ADMIN)
def generate_final_report(company_name: str, financial_summary: str, ratio_analysis: dict, news_summary: str, qualitative_insights: str) -> str:
    """
    Compiles all gathered information into a single, formatted financial analysis report. This is the final step.

    Args:
        company_name (str): The name of the company being analyzed.
        financial_summary (str): A summary of the income statement.
        ratio_analysis (dict): A dictionary of calculated financial ratios.
        news_summary (str): A summary of recent market news.
        qualitative_insights (str): Insights from the knowledge base about industry context.

    Returns:
        str: A comprehensive, formatted report ready for the user.
    """
    
    report = f"""
# Financial Analysis Report: {company_name}

## 1. Quantitative Financial Summary
{financial_summary}

## 2. Key Financial Ratios
- **Debt-to-Equity Ratio**: {ratio_analysis.get('debt_to_equity_ratio', 'N/A')}
- **Profit Margin**: {ratio_analysis.get('profit_margin_percent', 'N/A')}%
- **Price-to-Earnings (P/E) Ratio**: {ratio_analysis.get('price_to_earnings_ratio', 'N/A')}

## 3. Qualitative Context and Industry Benchmarks
{qualitative_insights}

## 4. Recent Market News
{news_summary}

--- End of Report ---
"""
    return report