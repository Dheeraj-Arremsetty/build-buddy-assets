#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required to create the custom tools.
3.  **Project Directory Structure**: Create a dedicated directory for the project to keep all artifacts organized.
    ```bash
    mkdir fincorp_orchestrate_demo
    cd fincorp_orchestrate_demo
    mkdir agents tools knowledge_base_docs
    ```
4.  **Environment Initialization**: You must have an active watsonx Orchestrate environment initialized. Follow the ADK documentation to log in and set up your environment.
    ```bash
    # Follow prompts to log in and select your environment
    orchestrate login
    orchestrate env init
    ```
5.  **Python Dependencies**: Create a `requirements.txt` file for any third-party libraries used in the custom tools.
    ```bash
    # Create the requirements.txt file
    echo "requests" > requirements.txt

    # Install the dependencies
    pip install -r requirements.txt
    ```

## Step 1: Create the Knowledge Base

The **Compliance Check Agent** will use a knowledge base to verify transactions against a set of financial regulations. This step involves creating a mock regulatory document and a YAML configuration to import it into Orchestrate's built-in vector store.

### 1.1. Create the Regulatory Document

First, create a simple text file containing mock financial regulations. This document will be ingested into the knowledge base.

**Command:** Create the file `knowledge_base_docs/fincorp_regulations.txt`.

# Script block 2
orchestrate knowledge-bases import -f knowledge_base_config.yaml

