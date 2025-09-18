# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 15:45:19
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Data Steward Assistant

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an **AI-Powered Data Steward Assistant** for the client using IBM watsonx Orchestrate. This solution is meticulously designed to address the client's need for an on-demand, conversational interface to automate complex data quality, validation, and cleansing tasks, directly aligning with their strategic focus on Data Processing, AI/ML, and Automation.

The proposed multi-agent system features a **Data Steward Supervisor** that intelligently orchestrates tasks among specialized collaborator agents. This empowers non-technical business analysts to perform sophisticated data quality checks on enterprise datasets through simple, natural language commands. This plan details the creation of the supervisor agent, its collaborators for data ingestion, validation, and reporting, the Python-based tools that grant them their skills, and a knowledge base of business rules. The final solution will demonstrably reduce data validation cycle times, minimize human error, and significantly improve the trustworthiness of data used for critical business analytics.

## Prerequisites

Before beginning, ensure your development environment is correctly configured to meet the requirements of the IBM watsonx Orchestrate Agent Development Kit (ADK).

1.  **Python**: Python version 3.8 or higher must be installed on your system.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If not, run the following command in your terminal:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
3.  **watsonx Orchestrate Environment**: You must have an active IBM watsonx Orchestrate environment initialized and configured with the ADK. Ensure you have logged in and set the target environment.
4.  **Required Python Packages**: The tools in this plan require external Python libraries. You will create a `requirements.txt` file and install them to ensure the tools function correctly.
5.  **Text Editor**: A code editor such as Visual Studio Code is highly recommended for creating and editing the Python and YAML files required for this project.

## Step 1: Prepare the Project Structure and Mock Data

A well-organized project structure is essential for managing the different components of the solution and ensuring scalability.

### 1.1. Create the Directory Structure

Create the following folder structure in your development environment. This separates agents, tools, knowledge bases, and data, making the project easy to navigate and maintain.

```
data_steward_demo/
├── agents/
│   ├── data_ingestion_agent.yaml
│   ├── data_validation_agent.yaml
│   ├── reporting_agent.yaml
│   └── data_steward_supervisor.yaml
├── tools/
│   ├── ingestion_tools.py
│   ├── validation_tools.py
│   └── reporting_tools.py
├── knowledge_bases/
│   └── data_quality_kb.yaml
├── mock_data/
│   ├── customer_records_q3.csv
│   └── data_quality_rules.pdf
└── requirements.txt
```

### 1.2. Create Mock Data Files

Populate the `mock_data` directory with synthetic data that simulates the client's real-world scenarios, including common data quality issues.

1.  **`customer_records_q3.csv`**: Create this file inside `mock_data/` with intentional errors.

    ```csv
    CustomerID,FirstName,LastName,Email,PhoneNumber,State
    CUST-001,John,Doe,john.doe@email.com,(123) 456-7890,CA
    CUST-002,Jane,Smith,,555-1234,NY
    CUST-003,Peter,Jones,peter.jones@email.com,(321) 654-0987,Calif.
    CUST-004,Mary,Williams,mary.w@invalid,123-456-7890,TX
    CUST-005,David,Brown,david.brown@email.com,(555) 876-5432,FL
    CUST-001,John,Doe,john.doe@email.com,(123) 456-7890,CA
    CUST-006,Susan,Miller,susan.miller@email.com,,Nevada
    ```

2.  **`data_quality_rules.pdf`**: Create a simple PDF document containing the official data standards. The content below can be saved into a text file and then converted to a PDF. This document will be ingested by the knowledge base.

    ```text
    Official Corporate Data Quality Standards

    1. Phone Number Format: All phone numbers must be in the format (XXX) XXX-XXXX.
    2. State Abbreviations: All state fields must use the 2-letter postal abbreviation (e.g., CA, NY, TX).
    3. Mandatory Fields: Every customer record must have a unique CustomerID and a valid email address.
    4. Email Validation: Emails must follow standard format conventions (e.g., user@domain.com).
    ```

### 1.3. Create the `requirements.txt` file

Create a `requirements.txt` file in the root of the `data_steward_demo` directory. The tools will use these packages.

```text
pandas
pydantic
requests
```

Install these packages using pip:
```bash
pip install -r requirements.txt
```

## Step 2: Create the Knowledge Base

The knowledge base allows the `Data_Validation_Agent` to dynamically access and apply the company's official data standards without hard-coding them into the agent's logic.

**Business Value:** By externalizing business rules into a knowledge base, the solution becomes more flexible and maintainable. Business analysts can update the `data_quality_rules.pdf` document, and the agent will automatically adopt the new rules without requiring any code changes, ensuring agility and adherence to evolving standards.

### `knowledge_bases/data_quality_kb.yaml`

Create the YAML configuration file for the knowledge base. This configuration points to the PDF document and uses a built-in vector index with a default IBM embedding model to make the content searchable.

```yaml
spec_version: v1
kind: knowledge_base
name: data_quality_kb
description: >
   Contains the official corporate data standards and validation rules for customer records, including required formats for phone numbers, emails, addresses, and state abbreviations.
documents:
   - "mock_data/data_quality_rules.pdf"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Develop the Python Tools for Collaborator Agents

Tools are the functional building blocks that enable agents to perform actions. We will create three sets of tools, each in its own Python file, corresponding to the capabilities of our collaborator agents.

### 3.1. Ingestion Tools (`tools/ingestion_tools.py`)

These tools are responsible for connecting to and retrieving data from various sources.

#### `read_csv_file` Tool
**Business Value:** This tool empowers the agent to work with one of the most common data exchange formats (CSV), enabling it to ingest batch data from file systems, data lakes, or user uploads. This is a foundational capability for any data processing workflow.
**Technical Implementation:** The tool takes a file path as input. It uses the `pandas` library for robust CSV parsing and error handling. Crucially, it converts the DataFrame into a list of dictionaries before returning, ensuring the output is a simple, JSON-serializable format that Orchestrate agents can easily process and pass to other agents.

#### `fetch_from_api` Tool
**Business Value:** This tool provides the agent with the ability to integrate with modern, real-time data sources via REST APIs. This is essential for validating data against live enterprise systems, such as a customer master database or a product catalog, ensuring data quality checks are based on the most current information.
**Technical Implementation:** This function simulates fetching data from a customer API endpoint. It demonstrates how to handle API responses and transform JSON data into the standardized list-of-dictionaries format used across the agent system. It includes mock data representing a typical API response.

```python
# tools/ingestion_tools.py
import pandas as pd
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a CSV file from the given path and returns its content as a list of records.

    Args:
        file_path (str): The full path to the CSV file to be read.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a row from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        # Convert NaN to None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        return df.to_dict('records')
    except FileNotFoundError:
        return [{"error": f"File not found at path: {file_path}"}]
    except Exception as e:
        return [{"error": f"An error occurred while reading the file: {str(e)}"}]

@tool(permission=ToolPermission.ADMIN)
def fetch_from_api(endpoint_url: str) -> List[Dict[str, Any]]:
    """
    Fetches customer data from a mock API endpoint.

    Args:
        endpoint_url (str): The URL of the API endpoint to fetch data from.

    Returns:
        List[Dict[str, Any]]: A list of customer records retrieved from the API.
    """
    # This is a mock implementation. In a real scenario, you would use the 'requests' library.
    print(f"Fetching data from mock API: {endpoint_url}")
    mock_api_data = [
        {"CustomerID": "API-101", "FirstName": "Alice", "LastName": "Johnson", "Email": "alice.j@email.com", "PhoneNumber": "(777) 111-2222", "State": "GA"},
        {"CustomerID": "API-102", "FirstName": "Bob", "LastName": "Williams", "Email": "bob.w@email.com", "PhoneNumber": "(888) 333-4444", "State": "WA"}
    ]
    return mock_api_data
