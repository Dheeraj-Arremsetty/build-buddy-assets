import json
import random
import re
from datetime import datetime, timedelta

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def extract_invoice_data(file_content: str) -> str:
    """
    Extracts key fields from the text content of an invoice document.

    This tool parses unstructured text to identify and return structured data, including the invoice number,
    vendor name, amount due, and due date. This is the first step in automating the procure-to-pay process.

    Args:
        file_content (str): The raw text content of the invoice file.

    Returns:
        str: A JSON string containing extracted fields like invoice_number, vendor_name, and amount_due.
    """
    try:
        # Mock extraction logic using regular expressions
        invoice_number = (re.search(r"Number:\s*(.*)", file_content, re.IGNORECASE) or re.search(r"Invoice #:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        vendor_name = (re.search(r"Vendor Name:\s*(.*)", file_content, re.IGNORECASE) or re.search(r"From:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        amount_due_str = (re.search(r"Amount Due:\s*([0-9,.]+)", file_content, re.IGNORECASE) or re.search(r"Total:\s*\$([0-9,.]+)", file_content, re.IGNORECASE)).group(1).strip().replace(',', '')
        amount_due = float(amount_due_str)
        due_date = (re.search(r"Due Date:\s*(.*)", file_content, re.IGNORECASE) or re.search(r"Payment Due:\s*(.*)", file_content, re.IGNORECASE)).group(1).strip()
        
        extracted_data = {
            "invoice_number": invoice_number,
            "vendor_name": vendor_name,
            "amount_due": amount_due,
            "due_date": due_date,
            "extraction_status": "Success"
        }
        return json.dumps(extracted_data)
    except Exception as e:
        error_data = {"error": f"Failed to extract invoice data: {str(e)}", "extraction_status": "Failed"}
        return json.dumps(error_data)

@tool(permission=ToolPermission.ADMIN)
def validate_vendor_details(vendor_name: str, search_result_from_kb: str) -> str:
    """
    Validates if a vendor from an invoice exists in the approved vendor knowledge base.

    This tool performs a critical compliance check. It takes the vendor name from an invoice and cross-references
    it with the search results from the 'vendor_database_kb'. This prevents payments to unapproved or fraudulent entities.

    Args:
        vendor_name (str): The name of the vendor extracted from the invoice.
        search_result_from_kb (str): The search result snippet returned from querying the knowledge base.

    Returns:
        str: A JSON string indicating if the vendor is valid and providing their Vendor ID if found.
    """
    # In a real scenario, search_result_from_kb would be rich with data.
    # Here, we simulate checking if the vendor_name is present in the KB search result.
    if vendor_name.lower() in search_result_from_kb.lower():
        # Mock finding the Vendor ID from the search result
        vendor_id = f"V-{random.randint(1000, 1999)}"
        validation_result = {
            "vendor_name": vendor_name,
            "is_valid": True,
            "vendor_id": vendor_id,
            "validation_timestamp": datetime.now().isoformat()
        }
    else:
        validation_result = {
            "vendor_name": vendor_name,
            "is_valid": False,
            "reason": "Vendor not found in the approved vendor database.",
            "validation_timestamp": datetime.now().isoformat()
        }
    return json.dumps(validation_result)


@tool(permission=ToolPermission.ADMIN)
def update_sap_invoice_status(invoice_number: str, vendor_name: str, amount: float, status: str) -> str:
    """
    Simulates updating an invoice's status in a backend ERP system like SAP.

    This tool represents the final action in the workflow. After an invoice is extracted and validated, this
    function is called to post the transaction to the system of record, completing the automation loop and
    triggering the payment process.

    Args:
        invoice_number (str): The unique identifier for the invoice.
        vendor_name (str): The name of the vendor being paid.
        amount (float): The total amount of the invoice.
        status (str): The new status to set for the invoice (e.g., 'Paid', 'Pending Approval').

    Returns:
        str: A JSON string confirming the update with a simulated transaction ID.
    """
    transaction_id = f"SAP-TXN-{random.randint(100000, 999999)}"
    update_result = {
        "status": "Success",
        "message": f"Invoice {invoice_number} for {vendor_name} (${amount:,.2f}) has been successfully updated to '{status}' in SAP.",
        "transaction_id": transaction_id,
        "update_timestamp": datetime.now().isoformat()
    }
    return json.dumps(update_result)