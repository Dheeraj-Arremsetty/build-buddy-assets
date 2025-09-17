# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 21:29:55
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Intelligent Document Processing (IDP) AI Gateway

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building the **Xerox Intelligent Document Processing (IDP) AI Gateway** demo using IBM watsonx Orchestrate. This solution is specifically tailored to address Xerox's strategic goal of evolving from a hardware provider to a leader in AI-powered document services.

The demo implements a sophisticated multi-agent system using the **Supervisor/Collaborator pattern**. A central `IDP_Gateway_Agent` acts as an intelligent router, classifying incoming documents (invoices, contracts) and delegating them to specialized collaborator agents for processing. This showcases a scalable, governed, and efficient framework for automating high-value document workflows, directly demonstrating how Xerox can offer advanced, AI-driven business process automation to its clients. The plan covers project setup, mock data creation, knowledge base configuration, tool development, agent definition, and deployment, culminating in a series of verification scenarios that highlight the business value of the solution.

## 2. Prerequisites

Before starting, ensure your development environment is correctly configured.

*   **Python:** Python 3.10 or later installed.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured. If not installed, run:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. Run `orchestrate login` and `orchestrate env select` to configure your CLI.
*   **Text Editor/IDE:** A code editor such as Visual Studio Code is recommended for creating and editing Python and YAML files.
*   **Project Directory:** Create a root folder for the demo to keep all files organized. We will refer to this as `xerox-idp-gateway/`.

## 3. Step 1: Project Structure and Mock Data Creation

A well-organized project structure is essential. We will create the necessary directories and mock data files that will be used by our agents and tools.

1.  **Create the Directory Structure:**
    Open your terminal and create the following folder structure inside your `xerox-idp-gateway/` directory:

    ```bash
    mkdir -p agents tools knowledge_bases mock_data
    ```

2.  **Create the Vendor Knowledge Base Data:**
    This CSV file will be ingested into a watsonx Orchestrate knowledge base. The `Invoice_Processor_Agent` will use it to validate that invoices are from approved vendors.

    Create a file named `vendor_database.csv` inside the `mock_data/` directory.

    **File:** `mock_data/vendor_database.csv`
    ```csv
    Vendor Name,Vendor ID,Payment_Terms
    ACME Corp,V-1001,Net 30
    Globex Corporation,V-1002,Net 60
    Stark Industries,V-1003,Net 45
    Wayne Enterprises,V-1004,Net 30
    Cyberdyne Systems,V-1005,Net 15
    ```

3.  **Create Mock Invoice and Contract Files:**
    These text files simulate the documents that users will upload for processing.

    **File:** `mock_data/invoice_acme.txt`
    ```text
    INVOICE
    Number: INV-123
    Date: 2024-09-15
    Vendor Name: ACME Corp
    Amount Due: 5400.00
    Due Date: 2024-10-15
    Line Items:
    - 10x Rocket Skates: 4000.00
    - 1x Giant Magnet: 1400.00
    ```

    **File:** `mock_data/contract_globex.txt`
    ```text
    SERVICE AGREEMENT
    Between: Globex Corporation ("Provider") and Client Inc. ("Client")
    Effective Date: 2024-10-01
    Contract Value: $250,000
    Term: 24 Months
    Termination Clause: Termination for cause requires a 30-day written notice.
    Liability Cap: Provider's liability is capped at the total fees paid in the preceding 12 months.
    Payment Terms: Net 60
    ```

    **File:** `mock_data/purchase_order.txt` (For the ambiguous document scenario)
    ```text
    PURCHASE ORDER
    PO Number: PO-9876
    Vendor: Stark Industries
    Date: 2024-09-20
    Item: 50x Mark V Power Core
    Total: $1,500,000
    ```

## 4. Step 2: Create the Knowledge Base Configuration

The knowledge base provides the `Invoice_Processor_Agent` with external data for validation tasks. We will define a built-in Milvus knowledge base that ingests our vendor CSV file.

**Business Value:** This component demonstrates how watsonx Orchestrate can enrich agent reasoning with proprietary business data, enabling critical validation steps that reduce fraud and ensure compliance with procurement policies.

Create the file `vendor_db.yaml` inside the `knowledge_bases/` directory.

**File:** `knowledge_bases/vendor_db.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: vendor_database_kb
description: >
   Contains approved Xerox vendor information, including official names, unique vendor IDs, and standard payment terms.
   This knowledge base is used by the Invoice_Processor_Agent to validate that incoming invoices are from legitimate, pre-approved vendors before processing payment.
documents:
   - "mock_data/vendor_database.csv"
vector_index:
   # Using the default embedding model for simplicity
   embeddings_model_name: ibm/slate-12m-english-rtrvr
```

## 5. Step 3: Develop the Python Tools

Tools are the building blocks that allow agents to perform actions. We will create two Python files, one for invoice-related tools and one for contract-related tools. Each tool is a Python function decorated with `@tool` and includes a detailed docstring, which the agent's LLM uses to understand its capability.

### 5.1. Invoice Processing Tools

Create the file `invoice_tools.py` inside the `tools/` directory.

**File:** `tools/invoice_tools.py`
```python
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
```

### 5.2. Contract Analysis Tools

Create the file `contract_tools.py` inside the `tools/` directory.

**File:** `tools/contract_tools.py`
```python
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
```

## 6. Step 4: Create Requirements File

Create a `requirements.txt` file in the root `xerox-idp-gateway/` directory to manage any dependencies. For this demo, no external libraries are needed beyond the ADK, but this is a best practice.

**File:** `requirements.txt`
```text
# No external dependencies required for these tools.
# If tools used libraries like 'requests' or 'pandas', they would be listed here.
# e.g., requests
```

## 7. Step 5: Define the Agent Configurations (YAML)

We will now define our three agents using YAML configuration files. These files specify each agent's name, description, instructions, tools, and collaborators, forming the core of our AI-driven workflow.

### 7.1. Collaborator: Invoice_Processor_Agent

This agent specializes in handling all aspects of invoice processing.

**Business Value:** This specialist agent automates the entire invoice validation and processing workflow, reducing manual data entry, minimizing payment errors, and accelerating the procure-to-pay cycle.

Create the file `Invoice_Processor_Agent.yaml` inside the `agents/` directory.

**File:** `agents/Invoice_Processor_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Invoice_Processor_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  A specialist agent for end-to-end invoice processing. It is an expert at extracting data from invoices,
  validating vendor details against the approved vendor database (vendor_database_kb), and updating payment
  status in the SAP ERP system. Use this agent for any tasks related to financial invoices.
instructions: >
  You are an expert invoice processor. Follow these steps meticulously:
  1.  When you receive the content of an invoice, your first step is to use the `extract_invoice_data` tool to get structured data.
  2.  After successful extraction, use the `vendor_name` from the extracted data to search the `vendor_database_kb` knowledge base to find information about the vendor.
  3.  Next, use the `validate_vendor_details` tool. Pass the `vendor_name` and the search results from the knowledge base to this tool to confirm the vendor is approved.
  4.  If the vendor is valid, use the `update_sap_invoice_status` tool to mark the invoice as 'Paid'. Use the invoice number, vendor name, and amount from the extracted data.
  5.  Finally, report the result of the SAP update, including the transaction ID, back to the user. If any step fails, report the error clearly.
collaborators: []
tools:
  - extract_invoice_data
  - validate_vendor_details
  - update_sap_invoice_status
knowledge_base:
  - vendor_database_kb
```

### 7.2. Collaborator: Contract_Analyzer_Agent

This agent specializes in analyzing legal contracts.

**Business Value:** This agent automates the review of legal documents, extracting key terms and risks. This drastically reduces the time required by legal and sales teams for contract review and ensures key data is captured accurately in downstream systems like Salesforce.

Create the file `Contract_Analyzer_Agent.yaml` inside the `agents/` directory.

**File:** `agents/Contract_Analyzer_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Contract_Analyzer_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  A specialist agent for analyzing legal contracts and agreements. It is an expert at extracting critical clauses,
  summarizing key terms, and creating corresponding records in Salesforce. Use this agent for any tasks involving
  legal documents like service agreements, NDAs, or partnership contracts.
instructions: >
  You are an expert legal contract analyst. Follow this precise workflow:
  1.  When given the content of a contract, first use the `extract_contract_clauses` tool to get structured data.
  2.  Next, take the JSON output from the extraction and pass it to the `summarize_key_terms` tool to create a human-readable summary.
  3.  Then, use the `create_salesforce_record` tool. Pass the summary, contract value, and effective date to this tool to log the new agreement in the CRM.
  4.  Conclude by presenting the summary and the confirmation message from the Salesforce update, including the new record ID, to the user.
collaborators: []
tools:
  - extract_contract_clauses
  - summarize_key_terms
  - create_salesforce_record
```

### 7.3. Supervisor: IDP_Gateway_Agent

This is the main agent that acts as the central router.

**Business Value:** The gateway agent serves as a single, intelligent entry point for all document processing tasks. It provides a layer of abstraction and governance, ensuring that documents are handled by the correct specialized process. This architecture is highly scalable, as Xerox can easily add new collaborator agents (e.g., for purchase orders, insurance claims) without changing the entry point.

Create the file `IDP_Gateway_Agent.yaml` inside the `agents/` directory.

**File:** `agents/IDP_Gateway_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: IDP_Gateway_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    An intelligent document processing gateway for Xerox. It analyzes incoming documents like invoices and contracts,
    and routes them to specialized agents for processing. It relies on the Invoice_Processor_Agent for financial documents
    and the Contract_Analyzer_Agent for legal agreements.
instructions: >
    Your primary role is to act as a classifier and router for business documents.
    - Carefully examine the user's request and any provided document content to determine the document type.
    - If the document is an invoice or relates to billing, use the `Invoice_Processor_Agent`.
    - If the document is a legal contract, service agreement, or NDA, use the `Contract_Analyzer_Agent`.
    - If the document type is ambiguous or one you are not equipped to handle (like a purchase order), do not guess. Inform the user clearly about your current capabilities (processing invoices and contracts) and ask for clarification or offer to save the document for later review. Do not attempt to process it.
collaborators:
  - Invoice_Processor_Agent
  - Contract_Analyzer_Agent
tools: []
```

## 8. Step 6: Deploy the Solution using ADK CLI

With all configuration files and tools created, we will now use the watsonx Orchestrate ADK CLI to import and deploy the entire solution. Run these commands from the root directory of your `xerox-idp-gateway/` project.

**IMPORTANT:** The order of operations matters. We must import tools and knowledge bases first, followed by the collaborator agents, and finally the supervisor agent that depends on them.

1.  **Import the Invoice Tools:**
    ```bash
    orchestrate tools import -f tools/invoice_tools.py
    ```

2.  **Import the Contract Tools:**
    ```bash
    orchestrate tools import -f tools/contract_tools.py
    ```

3.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/vendor_db.yaml
    ```

4.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/Invoice_Processor_Agent.yaml
    orchestrate agents import -f agents/Contract_Analyzer_Agent.yaml
    ```

5.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/IDP_Gateway_Agent.yaml
    ```

After these commands run successfully, all components of the IDP Gateway will be deployed and active in your watsonx Orchestrate environment.

## 9. Verification Steps

To test the solution and demonstrate the demo scenarios, you will interact with the `IDP_Gateway_Agent`. You can do this via the Orchestrate chat interface (`orchestrate chat start`) or by integrating it into a custom application.

### Scenario 1: Automated Invoice Processing

1.  **User Action:** Start a chat with the `IDP_Gateway_Agent` and provide the content of the mock invoice.
    *   **Prompt:** `"Please process this invoice: [Paste the content of mock_data/invoice_acme.txt here]"`
2.  **Expected Behavior:**
    *   The `IDP_Gateway_Agent` identifies the document as an invoice and routes the task to the `Invoice_Processor_Agent`.
    *   The `Invoice_Processor_Agent` executes its toolchain: extracts data, validates "ACME Corp" against the knowledge base, and calls the mock SAP update tool.
3.  **Expected Output (similar to):**
    `"Invoice #INV-123 for $5,400.00 from ACME Corp has been processed and marked as paid in SAP. The transaction ID is SAP-TXN-XXXXXX."`

### Scenario 2: Intelligent Contract Analysis

1.  **User Action:** In the same chat, provide the content of the mock contract.
    *   **Prompt:** `"Can you analyze this new client contract for me? [Paste the content of mock_data/contract_globex.txt here]"`
2.  **Expected Behavior:**
    *   The `IDP_Gateway_Agent` identifies the document as a contract and routes it to the `Contract_Analyzer_Agent`.
    *   The `Contract_Analyzer_Agent` extracts clauses, summarizes them, and calls the mock Salesforce creation tool.
3.  **Expected Output (similar to):**
    `"Contract analysis complete. Here is a summary: The agreement is effective from 2024-10-01 with a total value of $250,000. A new record has been created in Salesforce with ID 0068d00000XXXXXABC."`

### Scenario 3: Ambiguous Document Handling

1.  **User Action:** Provide the content of the out-of-scope document.
    *   **Prompt:** `"What can you tell me about this document? [Paste the content of mock_data/purchase_order.txt here]"`
2.  **Expected Behavior:**
    *   The `IDP_Gateway_Agent` analyzes the text, identifies it as a Purchase Order, and determines it has no specialist collaborator for this document type.
3.  **Expected Output (based on instructions):**
    `"I have identified this document as a Purchase Order. Currently, I am configured to process Invoices and Contracts. Would you like me to save this document for later review?"`

## 10. Troubleshooting

*   **Routing Failures:** If the `IDP_Gateway_Agent` routes incorrectly or fails to route, review its `description` and `instructions` as well as the `description` of the collaborator agents. The supervisor relies heavily on these natural language descriptions to make its routing decisions. Ensure they are distinct and accurately describe the collaborators' capabilities.
*   **Tool Not Found Errors:** If an agent reports it cannot find a tool, ensure the tool was imported successfully using `orchestrate tools list`. Verify that the tool names in the agent's YAML file exactly match the `name` defined in the `@tool` decorator or the function name if no name is specified.
*   **Python Tool Errors:** If a tool fails during execution, check the terminal where your Orchestrate server is running for Python stack traces. Common issues include errors in the mock logic (e.g., a regex failing to find a match) or incorrect data types being passed between tools.
*   **Knowledge Base Issues:** If the `Invoice_Processor_Agent` cannot validate a vendor, ensure the knowledge base was imported correctly (`orchestrate knowledge-bases list`) and that the CSV file path in the YAML is correct relative to where you run the import command.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
