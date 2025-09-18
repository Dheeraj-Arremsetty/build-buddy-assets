# tools/reporting_tools.py
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def generate_summary_report(title: str, issues_data: List[Dict[str, Any]]) -> str:
    """
    Generates a formatted summary report of data quality issues in a markdown table.

    Args:
        title (str): The title for the summary report.
        issues_data (List[Dict[str, Any]]): A list of dictionaries, where each dictionary represents a data quality issue or record.

    Returns:
        str: A string containing the formatted markdown report.
    """
    if not issues_data:
        return f"## {title}\n\nNo issues found."

    headers = issues_data[0].keys()
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    rows = []
    for item in issues_data:
        row_values = [str(item.get(h, '')).replace('\n', ' ').replace('|', ' ') for h in headers]
        rows.append("| " + " | ".join(row_values) + " |")

    report = f"## {title}\n\n" + "\n".join([header_line, separator_line] + rows)
    return report