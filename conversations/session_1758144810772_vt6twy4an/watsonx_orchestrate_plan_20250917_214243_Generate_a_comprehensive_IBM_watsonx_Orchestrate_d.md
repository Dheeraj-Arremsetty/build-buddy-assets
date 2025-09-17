# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 21:42:43
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Intelligent Procure-to-Pay (P2P) Orchestration Engine

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an **Intelligent Procure-to-Pay (P2P) Orchestration Engine** demo for the client using the IBM watsonx Orchestrate Agent Development Kit (ADK). The solution directly addresses the client's core challenge of automating their complex, multi-system invoice processing workflow. By implementing a multi-agent architecture, this demo will showcase how a central **Supervisor Agent** can intelligently coordinate specialized collaborator agents to ingest, validate, and process invoices, manage exceptions with human-in-the-loop collaboration, and trigger final payment and archival. This powerfully illustrates the business value of reducing manual effort, minimizing errors, accelerating payment cycles, and positioning watsonx Orchestrate as the intelligent automation fabric connecting their existing enterprise systems.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed and configured. If not, install it via pip:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Python 3.9+**: A recent version of Python is required to create the tools.
*   **Project Directory**: Create a dedicated project folder to organize all files. This structure is essential for the relative paths in the configuration files to work correctly.
    ```
    p2p-orchestration-demo/
    ├── agents/
    │   ├── P2P_Supervisor_Agent.yaml
    │   ├── Invoice_Data_Agent.yaml
    │   ├── ERP_Connector_Agent.yaml
    │   └── AP_Action_Agent.yaml
    ├── tools/
    │   ├── invoice_tools.py
    │   ├── erp_tools.py
    │   └── action_tools.py
    ├── knowledge_base/
    │   ├── procurement_policies.yaml
    │   └── docs/
    │       └── Corporate_Procurement_Policy.pdf
    ├── mock_data/
    │   ├── mock_invoice_queue.json
    │   ├── mock_erp_database.csv
    │   └── mock_vendor_master.txt
    └── requirements.txt
    ```
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized with the ADK CLI.

## 3. Step-by-Step Instructions

### Step 1: Create Mock Data and Project Structure

First, set up the project directory and create the synthetic data files that will simulate the client's enterprise systems. This data is designed to trigger all three specified demo scenarios.

1.  **Create the directory structure** using `mkdir` commands as shown in the Prerequisites section.

2.  **Create `mock_data/mock_invoice_queue.json`**: This file simulates a queue of incoming invoices waiting to be processed.
    ```json
    [
        {
            "invoice_id": "INV-1001",
            "vendor_name": "Global Tech Supplies",
            "po_number": "PO-9501",
            "amount": 4500.00,
            "invoice_date": "2024-07-15"
        },
        {
            "invoice_id": "INV-1002",
            "vendor_name": "Office Solutions Inc.",
            "po_number": "PO-9502",
            "amount": 1250.75,
            "invoice_date": "2024-07-16"
        },
        {
            "invoice_id": "INV-1003",
            "vendor_name": "Creative Design Co.",
            "po_number": "PO-9503",
            "amount": 8000.00,
            "invoice_date": "2024-07-17"
        }
    ]
    ```

3.  **Create `mock_data/mock_erp_database.csv`**: This file represents the ERP's Purchase Order records, which serve as the source of truth for validation.
    ```csv
    po_number,vendor_name,approved_amount,status
    PO-9501,"Global Tech Supplies",4500.00,"Approved"
    PO-9502,"Office Solutions Inc.",1200.00,"Approved"
    PO-9503,"Creative Design Co.",8000.00,"Pending Approval"
    ```

4.  **Create `mock_data/mock_vendor_master.txt`**: This file is a simple list of approved vendors, simulating a vendor master database.
    ```text
    Global Tech Supplies
    Office Solutions Inc.
    Logistics Partners LLC
    ```

### Step 2: Create the Knowledge Base

This component showcases how Orchestrate can provide contextual policy information alongside the automation workflow, adding a layer of Retrieval-Augmented Generation (RAG) to the solution.

1.  **Create a dummy PDF `knowledge_base/docs/Corporate_Procurement_Policy.pdf`**: Create a simple one-page PDF document with the following text:
    > **Corporate Procurement Policy v2.1**
    >
    > 1.  **Invoice Approval Thresholds**: All invoices exceeding $50,000 require director-level approval before payment processing.
    > 2.  **New Vendor Onboarding**: Invoices from new vendors must not be processed. Instead, initiate the New Vendor Onboarding Workflow by contacting the procurement department.
    > 3.  **Discrepancy Resolution**: Any mismatch between an invoice and its corresponding Purchase Order must be flagged to the Accounts Payable team via the designated Slack channel for manual review.

2.  **Create `knowledge_base/procurement_policies.yaml`**: This file defines the knowledge base for Orchestrate, pointing to the PDF document.
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: procurement_policies
    description: >
      Contains company policies and standard operating procedures for the procure-to-pay process, including approval thresholds and exception handling rules.
    documents:
      - "./knowledge_base/docs/Corporate_Procurement_Policy.pdf"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 3: Develop Python Tools

Create the Python tools that will perform the actions for each collaborator agent. These tools will read from the mock data files, simulating interactions with real enterprise systems.

1.  **Create `requirements.txt`**: List all necessary Python packages for the tools.
    ```text
    pandas
    ```
    Install them using `pip install -r requirements.txt`.

2.  **Create `tools/invoice_tools.py` for the `Invoice_Data_Agent`**
    *   **Purpose & Business Value**: This tool simulates the client's Xerox agent, responsible for the critical first step of ingesting and structuring raw invoice data. Automating this data extraction eliminates manual data entry, which is a primary source of errors and delays in the P2P cycle, directly improving operational efficiency and data accuracy.
    ```python
    import json
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="extract_invoice_details", description="Extracts structured details from a given invoice ID.", permission=ToolPermission.ADMIN)
    def extract_invoice_details(invoice_id: str) -> dict:
        """
        Retrieves and parses raw invoice information into a structured format.

        Args:
            invoice_id (str): The unique identifier for the invoice to be processed (e.g., 'INV-1001').

        Returns:
            dict: A dictionary containing the structured invoice data, or an error message if not found.
        """
        try:
            with open('./mock_data/mock_invoice_queue.json', 'r') as f:
                invoices = json.load(f)
            
            for invoice in invoices:
                if invoice.get("invoice_id") == invoice_id:
                    return {
                        "status": "success",
                        "data": invoice
                    }
            
            return {"status": "error", "message": f"Invoice with ID '{invoice_id}' not found."}
        except FileNotFoundError:
            return {"status": "error", "message": "Mock invoice data file not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    ```

3.  **Create `tools/erp_tools.py` for the `ERP_Connector_Agent`**
    *   **Purpose & Business Value**: These tools represent the crucial validation step against the system of record (the ERP). By automating PO matching and vendor verification, the business ensures financial compliance, prevents fraudulent or incorrect payments, and maintains the integrity of its financial data without tedious and error-prone manual cross-referencing. This is a core component of risk mitigation in the P2P process.
    ```python
    import pandas as pd
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="validate_po_match", description="Validates invoice details against a Purchase Order in the ERP system.", permission=ToolPermission.ADMIN)
    def validate_po_match(po_number: str, invoice_amount: float) -> dict:
        """
        Validates if the invoice amount matches the approved Purchase Order amount in the ERP system.

        Args:
            po_number (str): The Purchase Order number from the invoice.
            invoice_amount (float): The amount listed on the invoice.

        Returns:
            dict: A dictionary containing validation status ('match', 'mismatch', 'not_found') and details.
        """
        try:
            df = pd.read_csv('./mock_data/mock_erp_database.csv')
            po_record = df[df['po_number'] == po_number]
            
            if po_record.empty:
                return {"status": "not_found", "message": f"PO Number '{po_number}' not found in ERP."}

            approved_amount = po_record.iloc[0]['approved_amount']
            if float(invoice_amount) == float(approved_amount):
                return {"status": "match", "message": "Invoice amount matches PO."}
            else:
                return {
                    "status": "mismatch",
                    "message": f"Amount mismatch for PO '{po_number}'. Invoice: ${invoice_amount}, PO: ${approved_amount}.",
                    "invoice_amount": invoice_amount,
                    "po_amount": approved_amount
                }
        except FileNotFoundError:
            return {"status": "error", "message": "Mock ERP data file not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @tool(name="get_vendor_status", description="Checks if a vendor is in the approved vendor master list.", permission=ToolPermission.ADMIN)
    def get_vendor_status(vendor_name: str) -> dict:
        """
        Checks if a vendor is an approved vendor in the master list.

        Args:
            vendor_name (str): The name of the vendor from the invoice.

        Returns:
            dict: A dictionary with the vendor's status ('approved' or 'not_found').
        """
        try:
            with open('./mock_data/mock_vendor_master.txt', 'r') as f:
                approved_vendors = [line.strip() for line in f.readlines()]
            
            if vendor_name in approved_vendors:
                return {"status": "approved", "message": f"Vendor '{vendor_name}' is approved."}
            else:
                return {"status": "not_found", "message": f"Vendor '{vendor_name}' is not in the master list."}
        except FileNotFoundError:
            return {"status": "error", "message": "Mock vendor master file not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    ```

