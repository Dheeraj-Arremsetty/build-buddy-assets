import json
from datetime import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="summarize_contract", description="Generates a concise summary of a contract document using an AI model.", permission=ToolPermission.ADMIN)
def summarize_contract(contract_text: str) -> str:
    """
    Simulates a call to a watsonx.ai model to summarize the provided contract text.

    Args:
        contract_text (str): The full text of the contract to be summarized.

    Returns:
        str: A JSON string containing a bulleted summary of the contract.
    """
    # --- SYNTHETIC DATA GENERATION ---
    summary_points = [
        "Parties Involved: Client Corp and Vendor Inc.",
        "Effective Date: " + datetime.now().strftime('%Y-%m-%d'),
        "Term: 24 months from effective date.",
        "Key Services: Cloud data processing and analytics.",
        "Payment Terms: Net 30 days upon receipt of invoice."
    ]
    return json.dumps({"summary": summary_points, "model_used": "simulated/granite-3-8b-instruct"})

@tool(name="extract_key_clauses", description="Extracts specific key clauses from a contract, such as payment terms, termination conditions, and liability limits.", permission=ToolPermission.ADMIN)
def extract_key_clauses(contract_text: str) -> str:
    """
    Simulates a call to a watsonx.ai model to extract structured data from contract text.

    Args:
        contract_text (str): The full text of the contract.

    Returns:
        str: A JSON string containing the extracted clauses.
    """
    # --- SYNTHETIC DATA GENERATION ---
    clauses = {
        "payment_terms": "Payments are due within 30 days of the invoice date.",
        "termination_clause": "Either party may terminate with 60 days written notice.",
        "governing_law": "State of New York",
        "confidentiality": "Standard mutual confidentiality obligations apply for 5 years post-termination."
    }
    if "unlimited liability" in contract_text.lower():
        clauses["liability"] = "Vendor assumes unlimited liability for data breaches."
    else:
        clauses["liability"] = "Liability is capped at the total contract value for the preceding 12 months."
        
    return json.dumps(clauses, indent=2)

@tool(name="identify_contractual_risks", description="Analyzes a contract against a knowledge base of legal risks to identify non-standard or high-risk clauses.", permission=ToolPermission.ADMIN)
def identify_contractual_risks(contract_text: str) -> str:
    """
    Simulates using RAG to identify risks. In a real scenario, this tool would query the 
    'legal_risk_kb' knowledge base. Here, we simulate the outcome.

    Args:
        contract_text (str): The full text of the contract to analyze.

    Returns:
        str: A JSON string listing identified risks with severity levels.
    """
    # --- SYNTHETIC DATA GENERATION ---
    risks = []
    if "unlimited liability" in contract_text.lower():
        risks.append({
            "risk_type": "Unlimited Liability",
            "severity": "High",
            "recommendation": "Requires immediate legal review. Propose capping liability.",
            "source_in_kb": "Definition of 'Unlimited Liability' found in knowledge base."
        })
    if not risks:
        risks.append({
            "risk_type": "Standard Terms",
            "severity": "Low",
            "recommendation": "Contract appears to follow standard templates. Safe to proceed.",
            "source_in_kb": "N/A"
        })
        
    return json.dumps({"risk_analysis": risks, "timestamp": datetime.now().isoformat()})