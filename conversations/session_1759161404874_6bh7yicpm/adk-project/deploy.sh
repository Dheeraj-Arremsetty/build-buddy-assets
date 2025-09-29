#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have a configured IBM watsonx Orchestrate environment (either cloud or local developer edition). Initialize and activate your environment using the CLI:
    ```bash
    # Configure your environment (run once)
    orchestrate env add

    # Activate your environment for the current session
    orchestrate env use <your_environment_name>
    ```
4.  **Project Directory**: Create a dedicated directory to organize all the files for this demo. A structured layout is essential for managing agents, tools, and dependencies.
    ```bash
    mkdir finsecure_demo
    cd finsecure_demo
    mkdir agents
    mkdir tools
    ```

## Step 1: Create Project Dependencies

To ensure the Python-based tools have access to necessary libraries, we will define them in a `requirements.txt` file. This file lists all external packages that our tools depend on.

### Business Value
Defining dependencies in a `requirements.txt` file is a standard best practice that ensures reproducibility and simplifies deployment. It guarantees that the tools will run consistently across different environments by installing the exact libraries they were developed with.

### `requirements.txt` File
Create the following file in the root of your `finsecure_demo` directory. For this demo, we will use the `requests` library to simulate API calls and `python-dotenv` for managing environment variables, which is a good practice for future extensions.

**File:** `finsecure_demo/requirements.txt`

# Script block 2
pip install -r requirements.txt