4.  **Create `tools/action_tools.py` for the `AP_Action_Agent`**
    *   **Purpose & Business Value**: This toolset demonstrates the final, action-oriented phase of the process. It shows how Orchestrate can connect to external systems to complete the workflow, whether it's collaborating with humans via Slack for exceptions, triggering financial transactions in a payment gateway, or ensuring auditability by archiving documents. This closes the loop on the entire automated process, transforming it from a simple validation engine into a true end-to-end orchestration solution.
    ```python
    import json
    from datetime import datetime
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="send_slack_alert", description="Sends a formatted alert to a designated Slack channel for AP team review.", permission=ToolPermission.ADMIN)
    def send_slack_alert(invoice_id: str, reason: str, details: str) -> dict:
        """
        Sends a notification to the Accounts Payable team for exception handling.

        Args:
            invoice_id (str): The ID of the invoice requiring review.
            reason (str): The high-level reason for the alert (e.g., 'Amount Mismatch').
            details (str): A detailed message explaining the issue.

        Returns:
            dict: A confirmation of the action taken.
        """
        # This is a mock function. In a real scenario, it would use the Slack API.
        print(f"\n--- MOCK SLACK ALERT ---")
        print(f"To: #accounts-payable")
        print(f"Subject: [URGENT] Invoice Exception: {invoice_id}")
        print(f"Reason: {reason}")
        print(f"Details: {details}")
        print(f"------------------------\n")
        return {"status": "success", "message": f"Slack alert sent for invoice {invoice_id}."}

    @tool(name="trigger_payment", description="Initiates a payment transaction for a validated invoice.", permission=ToolPermission.ADMIN)
    def trigger_payment(invoice_id: str, vendor_name: str, amount: float) -> dict:
        """
        Triggers the financial transaction to pay a vendor for an approved invoice.

        Args:
            invoice_id (str): The invoice ID being paid.
            vendor_name (str): The name of the vendor to be paid.
            amount (float): The amount to be paid.

        Returns:
            dict: A dictionary with the transaction status and a confirmation number.
        """
        # This is a mock function. In a real scenario, it would call a payment gateway API.
        transaction_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "status": "success",
            "message": f"Payment of ${amount} to {vendor_name} for invoice {invoice_id} initiated.",
            "transaction_id": transaction_id
        }

    @tool(name="archive_invoice", description="Archives the processed invoice to a document management system.", permission=ToolPermission.ADMIN)
    def archive_invoice(invoice_id: str, status: str, transaction_id: str = None) -> dict:
        """
        Archives the invoice and its processing outcome for audit purposes.

        Args:
            invoice_id (str): The ID of the invoice to archive.
            status (str): The final status of the invoice (e.g., 'Paid', 'Rejected').
            transaction_id (str, optional): The payment transaction ID, if applicable.

        Returns:
            dict: A confirmation of the archival action.
        """
        # This is a mock function. In a real scenario, it would connect to a system like SharePoint or FileNet.
        archive_record = {
            "invoice_id": invoice_id,
            "status": status,
            "transaction_id": transaction_id,
            "archived_at": datetime.now().isoformat()
        }
        print(f"\n--- MOCK ARCHIVAL ---")
        print(f"Archived Record: {json.dumps(archive_record)}")
        print(f"---------------------\n")
        return {"status": "success", "message": f"Invoice {invoice_id} has been archived with status '{status}'."}
    ```

