#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
*   **Python Environment**: A working Python environment (version 3.9 or later) is required to create the custom tools.
*   **Configured Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured and logged in via the ADK CLI. This connects your local development to your Orchestrate instance.
    ```bash
    # Log in to your watsonx Orchestrate environment
    orchestrate login
    ```
*   **Project Directory**: Create a dedicated directory for the demo project to keep all files organized.
    ```bash
    mkdir barista_demo
    cd barista_demo
    mkdir agents tools
    ```

## 3. Step-by-Step Instructions

This plan is divided into four main steps: creating the dependencies file, building the individual Python tools, defining the agent's logic in a YAML file, and finally, importing everything into watsonx Orchestrate to bring the Virtual Barista to life.

### Step 3.1: Create Project Dependencies

Our Python tools will use the `pydantic` library for data validation and structuring, which is a best practice for creating robust tools in Orchestrate. Create a `requirements.txt` file in the root of your `barista_demo` directory to manage this dependency.

Create the file `requirements.txt`:

# Script block 2
pip install -r requirements.txt

