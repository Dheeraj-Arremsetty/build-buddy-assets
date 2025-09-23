# tools/invoice_tools.py
import json
import random
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# --- Tool 1: Invoice Data Extractor ---
@tool(permission=ToolPermission.ADMIN)
def invoice_data_extractor(file_path: str) -> dict:
    """
    Extracts key information from an invoice document using intelligent document processing.
    It identifies fields like invoice number, vendor, line items, and total amount.
    This tool also performs a basic validation by checking if the line items sum up to the total.

    Args:
        file_path (str): The local path to the invoice PDF file (e.g., 'mock_data/invoices/INV-10234.pdf').

    Returns:
        dict: A dictionary containing extracted and validated data. Includes a 'validation_status' field.
    """
    print(f"[Tool] Running invoice_data_extractor for: {file_path}")
    # In a real-world scenario, this would call a document intelligence service (e.g., IBM Datacap).
    # For this demo, we simulate the extraction and validation based on the filename.
    if "INV-10234.pdf" in file_path:
        # Simulates the "Happy Path" scenario
        return {
            "invoice_id": "INV-10234",
            "vendor_name": "ACME Corp",
            "total_amount": 5499.99,
            "line_items": [
                {"description": "Model X Scanner", "quantity": 1, "price": 4500.00},
                {"description": "Service Contract", "quantity": 1, "price": 999.99}
            ],
            "approver_email": "finance.approver@xerox.com",
            "validation_status": "Success",
            "validation_notes": "Line items sum matches total amount."
        }
    elif "INV-G556.pdf" in file_path:
        # Simulates the "Exception Handling" scenario
        return {
            "invoice_id": "INV-G556",
            "vendor_name": "Globex Inc.",
            "total_amount": 1250.00, # Stated total is incorrect
            "line_items": [
                {"description": "Enterprise Toner Cartridge", "quantity": 5, "price": 200.00},
                {"description": "Shipping", "quantity": 1, "price": 50.00}
            ],
            "approver_email": "ap.exceptions@xerox.com",
            "validation_status": "Failed",
            "validation_notes": "Discrepancy found: Sum of line items ($1050.00) does not match stated total ($1250.00)."
        }
    else:
        return {
            "validation_status": "Error",
            "validation_notes": f"Could not process unknown invoice file: {file_path}"
        }

# --- Tool 2: SAP Payment Creator ---
@tool(permission=ToolPermission.ADMIN)
def sap_payment_creator(invoice_data: dict) -> str:
    """
    Creates a payment entry in the SAP financial system using the validated invoice data.
    This tool connects to the financial system's API to log the transaction for payment processing.

    Args:
        invoice_data (dict): A dictionary of structured invoice data from the invoice_data_extractor tool.

    Returns:
        str: A confirmation message including the transaction ID from SAP upon successful creation.
    """
    print(f"[Tool] Running sap_payment_creator with data: {json.dumps(invoice_data, indent=2)}")
    # The URL for the mock API we started in Step 1
    api_url = "http://localhost:5001/invoices"
    try:
        response = requests.post(api_url, json=invoice_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        response_data = response.json()
        transaction_id = response_data.get("transactionId")
        return f"Successfully created payment entry in SAP. Transaction ID: {transaction_id}"
    except requests.exceptions.RequestException as e:
        print(f"[Tool Error] Failed to connect to Mock SAP API: {e}")
        return f"Error: Could not connect to the financial system. Details: {str(e)}"

# --- Tool 3: Approval Notifier ---
@tool(permission=ToolPermission.ADMIN)
def approval_notifier(recipient_email: str, subject: str, body: str) -> str:
    """
    Sends a notification email to a specified recipient for approval or review.
    This is used to alert approvers of new payment requests or to flag exceptions for human review.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject line of the notification email.
        body (str): The content of the notification email.

    Returns:
        str: A confirmation message indicating the notification was sent.
    """
    print(f"[Tool] Running approval_notifier...")
    print("--- SIMULATED EMAIL ---")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print("-----------------------")
    return f"Notification successfully sent to {recipient_email}."