```

### 3.2. Validation Tools (`tools/validation_tools.py`)

These tools form the core of the data quality engine, applying specific validation rules to datasets.

#### `check_missing_values` Tool
**Business Value:** This tool automates one of the most fundamental data quality checks: identifying incomplete records. By quickly flagging records with missing information in critical fields (like emails or phone numbers), it enables the business to prioritize data enrichment efforts and prevent operational issues caused by incomplete data.
**Technical Implementation:** The function iterates through a list of records and checks if the specified column has a null or empty value. It returns a new list containing only the records that fail this check, providing a clear and actionable result set.

#### `validate_phone_number_format` Tool
**Business Value:** Enforcing standard data formats is crucial for system interoperability and analytics consistency. This tool validates phone numbers against a specific corporate standard, preventing data entry errors and ensuring that data can be reliably used by communication platforms, CRMs, and marketing automation tools.
**Technical Implementation:** This tool uses a regular expression (`regex`) to match the phone number string against the required `(XXX) XXX-XXXX` format. Regular expressions provide a powerful and efficient way to enforce complex string patterns, making the tool both accurate and performant.

#### `verify_against_rules` Tool
**Business Value:** This advanced tool allows for dynamic, rule-based validation. Instead of hard-coding logic, it interprets a natural language rule (e.g., from the knowledge base) and applies the corresponding check. This makes the agent highly adaptable, allowing it to enforce new business rules without code changes, which is a significant advantage for agile business environments.
**Technical Implementation:** The tool accepts a dataset and a string describing the rule. It contains internal logic to map rule descriptions (like "phone number format") to specific validation functions. This acts as a simple routing mechanism within the tool, showcasing how an agent can perform complex, multi-step reasoning. For production, this could be expanded to a more robust dictionary-based mapping of rules to functions.

```python
# tools/validation_tools.py
import re
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def check_missing_values(records: List[Dict[str, Any]], column_name: str) -> List[Dict[str, Any]]:
    """
    Checks for missing or empty values in a specified column of the provided records.

    Args:
        records (List[Dict[str, Any]]): A list of records (dictionaries) to check.
        column_name (str): The name of the column to check for missing values.

    Returns:
        List[Dict[str, Any]]: A list of records that have a missing value in the specified column.
    """
    missing_records = []
    for record in records:
        if record.get(column_name) is None or str(record.get(column_name)).strip() == '':
            missing_records.append(record)
    return missing_records

@tool(permission=ToolPermission.ADMIN)
def validate_phone_number_format(phone_number: str) -> bool:
    """
    Checks if a phone number matches the standard corporate format (XXX) XXX-XXXX.

    Args:
        phone_number (str): The phone number string to validate.

    Returns:
        bool: True if the format is valid, False otherwise.
    """
    if not isinstance(phone_number, str):
        return False
    pattern = re.compile(r'^\(\d{3}\) \d{3}-\d{4}$')
    return bool(pattern.match(phone_number))

@tool(permission=ToolPermission.ADMIN)
def verify_against_rules(records: List[Dict[str, Any]], rule_description: str) -> List[Dict[str, Any]]:
    """
    Verifies records against a described data quality rule. Identifies records that violate the rule.

    Args:
        records (List[Dict[str, Any]]): The dataset to validate.
        rule_description (str): A natural language description of the rule to apply. e.g., 'Check for invalid phone number format'.

    Returns:
        List[Dict[str, Any]]: A list of records that violate the specified rule.
    """
    invalid_records = []
    if "phone number format" in rule_description.lower():
        for record in records:
            phone = record.get("PhoneNumber")
            if phone and not validate_phone_number_format(phone):
                invalid_records.append(record)
    elif "missing email" in rule_description.lower():
        return check_missing_values(records, "Email")
    # This logic can be expanded with more rules.
    else:
        return [{"error": f"Rule '{rule_description}' is not implemented."}]
        
    return invalid_records
