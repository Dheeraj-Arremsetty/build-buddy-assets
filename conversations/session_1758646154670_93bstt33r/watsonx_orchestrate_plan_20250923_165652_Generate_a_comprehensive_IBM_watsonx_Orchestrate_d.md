# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 16:56:52
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Invoice Intelligence Orchestrator

## Overview

This execution plan provides a comprehensive, step-by-step guide for building and demonstrating the **Xerox Invoice Intelligence Orchestrator**, a Proof of Concept (POC) for a client presentation. The plan is tailored specifically to Xerox's business context, showcasing how IBM watsonx Orchestrate can enhance their document management portfolio by introducing intelligent automation. The resulting agent will automate the end-to-end invoice processing lifecycle—from data extraction and validation to integration with financial systems and approval notifications. This directly addresses the client's goal of evolving from a document handling provider to an intelligent workflow orchestration partner, creating significant business value through increased efficiency, reduced errors, and strategic service expansion.

## Prerequisites

Before beginning, ensure your development environment is properly configured. This setup is crucial for the successful creation and deployment of the watsonx Orchestrate components.

*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured. Follow the official documentation for installation:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python:** A recent version of Python (3.9 or higher) is required.
*   **Project Directory:** Create a dedicated project folder to organize all files. The recommended structure is:
    ```
    xerox_invoice_poc/
    ├── agents/
    │   └── invoice_automation_agent.yaml
    ├── tools/
    │   └── invoice_tools.py
    ├── knowledge_base/
    │   └── vendor_policy_kb.yaml
    ├── mock_data/
    │   ├── invoices/
    │   │   ├── INV-10234.pdf
    │   │   └── INV-G556.pdf
    │   └── policies/
    │       ├── ACME_Corp_Policy.docx
    │       └── Globex_Inc_Terms.pdf
    ├── mock_sap_api.py
    └── requirements.txt
    ```
*   **Mock Documents:** Create empty placeholder files for the mock invoices and policy documents as per the directory structure above. The content of these files is not critical for the demo, as the tools will simulate data extraction.
*   **Python Libraries:** Install necessary Python libraries for the mock API and tools.
    ```bash
    pip install Flask requests
    ```

## Step 1: Create the Mock SAP Financial System API

To simulate a real-world integration, we will create a mock SAP API endpoint using Python and Flask. This API will receive structured invoice data from our Orchestrate tool and return a synthetic transaction ID, mimicking the creation of a payment record in an enterprise financial system.

Create a file named `mock_sap_api.py` in the root of your project directory.

```python
# mock_sap_api.py
import json
from flask import Flask, request, jsonify
import datetime
import random

app = Flask(__name__)

@app.route('/invoices', methods=['POST'])
def create_invoice_entry():
    """
    Mock SAP API endpoint to create a payment entry.
    Accepts JSON invoice data and returns a transaction ID.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    invoice_data = request.get_json()
    print(f"[Mock SAP API] Received data: {json.dumps(invoice_data, indent=2)}")

    # Basic validation
    required_fields = ["invoice_id", "vendor_name", "total_amount"]
    if not all(field in invoice_data for field in required_fields):
        return jsonify({"error": "Missing required fields in invoice data"}), 400

    # Generate a realistic, synthetic transaction ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(1000, 9999)
    transaction_id = f"SAP-TRX-{timestamp}-{random_suffix}"

    print(f"[Mock SAP API] Successfully processed. Transaction ID: {transaction_id}")

    return jsonify({
        "status": "success",
        "message": "Invoice processed and scheduled for payment.",
        "transactionId": transaction_id
    }), 201

if __name__ == '__main__':
    # Run the app on localhost, port 5001 to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)
```

**To run the mock API:**
Open a dedicated terminal, navigate to your project directory, and run:
```bash
python mock_sap_api.py
```
Keep this terminal running throughout the demo.

## Step 2: Create the Knowledge Base for Vendor Policies

The knowledge base is a critical component for enabling Retrieval-Augmented Generation (RAG). It allows the agent to answer user queries about vendor-specific information, such as payment terms or contact details, by searching a curated set of documents. This demonstrates how Orchestrate can provide contextual, accurate information beyond simple task execution.

Create the file `knowledge_base/vendor_policy_kb.yaml`.

