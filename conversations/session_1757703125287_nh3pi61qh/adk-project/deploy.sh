#!/bin/bash
# Generated deployment script

# Script block 1
pip install --upgrade ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required to create the custom tools.
3.  **Project Directory**: Create a dedicated project directory to organize all your files. This structure is crucial for managing agents, tools, and knowledge bases effectively.
    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir -p agents tools knowledge_base
    ```
4.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. If you have not already done so, initialize your environment and log in.
    ```bash
    # Initialize your environment (run only once)
    orchestrate env init

    # Log in to your environment
    orchestrate login
    ```
5.  **Text Editor**: A code editor like Visual Studio Code is recommended for creating and editing the YAML and Python files.

## Step 1: Create the Knowledge Base
The knowledge base will serve as the foundation for answering general employee questions, such as company policies and FAQs. This demonstrates the Retrieval-Augmented Generation (RAG) capabilities of watsonx Orchestrate, providing grounded, accurate answers from trusted company documents.

### 1.1. Create the Source Document
First, create a sample text file containing common employee questions. This file will be ingested into the built-in Milvus vector database.

**File:** `knowledge_base/employee_faq.txt`

