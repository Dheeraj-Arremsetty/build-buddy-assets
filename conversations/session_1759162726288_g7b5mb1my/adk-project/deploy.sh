#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A Python version of 3.10 or higher is required. It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **watsonx Orchestrate Environment Configuration**: You must have an active watsonx Orchestrate environment configured with the ADK. This involves initializing the environment and logging in.
    ```bash
    # Initialize your environment (follow the prompts)
    orchestrate env init

    # Set your environment as active
    orchestrate env use <your_env_name>
    ```
4.  **Project Directory**: Create a dedicated directory for this demo to keep all files organized.
    ```bash
    mkdir global_finance_corp_demo
    cd global_finance_corp_demo
    mkdir agents tools docs
    ```

## Step 1: Create Project Structure and Dependencies

We will start by defining the project's file structure and the necessary Python dependencies. This ensures a clean and manageable workspace.

1.  **Create `requirements.txt`**: This file will list all the Python packages our custom tools depend on.
    ```bash
    # Create the requirements.txt file in the root of your project directory
    touch requirements.txt
    ```
    Add the following content to `requirements.txt`. These packages are used for making HTTP requests and handling environment variables, which are common patterns in tool development.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
2.  **Install Dependencies**: Install the packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Step 2: Create and Import the Knowledge Base

The knowledge base will provide the primary agent with contextual information about Global Finance Corp's internal lending policies. This enables the agent to answer policy-related questions without needing a specific tool.

1.  **Create a Mock Policy Document**: Create a simple text file that will act as our knowledge source. In a real-world scenario, this would be a comprehensive PDF or Word document.
    Save the following content as `docs/lending_policies.txt`:
    ```text
    # Global Finance Corp - Internal Lending Policies v2.1

    ## Personal Loans
    - Minimum Credit Score: 680
    - Maximum Debt-to-Income (DTI) Ratio: 40%
    - Maximum Loan Amount: $50,000
    - Required Documents: Proof of income (last 2 pay stubs), Government-issued ID.

    ## Mortgage Loans
    - Minimum Credit Score: 720
    - Maximum Debt-to-Income (DTI) Ratio: 43%
    - Minimum Down Payment: 10% of property value
    - Required Documents: Proof of income (2 years of tax returns), Bank statements (last 3 months), Government-issued ID, Property appraisal report.

    ## Loan Review Process
    All applications undergo a mandatory 4-step review: Data Validation, Risk Analysis, Compliance Check (KYC/AML), and Final Decision. High-risk applications require manual review by a senior underwriter.
    ```

2.  **Create the Knowledge Base YAML Configuration**: This file defines the knowledge base for Orchestrate, pointing to our policy document.
    Save the following content as `knowledge_base.yaml` in the root directory:
    ```yaml
    # knowledge_base.yaml
    spec_version: v1
    kind: knowledge_base
    name: loan_policy_kb
    description: >
      Contains internal lending policies for Global Finance Corp, including minimum credit scores,
      debt-to-income (DTI) ratio limits, and required documentation for personal and mortgage loans.
      Use this to answer questions about the company's lending criteria and processes.
    documents:
      - "docs/lending_policies.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

3.  **Import the Knowledge Base**: Use the ADK CLI to import the knowledge base into your Orchestrate environment.
    ```bash
    orchestrate knowledge-bases import -f knowledge_base.yaml
    ```

## Step 3: Create the Custom Tools

Now, we will create the Python-based tools for each specialized agent. Each tool simulates an action, such as fetching data or performing a calculation, and returns realistic synthetic data.

### 3.1 Data Validation Tools

These tools are used by the `DataValidation` agent to gather and verify applicant information.

**Business Value**: Automating data collection from disparate sources significantly reduces the time and potential for human error involved in manual data entry and verification. It ensures that the rest of the process is based on accurate, up-to-date information.

Save the following code as `tools/data_validation_tools.py`:

