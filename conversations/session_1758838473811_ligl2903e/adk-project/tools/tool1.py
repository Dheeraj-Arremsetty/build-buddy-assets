import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="list_pending_contracts", description="Lists all contracts from Box that are in the 'Pending Review' folder.", permission=ToolPermission.ADMIN)
def list_pending_contracts() -> str:
    """
    Retrieves a list of contract documents awaiting review from a specific folder in Box.

    Returns:
        str: A JSON string representing a list of pending contracts with their metadata.
    """
    # --- SYNTHETIC DATA GENERATION ---
    mock_contracts = [
        {"id": "box-doc-112233", "name": "High_Risk_Vendor_Agreement.pdf", "status": "Pending Review", "uploaded_by": "sales.ops@example.com", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
        {"id": "box-doc-445566", "name": "Standard_MSA_Template.pdf", "status": "Pending Review", "uploaded_by": "legal.team@example.com", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()},
        {"id": "box-doc-778899", "name": "Simple_NDA.pdf", "status": "Pending Review", "uploaded_by": "hr@example.com", "timestamp": (datetime.now() - timedelta(days=3)).isoformat()}
    ]
    return json.dumps(mock_contracts, indent=2)

@tool(name="fetch_contract_from_box", description="Fetches the content of a specific contract document from Box by its name.", permission=ToolPermission.ADMIN)
def fetch_contract_from_box(document_name: str) -> str:
    """
    Simulates downloading a contract document from Box.

    Args:
        document_name (str): The filename of the contract to fetch (e.g., 'High_Risk_Vendor_Agreement.pdf').

    Returns:
        str: A JSON string containing mock content and metadata of the fetched document.
    """
    # --- SYNTHETIC DATA GENERATION ---
    mock_content = {
        "Standard_MSA_Template.pdf": "This is a standard Master Services Agreement...",
        "High_Risk_Vendor_Agreement.pdf": "This agreement contains a clause stating: The vendor assumes unlimited liability...",
        "Simple_NDA.pdf": "This is a simple Non-Disclosure Agreement..."
    }
    
    if document_name in mock_content:
        return json.dumps({
            "document_name": document_name,
            "content": mock_content[document_name],
            "fetch_status": "Success",
            "timestamp": datetime.now().isoformat()
        })
    else:
        return json.dumps({
            "document_name": document_name,
            "content": None,
            "fetch_status": "Error: Document not found",
            "timestamp": datetime.now().isoformat()
        })

@tool(name="upload_signed_contract_to_box", description="Uploads a signed contract to the 'Executed Agreements' folder in Box.", permission=ToolPermission.ADMIN)
def upload_signed_contract_to_box(document_name: str, salesforce_opportunity_id: str) -> str:
    """
    Simulates uploading a signed contract document to a specific folder in Box.

    Args:
        document_name (str): The filename of the signed contract.
        salesforce_opportunity_id (str): The related Salesforce Opportunity ID for metadata tagging.

    Returns:
        str: A JSON string confirming the upload status and providing a mock Box URL.
    """
    # --- SYNTHETIC DATA GENERATION ---
    new_doc_id = f"box-doc-{random.randint(100000, 999999)}"
    return json.dumps({
        "document_name": document_name,
        "upload_status": "Success",
        "destination_folder": "/Executed Agreements/",
        "box_url": f"https://app.box.com/file/{new_doc_id}",
        "metadata_tags": {"salesforce_opportunity_id": salesforce_opportunity_id},
        "timestamp": datetime.now().isoformat()
    })