### Step 4: Define Agent Configurations (YAML)

Define the agents themselves using YAML files. The clarity of the `description` and `instructions` fields is paramount for the supervisor agent's ability to reason and delegate tasks correctly.

1.  **Create `agents/Invoice_Data_Agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: Invoice_Data_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialized agent that simulates a document processing system like Xerox. Its sole purpose is to receive an invoice identifier and use its tool to extract and return structured data from that invoice. It is the first step in the P2P workflow.
    instructions: >
      Your only function is to use the 'extract_invoice_details' tool when given an invoice ID. Return the results directly without interpretation or additional conversation.
    tools:
      - extract_invoice_details
    ```

2.  **Create `agents/ERP_Connector_Agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: ERP_Connector_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An agent that acts as a connector to the company's ERP system. It is equipped with tools to validate purchase orders against invoices and to check the status of vendors in the master vendor list. This agent is critical for financial validation and compliance checks.
    instructions: >
      Use the 'validate_po_match' tool to compare invoice amounts with PO data. Use the 'get_vendor_status' tool to verify if a vendor is approved. Provide clear, direct answers based on the tool outputs.
    tools:
      - validate_po_match
      - get_vendor_status
    ```

3.  **Create `agents/AP_Action_Agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: AP_Action_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An agent responsible for executing outbound actions. It can notify the Accounts Payable team of exceptions via Slack, trigger financial payments for approved invoices, and archive processed documents for compliance and auditing. This agent completes the workflow by interacting with external systems.
    instructions: >
      When asked to handle an exception, use the 'send_slack_alert' tool. When an invoice is fully approved, you must use the 'trigger_payment' tool first, and then use the 'archive_invoice' tool.
    tools:
      - send_slack_alert
      - trigger_payment
      - archive_invoice
    ```

4.  **Create `agents/P2P_Supervisor_Agent.yaml`** (The core orchestrator)
    ```yaml
    spec_version: v1
    kind: native
    name: P2P_Supervisor_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An agent that orchestrates the entire Procure-to-Pay lifecycle. It validates invoice data, handles exceptions, and coordinates with ERP, notification, and financial systems via its collaborator agents. It acts as the central brain for the P2P process.
    instructions: >
      Your purpose is to process invoices efficiently by following a strict workflow.
      1. When you receive an invoice ID, first use the Invoice_Data_Agent to extract its details.
      2. Next, use the ERP_Connector_Agent to perform two checks: verify if the vendor is approved AND if the invoice details match the Purchase Order.
      3. If the vendor is not approved, state that the new vendor onboarding process must be started and stop all further actions for this invoice.
      4. If the invoice and PO data do not match, use the AP_Action_Agent to send a Slack alert to the AP team with the invoice details and the specific discrepancy. Then, stop processing.
      5. If all data is validated successfully, use the AP_Action_Agent to first trigger the payment and then archive the invoice with a 'Paid' status. Report the final outcome, including the transaction ID.
    collaborators:
      - Invoice_Data_Agent
      - ERP_Connector_Agent
      - AP_Action_Agent
    knowledge_base:
      - procurement_policies
    ```

### Step 5: Deploy the Solution using the ADK CLI

With all artifacts created, use the `orchestrate` CLI to import them into your environment. The order of operations is critical: dependencies like tools and collaborator agents must be imported before the supervisor agent that uses them.

