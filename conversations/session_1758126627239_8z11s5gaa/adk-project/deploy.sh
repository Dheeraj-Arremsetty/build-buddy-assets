#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
2.  **Python Environment**: A Python 3.9+ environment is required to run the mock Salesforce API and execute the Python-based tool.
3.  **Project Directory**: Create a dedicated project directory to organize all configuration files, tools, and mock data.
    ```bash
    mkdir xerox_sales_copilot
    cd xerox_sales_copilot
    mkdir agents tools mock_docs
    ```
4.  **Python Libraries**: Install the necessary Python libraries for the mock API.
    ```bash
    pip install Flask
    ```
5.  **`requirements.txt` file**: Create a `requirements.txt` file in the root of your project directory for dependency management.
    ```text
    # requirements.txt
    ibm-watsonx-orchestrate
    Flask
    ```

## Step 1: Create Mock Data and Services

To simulate a real-world enterprise environment, we will create mock service documents for the knowledge base and a mock Salesforce REST API for customer data retrieval.

### 1.1. Create Mock Service Catalog Documents
These documents will be ingested into a watsonx Orchestrate knowledge base, allowing the `Proposal_Generation_Agent` to perform semantic searches for service details.

**File: `mock_docs/Managed_Print_Services.pdf`**
(Create a simple PDF document with the following text)
> **Xerox Managed Print Services (MPS)**
> Our comprehensive MPS solution streamlines print operations, reduces costs, and enhances document security.
> **Features:**
> -   Automated supply replenishment
> -   Proactive device monitoring and maintenance
> -   Fleet optimization and right-sizing
> -   Secure print release and access control
> **Pricing Tiers:**
> -   Standard: $50/user/month
> -   Premium: $75/user/month (includes advanced security)

**File: `mock_docs/IT_Outsourcing_Solutions.txt`**
> **Xerox IT Outsourcing (ITO) Solutions**
> We provide end-to-end IT management, allowing you to focus on your core business.
> **Services Offered:**
> -   24/7 Help Desk and Technical Support
> -   Network Infrastructure Management
> -   Cloud Services and Migration
> -   Cybersecurity and Compliance
> **Standard Terms:** 12-month minimum contract.

**File: `mock_docs/Digital_Transformation_Services.txt`**
> **Xerox Digital Transformation Services**
> Accelerate your digital journey with our expert consulting and implementation services.
> **Capabilities:**
> -   Workflow Automation and Process Re-engineering
> -   Document Digitization and Management
> -   Custom Application Development
> -   Data Analytics and Business Intelligence

### 1.2. Create the Mock Salesforce API
This simple Flask application will simulate a Salesforce REST API, serving customer data. This is essential for demonstrating the `Salesforce_Data_Agent`'s ability to connect to external systems via OpenAPI.

**File: `tools/mock_salesforce_api.py`**

# Script block 2
python mock_salesforce_api.py

# Script block 3
orchestrate knowledge-bases import -f xerox_kb.yaml

# Script block 4
orchestrate tools import -f tools/salesforce_api.openapi.yaml

# Script block 5
orchestrate tools import -k python -f tools/proposal_tool.py

# Script block 6
# Import Collaborator Agents
orchestrate agents import -f agents/salesforce_agent.yaml
orchestrate agents import -f agents/proposal_agent.yaml

# Import the Supervisor Agent
orchestrate agents import -f agents/xerox_sales_copilot.yaml

# Script block 7
orchestrate chat start

