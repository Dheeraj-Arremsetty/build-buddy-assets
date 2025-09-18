#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[all]"
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment configured. Initialize it if you haven't already:
    ```bash
    orchestrate setup
    ```
*   **Python Libraries:** The custom tools will require the `pandas` library for data manipulation. It will be listed in a `requirements.txt` file.
*   **Text Editor:** A text editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## 3. Project Structure Setup

To maintain clarity and organization, create the following directory structure for the project. This structure separates agents, tools, data, and knowledge base assets, making the project easy to manage and scale.

# Script block 2
# Import the dataset locator tool
    orchestrate tools import -f ./tools/dataset_locator_tools.py

    # Import the data validator tool
    orchestrate tools import -f ./tools/data_validator_tools.py -r ./requirements.txt
    ```

2.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f ./knowledge_base/ValidationRulesKB.yaml
    ```

3.  **Import the Collaborator Agents:**
    ```bash
    # Import the locator agent
    orchestrate agents import -f ./agents/DatasetLocatorAgent.yaml

    # Import the validator agent
    orchestrate agents import -f ./agents/DataValidatorAgent.yaml
    ```

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f ./agents/ValidationSupervisorAgent.yaml
    ```

## 5. Verification and Demo Scenarios

After successfully importing all assets, you can start an interactive chat session to test the demo scenarios.

**Start the Chat:**