```

### 3.3. Reporting Tools (`tools/reporting_tools.py`)

This tool is dedicated to formatting and presenting the results of data quality checks in a clear, human-readable format.

#### `generate_summary_report` Tool
**Business Value:** The final step of any data quality process is communicating the findings. This tool transforms raw lists of data errors into a clean, formatted summary table. This allows business users to quickly understand the scope of data issues and take action, bridging the gap between automated analysis and human decision-making.
**Technical Implementation:** The function takes a list of identified issues (dictionaries) and a title for the report. It dynamically constructs a GitHub-flavored Markdown table as a string. This format is lightweight and renders well in most chat interfaces, providing a universally accessible way to present tabular data.

```python
# tools/reporting_tools.py
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def generate_summary_report(title: str, issues_data: List[Dict[str, Any]]) -> str:
    """
    Generates a formatted summary report of data quality issues in a markdown table.

    Args:
        title (str): The title for the summary report.
        issues_data (List[Dict[str, Any]]): A list of dictionaries, where each dictionary represents a data quality issue or record.

    Returns:
        str: A string containing the formatted markdown report.
    """
    if not issues_data:
        return f"## {title}\n\nNo issues found."

    headers = issues_data[0].keys()
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    rows = []
    for item in issues_data:
        row_values = [str(item.get(h, '')).replace('\n', ' ').replace('|', ' ') for h in headers]
        rows.append("| " + " | ".join(row_values) + " |")

    report = f"## {title}\n\n" + "\n".join([header_line, separator_line] + rows)
    return report
```

## Step 4: Define the Agent Configurations (YAML)

With the tools defined, we now configure the agents that will use them. Each agent has a specific role, and its YAML file defines its identity, capabilities, and instructions.

### 4.1. Data Ingestion Agent (`agents/data_ingestion_agent.yaml`)

**Role:** This is a specialized collaborator agent focused solely on data retrieval. Its well-defined scope makes it a reusable component for any workflow that needs to read files or call APIs.
**Configuration:** The `description` clearly states its purpose. The `tools` list explicitly grants it access to `read_csv_file` and `fetch_from_api`, limiting its capabilities to prevent it from performing tasks outside its designated function.

```yaml
spec_version: v1
kind: native
name: data_ingestion_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialized agent that connects to and retrieves data for analysis. It can read data from local files like CSVs and fetch data from external REST APIs. Use this agent for any task involving data acquisition.
instructions: >
    Your only purpose is to fetch data. When asked to read a file, use the read_csv_file tool. When asked to get data from an API, use the fetch_from_api tool. Do not analyze, modify, or report on the data. Simply return the raw data you retrieve.
tools:
  - read_csv_file
  - fetch_from_api
```

### 4.2. Data Validation Agent (`agents/data_validation_agent.yaml`)

**Role:** This is the core data quality engine. It's a collaborator agent that takes a dataset and applies validation logic using its specialized tools and knowledge base.
**Configuration:** Its `description` details its capabilities, such as checking for missing values and validating formats. Critically, it includes a `knowledge_base` section, linking it to `data_quality_kb`. This allows the agent's LLM to reason over the business rules document and use that context when executing its `verify_against_rules` tool.

```yaml
spec_version: v1
kind: native
name: data_validation_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An expert data validation agent. It applies data quality rules to datasets. Its capabilities include checking for missing values, validating formats for emails and phone numbers, and verifying data against business rules defined in its knowledge base.
instructions: >
    You are a data quality specialist. Use your tools to validate datasets provided to you. For simple checks like missing data, use the check_missing_values tool. For complex validations against corporate standards, you MUST consult your knowledge base to understand the required rules, then use the verify_against_rules tool to find records that violate them.
tools:
  - check_missing_values
  - validate_phone_number_format
  - verify_against_rules
knowledge_base:
  - data_quality_kb
```

### 4.3. Reporting Agent (`agents/reporting_agent.yaml`)

**Role:** This collaborator agent specializes in presenting information. Its sole purpose is to take structured data (like a list of errors) and format it for human consumption.
**Configuration:** The `description` is focused on its ability to create summaries and reports. It is equipped with only one tool, `generate_summary_report`, ensuring it performs its presentation role effectively and without distraction.

```yaml
spec_version: v1
kind: native
name: reporting_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialized agent for creating clear and concise summaries. It takes structured data, such as a list of data quality issues, and formats it into a human-readable report, typically a markdown table.
instructions: >
    Your only job is to present data clearly. When given a list of items and a title, you MUST use the generate_summary_report tool to create a markdown table. Do not perform any analysis yourself; only format the data you are given.
tools:
  - generate_summary_report