```bash
# Navigate to the root of your project directory (p2p-orchestration-demo)
cd /path/to/p2p-orchestration-demo

# Step 1: Import all Python tools. These are the foundational capabilities for the agents.
echo "Importing tools..."
orchestrate tools import -f tools/invoice_tools.py
orchestrate tools import -f tools/erp_tools.py
orchestrate tools import -f tools/action_tools.py

# Step 2: Import the knowledge base. This makes the policy documents available for queries.
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/procurement_policies.yaml

# Step 3: Import the collaborator agents. These must exist before the supervisor can be configured to use them.
echo "Importing collaborator agents..."
orchestrate agents import -f agents/Invoice_Data_Agent.yaml
orchestrate agents import -f agents/ERP_Connector_Agent.yaml
orchestrate agents import -f agents/AP_Action_Agent.yaml

# Step 4: Import the main supervisor agent last, after all its dependencies (tools, KB, collaborators) are registered.
echo "Importing supervisor agent..."
orchestrate agents import -f agents/P2P_Supervisor_Agent.yaml

# Step 5: Start the chat interface to begin the demo.
echo "Deployment complete. Starting chat..."
orchestrate chat start
```

## 4. Verification and Demo Scenarios

After running `orchestrate chat start`, a chat interface will open. Use the following prompts to demonstrate the three key scenarios, showcasing the supervisor's ability to handle different business logic paths.

*   **Scenario 1: The "Happy Path"**
    *   **User Prompt**: `Process invoice INV-1001`
    *   **Expected Outcome**: The supervisor will coordinate the agents. It will find that the vendor is approved and the amounts match. It will then trigger a mock payment and archive the invoice, reporting success with a transaction ID printed in the console and a confirmation message in the chat.

*   **Scenario 2: Exception - Data Mismatch**
    *   **User Prompt**: `Process invoice INV-1002`
    *   **Expected Outcome**: The supervisor will find the vendor is approved but will detect a mismatch between the invoice amount ($1250.75) and the PO amount ($1200.00). It will invoke the `AP_Action_Agent` to send a mock Slack alert (printed to the console) with the details of the discrepancy and will report this action in the chat.

*   **Scenario 3: Exception - New Vendor**
    *   **User Prompt**: `Process invoice INV-1003`
    *   **Expected Outcome**: The supervisor will use the `ERP_Connector_Agent` and discover that "Creative Design Co." is not on the approved vendor list. It will halt the process and respond with a message indicating that the new vendor onboarding workflow must be initiated, as per its instructions.

*   **Bonus Scenario: Knowledge Base Query**
    *   **User Prompt**: `What is the policy for handling large invoices?`
    *   **Expected Outcome**: The agent will query the `procurement_policies` knowledge base and respond with the information from the PDF about the $50,000 approval threshold.

## 5. Troubleshooting

*   **Tool Import Fails**:
    *   **Issue**: `orchestrate tools import` command fails.
    *   **Solution**: Check for syntax errors in the Python files (`.py`). Ensure all required packages from `requirements.txt` are installed in your Python environment (`pip install -r requirements.txt`). Verify that the `@tool` decorator is correctly used with all required arguments.
*   **Agent Import Fails**:
    *   **Issue**: `orchestrate agents import` command fails, often with a "collaborator not found" or "tool not found" error.
    *   **Solution**: Ensure you are importing assets in the correct order as shown in the Step 5 script: tools first, then knowledge bases, then collaborator agents, and finally the supervisor agent. Check for YAML syntax errors and verify that all `tools`, `collaborators`, and `knowledge_base` names in the YAML files exactly match the names of the imported assets.
*   **Agent Does Not Follow Instructions**:
    *   **Issue**: The supervisor agent doesn't call the correct collaborator or performs steps out of order.
    *   **Solution**: The `instructions` in the `P2P_Supervisor_Agent.yaml` are critical. Make them more explicit and prescriptive. Using a numbered list (1, 2, 3...) as shown in the example provides clear, sequential logic for the LLM to follow. Also, ensure the `description` fields for the collaborator agents are very clear and action-oriented, as the supervisor uses these to decide which agent to route tasks to.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
