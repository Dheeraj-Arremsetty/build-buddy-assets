#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[all]"
    ```
2.  **Python Environment:** A working Python environment (version 3.10 or later) is required to create the custom tools.
3.  **Orchestrate Environment:** You must have an active watsonx Orchestrate environment configured. Use the following command to set up and activate your environment.
    ```bash
    # Configure your environment (run once)
    orchestrate env add
    
    # Activate your environment for the current session
    orchestrate env use <your_environment_name>
    ```
4.  **Project Directory:** Create a dedicated directory to organize all demo assets.
    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir agents tools knowledge_docs
    ```

---

## Step 1: Create the Knowledge Base for Company Policies

To enable the "Empower" agent to answer general policy and procedure questions, we will create a knowledge base from internal documents. This demonstrates Retrieval-Augmented Generation (RAG), allowing the agent to provide accurate answers based on trusted company sources.

### 1.1. Create Mock Documents
First, create mock FAQ and benefits documents inside the `knowledge_docs` directory.

**File: `knowledge_docs/employee_faq.txt`**

# Script block 2
orchestrate knowledge-bases import -f empower_kb.yaml

# Script block 3
orchestrate tools import -k python -f tools/get_healthcare_benefits.py

