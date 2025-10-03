# tools/data_collection_tools.py

import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def fetch_applicant_details(applicant_id: str) -> str:
    """
    Fetches basic details for a loan applicant from the primary CRM system.

    Args:
        applicant_id (str): The unique identifier for the applicant.

    Returns:
        str: A JSON string containing the applicant's details, including name, contact information, and employment status.
    """
    print(f"Fetching details for applicant ID: {applicant_id}")
    applicants = {
        "789123": {"full_name": "Alice Johnson", "email": "alice.j@example.com", "phone": "555-0101", "employment_status": "Employed", "years_at_employer": 5},
        "456789": {"full_name": "Bob Williams", "email": "bob.w@example.com", "phone": "555-0102", "employment_status": "Self-Employed", "years_at_employer": 8},
    }
    data = applicants.get(applicant_id, {"error": "Applicant not found"})
    return json.dumps({"status": "success", "applicant_id": applicant_id, "data": data})

@tool(permission=ToolPermission.ADMIN)
def get_credit_score(applicant_id: str) -> str:
    """
    Retrieves the credit score for a given applicant by simulating a call to a credit bureau API.

    Args:
        applicant_id (str): The unique identifier for the applicant.

    Returns:
        str: A JSON string containing the credit score and the reporting bureau.
    """
    print(f"Getting credit score for applicant ID: {applicant_id}")
    # Simulate different scores for different applicants
    scores = {
        "789123": random.randint(720, 850),
        "456789": random.randint(650, 719),
    }
    score = scores.get(applicant_id, random.randint(500, 649))
    bureau = random.choice(["Equifax", "Experian", "TransUnion"])
    return json.dumps({"status": "success", "applicant_id": applicant_id, "credit_score": score, "bureau": bureau})

@tool(permission=ToolPermission.ADMIN)
def retrieve_financial_statements(applicant_id: str) -> str:
    """
    Retrieves financial statement summaries for an applicant, such as annual income and total assets/liabilities.

    Args:
        applicant_id (str): The unique identifier for the applicant.

    Returns:
        str: A JSON string containing a summary of the applicant's financial statements.
    """
    print(f"Retrieving financials for applicant ID: {applicant_id}")
    financials = {
        "789123": {
            "annual_income": 120000,
            "total_assets": 550000,
            "total_liabilities": 150000,
            "monthly_debt_payments": 2500
        },
        "456789": {
            "annual_income": 85000,
            "total_assets": 200000,
            "total_liabilities": 95000,
            "monthly_debt_payments": 3000
        },
    }
    data = financials.get(applicant_id, {"error": "Financial statements not available"})
    return json.dumps({"status": "success", "applicant_id": applicant_id, "financials": data})