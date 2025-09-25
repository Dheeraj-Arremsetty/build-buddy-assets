#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A Python 3.9+ environment is required. It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv orchestrate-demo-env
    source orchestrate-demo-env/bin/activate
    ```
3.  **Project Directory Structure**: Create a structured directory to organize all artifacts for the demo.
    ```bash
    mkdir -p finsecure_demo/{agents,tools,knowledge_base/docs}
    cd finsecure_demo
    ```
4.  **Required Python Packages**: Create a `requirements.txt` file in the root of your `finsecure_demo` directory. This demo will use the `requests` library for potential future API calls, though the mock data is self-contained.
    ```text
    # requirements.txt
    requests
    ```
    Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Orchestrate CLI Login**: Ensure you are logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```

## Step 1: Create the Knowledge Base
To ground the `Risk Analysis Agent` in FinSecure Capital's specific compliance landscape, we will create a knowledge base. This will contain mock regulatory documents and internal policy guidelines, allowing the agent to perform more accurate, context-aware analysis.

### 1.1. Create Mock Documents
Create two text files inside the `knowledge_base/docs/` directory.

**`knowledge_base/docs/internal_policy_v1.txt`**:

