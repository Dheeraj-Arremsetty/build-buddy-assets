#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
2.  **Active Environment**: You must have an active watsonx Orchestrate environment (either cloud or local Developer Edition). Activate your environment using the CLI.
    ```bash
    orchestrate env activate <your_env_name>
    ```
3.  **Python 3.8+**: A compatible version of Python is required to create the custom tools.
4.  **Project Directory**: Create a dedicated directory to organize all your files for this demo.
    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir agents tools knowledge_base
    ```
5.  **Required Python Libraries**: Create a `requirements.txt` file in your root `empower-demo` directory. The tools will use the `requests` library for simulated API calls.
    ```text
    # requirements.txt
    requests
    ```
    Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Step 1: Create the Tools

Tools are the foundational components that allow agents to perform actions. We will create two sets of Python-based tools: one for customer care (healthcare/benefits) and one for IT support (ServiceNow).

### 1.1 Customer Care Tools

These tools, as detailed in the reference material, simulate interactions with a healthcare benefits system.

#### **File: `tools/customer_care_tools.py`**

This file will contain all three customer care tools for simplicity.

**Business Value**: These tools automate the retrieval of complex benefits, claims, and provider information, empowering employees to self-serve their healthcare inquiries 24/7. This reduces calls to the HR department and improves employee satisfaction by providing immediate answers.

