import json
import random
import re
from datetime import datetime

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def extract_contract_clauses(file_content: str) -> str:
    """
    Extracts critical clauses and key terms from the text of a legal contract.

    This tool automates the tedious and error-prone task of reviewing contracts. It identifies important data points
    like the effective date, contract value, and specific legal clauses, turning unstructured legal text into
    structured, actionable data for business systems.

    Args:
        file_content (str): The raw text content of the contract file.

    Returns:
        str: A JSON string containing extracted contract terms.
    """
    try:
        effective_date = (re.search(r"Effective Date:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        contract_value_str = (re.search(r"Contract Value:\s*\$?([0-9,.]+)", file_content, re.IGNORECASE)).group(1).strip().replace(',', '')
        contract_value = float(contract_value_str)
        termination_clause = (re.search(r"Termination Clause:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        liability_clause = (re.search(r"Liability Cap:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        
        extracted_data = {
            "effective_date": effective_date,
            "contract_value": contract_value,
            "termination_clause": termination_clause,
            "liability_clause": liability_clause,
            "extraction_status": "Success"
        }
        return json.dumps(extracted_data)
    except Exception as e:
        error_data = {"error": f"Failed to extract contract data: {str(e)}", "extraction_status": "Failed"}
        return json.dumps(error_data)

@tool(permission=ToolPermission.ADMIN)
def summarize_key_terms(contract_data_json: str) -> str:
    """
    Generates a concise, human-readable summary of key contract terms.

    After data extraction, this tool synthesizes the information into a brief summary. This is valuable for
    executives and sales teams who need to quickly understand the core obligations and value of a contract
    without reading the entire document.

    Args:
        contract_data_json (str): A JSON string containing the structured data extracted from the contract.

    Returns:
        str: A brief summary of the contract's most important terms.
    """
    data = json.loads(contract_data_json)
    summary = (
        f"Contract Summary: The agreement is effective from {data['effective_date']} with a total value of ${data['contract_value']:,.2f}. "
        f"Key clauses include: Termination requires specific notice, and liability is capped. "
        f"Please review the full document for details."
    )
    return summary

@tool(permission=ToolPermission.ADMIN)
def create_salesforce_record(contract_summary: str, contract_value: float, effective_date: str) -> str:
    """
    Simulates the creation of a new Opportunity or Contract record in a CRM like Salesforce.

    This tool bridges the gap between legal and sales. It takes the analyzed contract data and creates a
    corresponding record in the CRM, ensuring that the sales and finance teams have immediate visibility into
    new agreements, which accelerates the contract-to-cash cycle.

    Args:
        contract_summary (str): A summary of the contract terms.
        contract_value (float): The total value of the contract.
        effective_date (str): The start date of the contract.

    Returns:
        str: A JSON string confirming the creation of the Salesforce record with a simulated record ID.
    """
    record_id = f"0068d00000{random.randint(10000, 99999)}ABC"
    creation_result = {
        "status": "Success",
        "message": "A new Contract record has been created in Salesforce.",
        "salesforce_record_id": record_id,
        "record_details": {
            "value": f"${contract_value:,.2f}",
            "effective_date": effective_date,
            "summary": contract_summary
        },
        "creation_timestamp": datetime.now().isoformat()
    }
    return json.dumps(creation_result)