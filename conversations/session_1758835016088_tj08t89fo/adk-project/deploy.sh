#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Active Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. Verify your setup by running:
    ```bash
    orchestrate env show
    ```
4.  **Required Python Packages**: The custom tools in this demo rely on external packages. A `requirements.txt` file will be created to manage these dependencies.
5.  **Text Editor**: A text editor or IDE (like Visual Studio Code) is needed to create and edit Python and YAML files.

## Step 1: Project Setup

First, create a structured directory for all the demo assets. This organization is crucial for managing agents, tools, and knowledge base documents effectively.

1.  Open your terminal or command prompt.
2.  Create the main project directory and navigate into it.

    ```bash
    mkdir empower-demo
    cd empower-demo
    ```

3.  Create the necessary subdirectories for agents, tools, and knowledge base documents.

    ```bash
    mkdir agents tools knowledge_base_docs
    mkdir tools/customer_care tools/service_now
    ```

4.  Create placeholder documents for the knowledge base. These files will be ingested by Orchestrate to answer policy-related questions.

    ```bash
    # Create a dummy employee handbook
    echo "Our company offers tuition reimbursement up to $5,000 per year for approved courses. To be eligible, employees must be full-time and have completed at least one year of service. All courses must be related to the employee's current role or a potential future role within the company. Approval from the employee's manager is required before enrollment." > knowledge_base_docs/Employee_Handbook.txt

    # Create a dummy IT policy document (can be any format like .pdf, .txt, .docx)
    echo "To reset your password, please open a high-priority ticket with the IT department using the 'create ticket' command. For urgent system-wide outages, please contact the IT helpdesk directly via phone." > knowledge_base_docs/IT_Policy.txt
    ```

5.  Create a `requirements.txt` file to list the Python dependencies for our custom tools.

    ```bash
    touch requirements.txt
    ```
    Open `requirements.txt` and add the following packages:
    ```text
    requests
    pydantic
    ```
6.  Install the dependencies from the project's root directory.
    ```bash
    pip install -r requirements.txt
    ```

Your project structure should now look like this:

