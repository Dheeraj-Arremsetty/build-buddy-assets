#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python**: Python 3.9 or higher is required.
*   **Project Structure**: Create a dedicated project directory to organize your files.
    ```bash
    mkdir financial_insights_engine
    cd financial_insights_engine
    mkdir -p agents tools knowledge_base/documents
    ```
*   **Orchestrate Environment**: You must be logged into your IBM watsonx Orchestrate environment via the CLI.
    ```bash
    # Log in to your Orchestrate environment (follow the prompts)
    orchestrate login

    # Set the active environment for your project
    orchestrate env set <your_environment_name>
    ```
*   **Text Editor**: A code editor like Visual Studio Code is recommended for editing Python and YAML files.

## 3. Step-by-Step Instructions

### Step 1: Create the Knowledge Base and Mock Financial Documents

The foundation of our RAG (Retrieval-Augmented Generation) pattern is a secure knowledge base containing the client's financial documents. We will create mock documents and a knowledge base definition to ingest them.

**A. Create Mock Financial Documents**

First, we will create two sample text files representing quarterly financial reports. Place these files in the `knowledge_base/documents/` directory.

**File: `knowledge_base/documents/Q1_2024_Financial_Report.txt`**