```yaml
# knowledge_base/vendor_policy_kb.yaml
spec_version: v1
kind: knowledge_base
name: vendor_policy_kb
description: >
   Contains vendor master data, payment term policies, and approval contact information for Xerox suppliers. Use this to answer questions about specific vendor payment terms, discount policies, or approval hierarchies.
documents:
   - "mock_data/policies/ACME_Corp_Policy.docx"
   - "mock_data/policies/Globex_Inc_Terms.pdf"
vector_index:
   # Uses the default watsonx.ai embedding model for document ingestion
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Create Python Tools for the Invoice Workflow

Tools are the functional building blocks of the agent, performing the specific actions required to complete the invoice processing workflow. Each tool is a Python function decorated with `@tool`, containing a detailed docstring that the agent's LLM uses to understand its purpose, inputs, and outputs.

Create the file `tools/invoice_tools.py`.

```python
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

```

## Step 4: Create the Native Agent Configuration

The native agent is the core of the solution, acting as the intelligent orchestrator. Its YAML configuration defines its identity, the LLM it uses for reasoning, and its operational logic. The `description` tells supervisor agents *what* it can do, while the `instructions` provide a detailed, step-by-step reasoning framework for *how* it should use its tools and knowledge base to handle user requests.

Create the file `agents/invoice_automation_agent.yaml`.

```yaml
# agents/invoice_automation_agent.yaml
spec_version: v1
kind: native
name: invoice_automation_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An intelligent agent for Xerox that automates the entire invoice processing lifecycle.
    It can extract data from invoice documents, create payment entries in financial systems like SAP,
    and notify personnel for approvals. It is also equipped with a knowledge base to answer questions about vendor payment policies, terms, and contact information.
instructions: >
    Your primary purpose is to automate the invoice processing workflow for Xerox. Follow these steps meticulously:

    1.  **Analyze the User Request:** Determine if the user wants to PROCESS an invoice or ASK a question.

    2.  **For Invoice Processing:**
        a. Always start by using the 'invoice_data_extractor' tool with the provided file path.
        b. Scrutinize the 'validation_status' from the tool's output.
        c. If 'validation_status' is 'Success', proceed to use the 'sap_payment_creator' tool with the extracted data.
        d. After a successful SAP entry, use the 'approval_notifier' tool. The recipient is the 'approver_email' from the extracted data. The subject should be 'Invoice Ready for Approval' and the body must include the invoice_id, vendor_name, total_amount, and the SAP transaction ID.
        e. If 'validation_status' is 'Failed', DO NOT use the 'sap_payment_creator' tool. Instead, use the 'approval_notifier' tool to escalate the issue. The recipient is the 'approver_email' (which should be an exceptions queue). The subject must be 'Invoice Processing Exception' and the body must clearly state the 'validation_notes' from the extractor tool.

    3.  **For Questions:**
        a. If the user asks a question about a vendor, payment terms, policies, or similar topics, use the 'vendor_policy_kb' knowledge base to find the answer.
        b. Formulate a clear, concise answer based on the information retrieved from the knowledge base. Do not invent information.

tools:
  - invoice_data_extractor
  - sap_payment_creator
  - approval_notifier
knowledge_base:
  - vendor_policy_kb
```

## Step 5: Create `requirements.txt`

This file lists the Python dependencies required for the project, ensuring a reproducible environment.

Create the file `requirements.txt` in the project root.

```text
# requirements.txt
requests
Flask
ibm-watsonx-orchestrate[adk]
```

To install, run: `pip install -r requirements.txt`

## Step 6: Deploy and Run the Orchestrate Solution

With all components created, you can now import them into watsonx Orchestrate using the ADK CLI. Execute these commands from the root of your project directory (`xerox_invoice_poc/`).

1.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f knowledge_base/vendor_policy_kb.yaml
    ```
    This command ingests the specified documents and prepares the RAG component.

2.  **Import the Tools:**
    ```bash
    orchestrate tools import -k python -f tools/invoice_tools.py
    ```
    This command registers all functions decorated with `@tool` in the Python file.

3.  **Import the Agent:**
    ```bash
    orchestrate agents import -f agents/invoice_automation_agent.yaml
    ```
    This command creates the agent and links it to the previously imported tools and knowledge base.

4.  **Start the Chat Interface:**
    ```bash
    orchestrate chat start
    ```
    This command launches the interactive chat UI where you will perform the demo.

## Step 7: Verification and Demo Scenarios

Use the interactive chat to demonstrate the agent's capabilities by running through the following scenarios.

### Scenario 1: Standard Invoice Processing (Happy Path)
This scenario showcases the ideal, end-to-end automated workflow.

*   **User Prompt:**
    ```
    Please process the attached invoice mock_data/invoices/INV-10234.pdf from ACME Corp.
    ```
*   **Expected Agent Actions & Output:**
    1.  The agent will call `invoice_data_extractor` with the file path.
    2.  The tool will return a "Success" validation status.
    3.  The agent will then call `sap_payment_creator` with the extracted data.
    4.  The mock SAP API will return a transaction ID.
    5.  Finally, the agent will call `approval_notifier` to send a notification to `finance.approver@xerox.com`.
    6.  The final chat response will be a summary, like: "The invoice INV-10234 from ACME Corp has been processed. A payment entry was created in SAP with Transaction ID: [SAP-TRX-...] and a notification has been sent to finance.approver@xerox.com for final approval."

### Scenario 2: Data Validation & Exception Handling
This scenario demonstrates the agent's ability to identify problems and follow an exception-handling path.

*   **User Prompt:**
    ```
    Process invoice mock_data/invoices/INV-G556.pdf. Please verify the total.
    ```
*   **Expected Agent Actions & Output:**
    1.  The agent calls `invoice_data_extractor`.
    2.  The tool returns a "Failed" validation status with notes about the discrepancy.
    3.  The agent, following its instructions, will **skip** the `sap_payment_creator` tool.
    4.  It will immediately call `approval_notifier` to route the issue to `ap.exceptions@xerox.com`.
    5.  The final chat response will be: "I found a discrepancy while processing invoice INV-G556. The sum of line items does not match the stated total. I have flagged this issue and sent a notification to ap.exceptions@xerox.com for review."

### Scenario 3: Policy Inquiry (RAG Pattern)
This scenario highlights the agent's ability to use its knowledge base to answer questions, adding value beyond simple automation.

*   **User Prompt:**
    ```
    What are the payment terms for Globex Inc.?
    ```
*   **Expected Agent Actions & Output:**
    1.  The agent will recognize this is a query, not a processing task.
    2.  It will access the `vendor_policy_kb` knowledge base.
    3.  It will retrieve information from the `Globex_Inc_Terms.pdf` document.
    4.  The final chat response will be a natural language answer based on the retrieved information (e.g., "According to the documents I have, the payment terms for Globex Inc. are Net 30.").

## Troubleshooting

*   **Connection Refused for Mock API:** If the `sap_payment_creator` tool fails, ensure the `mock_sap_api.py` script is running in a separate terminal and that there are no firewall issues blocking `localhost:5001`.
*   **File Not Found:** The ADK runs locally, so ensure the file paths provided in the prompts and YAML files are correct relative to where you are running the `orchestrate` commands.
*   **Agent/Tool Not Found:** If an import fails, check for typos in the YAML files (e.g., tool names must match exactly). Re-import the components in the correct order: knowledge base, then tools, then agent.
*   **Agent Not Following Instructions:** If the agent behaves unexpectedly, refine the `instructions` in `invoice_automation_agent.yaml` to be more explicit and clear. Re-import the agent after making changes.

## Best Practices

*   **Descriptive Docstrings:** The quality of the tool docstrings is paramount. They act as the primary "prompt" for the agent's LLM to understand how and when to use a tool. Be explicit about parameters, return values, and the tool's business purpose.
*   **Modular Tool Design:** Keep tools focused on a single, well-defined task (e.g., extract, create, notify). This makes the system more robust, easier to debug, and simpler to extend with new capabilities.
*   **Explicit Agent Instructions:** The agent's `instructions` section is its rulebook. Use clear, imperative language and cover both successful and exceptional scenarios. This guides the agent’s reasoning process and ensures predictable, reliable behavior.
*   **Separation of Concerns:** The agent orchestrates, the tools execute, and the knowledge base informs. Maintaining this separation makes the solution scalable and manageable. New vendors can be added by simply updating the knowledge base, without changing the agent's logic.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