```

### 4.4. Data Steward Supervisor (`agents/data_steward_supervisor.yaml`)

**Role:** This is the master orchestrator and the primary user interface. It interprets the user's natural language request and delegates sub-tasks to the appropriate collaborator agents.
**Configuration:** This agent has no tools of its own. Its power lies in its `description` and `instructions`, which are carefully crafted to guide its LLM in routing tasks. The `collaborators` section lists all the specialized agents it can command. To enforce a strict separation of concerns, this supervisor does not have a direct link to the knowledge base; it relies on the `data_validation_agent` to handle all knowledge-based reasoning.

```yaml
spec_version: v1
kind: native
name: data_steward_supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An expert assistant for data quality. It understands requests to validate, clean, and report on datasets. It collaborates with other agents to connect to data, apply validation rules, and generate summaries.
instructions: >
    Your primary role is to orchestrate data quality tasks by delegating to your collaborators. You MUST follow this logic:
    - When a user asks to read, get, or fetch data, you MUST use the data_ingestion_agent.
    - When a user asks to check, validate, verify, or find errors in data, you MUST use the data_validation_agent.
    - When a user asks for a summary, list, or report of findings, you MUST use the reporting_agent.
    - You orchestrate the flow: first ingest, then validate, then report. Never perform these actions yourself.
collaborators:
  - data_ingestion_agent
  - data_validation_agent
  - reporting_agent
```

## Step 5: Deploy the Solution using the ADK CLI

With all configuration files and tools in place, you can now deploy the entire solution to your watsonx Orchestrate environment. The order of operations is important to ensure dependencies are met.

1.  **Navigate to the Project Directory**: Open your terminal and change into the `data_steward_demo` directory.
    ```bash
    cd path/to/data_steward_demo
    ```

2.  **Import All Tools**: Import the Python tools first, as the agents depend on them.
    ```bash
    orchestrate tools import -f tools/ingestion_tools.py
    orchestrate tools import -f tools/validation_tools.py
    orchestrate tools import -f tools/reporting_tools.py
    ```

3.  **Import the Knowledge Base**: Deploy the knowledge base so it can begin ingesting the document.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/data_quality_kb.yaml
    ```
    You can check its status with `orchestrate knowledge-bases status --name data_quality_kb`. Wait for it to be `Ready`.

4.  **Import the Collaborator Agents**: Import the specialized agents.
    ```bash
    orchestrate agents import -f agents/data_ingestion_agent.yaml
    orchestrate agents import -f agents/data_validation_agent.yaml
    orchestrate agents import -f agents/reporting_agent.yaml
    ```

5.  **Import the Supervisor Agent**: Finally, import the supervisor agent, which depends on all other components.
    ```bash
    orchestrate agents import -f agents/data_steward_supervisor.yaml
    ```

## Step 6: Verification and Demo Scenarios

After successful deployment, you can interact with your multi-agent system.

### 6.1. Start the Chat

Launch the interactive chat interface, specifying the `data_steward_supervisor` as the entry point.

```bash
orchestrate chat start --agent data_steward_supervisor
```

### 6.2. Execute Demo Scenarios

Engage with the agent in the chat window using the following prompts to demonstrate the solution's capabilities.

**Scenario 1: Simple Validation**
This scenario demonstrates the basic orchestration of ingestion, validation, and reporting.

*   **User Prompt:** `In mock_data/customer_records_q3.csv, find all customers with missing email addresses and generate a list.`
*   **Expected Agent Flow:**
    1.  The **Supervisor** receives the request. It understands "In...csv" means data ingestion, "find...missing" means validation, and "generate a list" means reporting.
    2.  It delegates to the **Data Ingestion Agent**, which uses the `read_csv_file` tool.
    3.  The data is passed back to the **Supervisor**, who then delegates to the **Data Validation Agent**.
    4.  The **Validation Agent** uses the `check_missing_values` tool on the "Email" column.
    5.  The list of records with missing emails is returned to the **Supervisor**, who delegates to the **Reporting Agent**.
    6.  The **Reporting Agent** uses `generate_summary_report` to format the results into a markdown table, which is presented to the user.

