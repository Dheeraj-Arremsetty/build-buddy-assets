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