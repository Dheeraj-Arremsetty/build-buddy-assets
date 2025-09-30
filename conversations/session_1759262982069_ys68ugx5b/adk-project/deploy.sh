#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Project Directory Structure**: Create a dedicated folder for the demo assets to maintain organization.
    ```bash
    mkdir financial_compliance_demo
    cd financial_compliance_demo
    mkdir agents
    mkdir tools
    ```
4.  **Python Dependencies**: The Python tools will require external libraries. Create a `requirements.txt` file in the root of your `financial_compliance_demo` directory with the following content.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
    Install these dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
5.  **watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured with the ADK. Follow the official documentation to log in and set up your environment using the CLI.

## Step 1: Develop the Python Tools
The foundation of our automation is a set of powerful, modular Python tools. Each tool simulates a specific action within the compliance workflow, from data collection to report generation. We will create each tool in its own file within the `tools/` directory.

### 1.1 Data Ingestion Tools

#### `collect_swift_transactions.py`
**Business Value**: This tool simulates the critical first step of the compliance process: gathering raw transaction data from the SWIFT network. By automating this data collection, the client can ensure that all international transactions are captured in near real-time, eliminating manual data entry, reducing the risk of missed transactions, and providing a timely and complete dataset for downstream analysis.

**Technical Implementation**: The tool generates a list of synthetic SWIFT MT103 messages. It uses Python's `random` and `datetime` libraries to create realistic-looking transaction details, including unique IDs, sender/receiver BIC codes, amounts, currencies, and timestamps. This provides a dynamic and varied dataset for each demo run. The output is a JSON-serializable list of dictionaries, a standard format easily consumed by other tools and agents.