**Scenario 2: Knowledge-Based Validation**
This scenario showcases the agent's ability to use the knowledge base for dynamic rule application.

*   **User Prompt:** `Validate the entire mock_data/customer_records_q3.csv file against our official data quality rules for phone numbers.`
*   **Expected Agent Flow:**
    1.  The **Supervisor** understands the request requires ingestion and complex validation against "official rules."
    2.  It first calls the **Data Ingestion Agent** to read the CSV file.
    3.  The data is returned, and the **Supervisor** then tasks the **Data Validation Agent** with the validation job.
    4.  The **Validation Agent's** LLM consults its **Knowledge Base (`data_quality_kb`)** to understand the "official rule for phone numbers" is "(XXX) XXX-XXXX".
    5.  The **Validation Agent** then uses its `verify_against_rules` tool with the rule description "phone number format", which identifies all records not matching the pattern.
    6.  The results are passed to the **Reporting Agent** to be formatted and displayed.

**Scenario 3: Interactive Cleansing & Reporting**
This scenario demonstrates advanced reasoning and the full orchestration pipeline.

*   **User Prompt:** (After Scenario 2) `For the invalid phone numbers, suggest the correct format and create a summary report of all data quality issues.`
*   **Expected Agent Flow:**
    1.  The **Supervisor** understands the context from the previous turn.
    2.  It passes the list of invalid records to the **Data Validation Agent**. The agent's underlying LLM uses its reasoning capabilities to suggest corrections (e.g., transforming `555-1234` into `(XXX) 555-1234`). This does not require a tool but uses the model's generative power.
    3.  The **Supervisor** then instructs the **Reporting Agent** to use the `generate_summary_report` tool to create a clean summary of the identified issues.
    4.  The final response presented to the user includes both the suggested corrections and the summary report.

## Step 7: Troubleshooting

*   **Tool Import Fails**:
    *   **Symptom**: `orchestrate tools import` command returns an error.
    *   **Solution**: Ensure all packages in `requirements.txt` are installed. Check for Python syntax errors in the tool file. Verify that every function intended as a tool has the `@tool` decorator.
*   **Agent Fails to Route to Collaborator**:
    *   **Symptom**: The supervisor agent tries to perform a task itself or says it cannot perform the task.
    *   **Solution**: The descriptions and instructions for the supervisor and collaborator agents are critical. Make them more explicit. For example, in the supervisor's instructions, use strong language like "You MUST use the data_ingestion_agent for fetching data."
*   **Knowledge Base Not Used**:
    *   **Symptom**: Agent says it doesn't know the official rules.
    *   **Solution**: Run `orchestrate knowledge-bases status --name data_quality_kb` to confirm the status is `Ready`. Ensure the `knowledge_base` section is correctly configured in the `data_validation_agent.yaml` file.
*   **Incorrect Data from Tools**:
    *   **Symptom**: The agent shows malformed or unexpected data.
    *   **Solution**: Verify that all tools return simple, JSON-serializable data types (e.g., list, dict, string, boolean). Avoid returning complex objects like pandas DataFrames directly. Add `print()` statements inside your tool's Python code to debug the data being processed and returned.

## Step 8: Best Practices

*   **Descriptive Agents and Tools**: The LLM relies heavily on the `description` fields of agents and the docstrings of tools to make decisions. Be clear, specific, and comprehensive. A good docstring for a tool should explain what it does, its arguments (`Args:`), and what it returns (`Returns:`).
*   **Modular and Single-Purpose Design**: Follow the principle of separation of concerns. Agents and tools should have a single, well-defined responsibility. This makes the system more robust, easier to debug, and allows for the reuse of components in other solutions.
*   **Supervisor-Collaborator Pattern**: For complex workflows, always use a supervisor agent to orchestrate tasks. This centralizes the decision-making logic and keeps the collaborator agents simple and focused.
*   **Stateless Tools**: Design tools to be stateless whenever possible. They should receive all the data they need through their arguments and not rely on previous states. This makes their behavior predictable and easier to test.
*   **Iterative Development**: Start with a simple version of your agents and tools. Test them, then gradually add more complexity. For example, start with one collaborator and one tool, ensure it works, then add the next.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
