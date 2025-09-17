#!/bin/bash
# Generated deployment script

# Script block 1
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

