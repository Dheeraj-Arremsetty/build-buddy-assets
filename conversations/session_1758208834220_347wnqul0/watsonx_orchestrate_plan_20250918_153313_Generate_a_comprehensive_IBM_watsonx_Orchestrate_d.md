# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 15:33:13
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Data Validation Co-Pilot for S&P Global

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Data Validation Co-Pilot" for S&P Global using IBM watsonx Orchestrate. The solution is designed to directly address S&P Global's critical need for high-integrity financial data and improved operational efficiency. By leveraging a sophisticated supervisor-collaborator agent architecture, this Co-Pilot will empower S&P Global analysts to perform complex data quality checks, locate datasets, and query validation rules using simple natural language.

The plan meticulously follows the proposed demo concept, creating a multi-agent system where a `ValidationSupervisorAgent` intelligently orchestrates tasks between two specialist agents: `DatasetLocatorAgent` for finding data and `DataValidatorAgent` for executing quality checks. This modular design not only demonstrates the power of watsonx Orchestrate but also provides a scalable framework for future expansion. The plan includes the creation of all required assets, from mock data and Python-based tools to the agent YAML configurations and a document-based knowledge base, culminating in a fully deployable and testable solution.

## 2. Prerequisites

Before beginning, ensure your development environment is correctly configured.

*   **Python:** Python version 3.10 or higher installed.
*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed. If not, install it using pip:
    ```bash
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

```
spg-demo/
├── agents/
│   ├── ValidationSupervisorAgent.yaml
│   ├── DatasetLocatorAgent.yaml
│   └── DataValidatorAgent.yaml
├── tools/
│   ├── dataset_locator_tools.py
│   └── data_validator_tools.py
├── data/
│   ├── q4_institutional_holdings.csv
│   └── data_catalog.json
├── knowledge_base/
│   ├── ValidationRulesKB.yaml
│   └── docs/
│       └── validation_rules.md
└── requirements.txt
```

## 4. Step-by-Step Instructions

This section details the creation of all necessary components, from the underlying data and tools to the final agent configurations.

### Step 4.1: Create Mock Data and Knowledge Base Content

First, we will create the synthetic data and documentation that will power the demo.

1.  **Create the Data Catalog (`data/data_catalog.json`):**
    This file maps user-friendly dataset names to their physical file paths. The `DatasetLocatorAgent` will use this as its source of truth.

    ```json
    {
      "q4_institutional_holdings": "./data/q4_institutional_holdings.csv",
      "q4_corporate_bonds": "./data/q4_corporate_bonds.csv",
      "annual_earnings_report_2023": "./data/annual_earnings_report_2023.csv"
    }
    ```

2.  **Generate the Synthetic Dataset (`data/q4_institutional_holdings.csv`):**
    This CSV file represents a typical S&P dataset and includes intentionally seeded errors (missing values and outliers) for the `DataValidatorAgent` to detect.

    ```csv
    CIK,company_name,shares_held,market_value,report_date
    1018724,AMAZON COM INC,500000,150000000.00,2023-12-31
    1318605,TESLA INC,750000,187500000.00,2023-12-31
    1652044,UBER TECHNOLOGIES INC,300000,,2023-12-31
    1045810,NVIDIA CORP,400000,196000000.00,2023-12-31
    1326801,META PLATFORMS INC,250000,87500000.00,2023-12-31
    320193,APPLE INC,9000000000,270000000000.00,2023-12-31
    789019,MICROSOFT CORP,600000,222000000.00,2023-12-31
    1067983,ALPHABET INC,350000,49000000.00,2023-12-31
    1748790,SNOWFLAKE INC,150000,,2023-12-31
    1108524,SALESFORCE INC,200000,52000000.00,2023-12-31
    ```

3.  **Create the Knowledge Base Document (`knowledge_base/docs/validation_rules.md`):**
    This Markdown file contains the business rules for data validation. The `ValidationSupervisorAgent` will query this document to answer analyst questions.

    ```markdown
    # S&P Global Data Validation Standards

    ## Rule 1: Market Value Integrity
    The `market_value` column is critical for financial reporting and cannot be null or empty. It must be a positive numerical value representing the total market value of the shares held.

    ## Rule 2: Share Holdings Constraints
    The `shares_held` column must be a positive integer. Any records with zero or negative shares are considered invalid. Outlier detection should be performed to flag unusually large holdings that may indicate data entry errors.

    ## Rule 3: Reporting Date Format
    The `report_date` must strictly adhere to the YYYY-MM-DD format to ensure consistency across all datasets.
    ```

### Step 4.2: Develop Custom Python Tools

Next, create the Python tools that provide the core functionality for the agents.

1.  **Create the `requirements.txt` file:**
    This file lists the necessary Python packages for the tools.

    ```text
    pandas
    ```

2.  **Create the Dataset Locator Tool (`tools/dataset_locator_tools.py`):**
    This tool is responsible for finding the file path of a dataset based on its common name. It provides a crucial link between the user's request and the physical data. Its business value lies in abstracting away the complexity of file systems or databases, allowing analysts to request data naturally without needing to know technical details.

    ```python
    import json
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="find_dataset_path", permission=ToolPermission.ADMIN)
    def find_dataset_path(dataset_name: str) -> str:
        """
        Finds the file path for a given financial dataset name.

        Args:
            dataset_name (str): The common name of the dataset, e.g., 'q4 institutional holdings'.

        Returns:
            str: The file path of the dataset or an error message if not found.
        """
        catalog_path = './data/data_catalog.json'
        try:
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
            
            # Normalize the key for matching
            normalized_name = dataset_name.lower().replace(" ", "_")
            
            if normalized_name in catalog:
                return f"Dataset found. Path: {catalog[normalized_name]}"
            else:
                available_datasets = ", ".join(catalog.keys())
                return f"Error: Dataset '{dataset_name}' not found. Available datasets are: {available_datasets}."
        except FileNotFoundError:
            return f"Error: The data catalog file was not found at {catalog_path}."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    ```

3.  **Create the Data Validator Tool (`tools/data_validator_tools.py`):**
    This is the workhorse tool that performs the actual data quality checks using the pandas library. It ingests a dataset path, runs a series of pre-defined validation rules (checking for nulls, identifying outliers), and generates a concise summary. This tool delivers immense business value by automating a tedious and error-prone manual process, ensuring data consistency and freeing up analysts to focus on higher-value analysis.

    ```python
    import pandas as pd
    import json
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="run_quality_checks", permission=ToolPermission.ADMIN)
    def run_quality_checks(file_path: str) -> str:
        """
        Runs a series of data quality checks on a given CSV dataset. It checks for null values, identifies potential outliers, and provides summary statistics.

        Args:
            file_path (str): The full path to the CSV file to be validated.

        Returns:
            str: A JSON formatted string summarizing the data quality findings.
        """
        try:
            df = pd.read_csv(file_path)
            
            # 1. Null Value Check
            null_summary = df.isnull().sum()
            null_findings = {col: int(count) for col, count in null_summary.items() if count > 0}
            
            # 2. Outlier Detection (using IQR method on numeric columns)
            outlier_findings = {}
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                if not outliers.empty:
                    outlier_findings[col] = len(outliers)
            
            # 3. Summary Statistics
            total_records = len(df)
            
            # 4. Construct the report
            report = {
                "validation_status": "Completed",
                "total_records_analyzed": total_records,
                "findings": {
                    "null_values": null_findings or "No null values found.",
                    "potential_outliers": outlier_findings or "No potential outliers detected."
                }
            }
            
            return json.dumps(report, indent=2)

        except FileNotFoundError:
            return json.dumps({"validation_status": "Error", "message": f"File not found at path: {file_path}"})
        except Exception as e:
            return json.dumps({"validation_status": "Error", "message": f"An error occurred during validation: {str(e)}"})
    ```

### Step 4.3: Define the Knowledge Base

Create the YAML configuration for the knowledge base, which will ingest the validation rules document.

*   **Create `knowledge_base/ValidationRulesKB.yaml`:**

    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: ValidationRulesKB
    description: >
       Contains the official business rules and standards for validating S&P Global financial datasets, including rules for market value, shares held, and date formats.
    documents:
       - "./knowledge_base/docs/validation_rules.md"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 4.4: Define the Agent Architecture

Now, define the three agents using YAML configuration files. The descriptions are critical as they enable the supervisor agent to route tasks correctly.

1.  **Create `agents/DatasetLocatorAgent.yaml`:**
    A specialist agent with a single purpose: to locate datasets. Its description clearly states this capability.

    ```yaml
    spec_version: v1
    kind: native
    name: DatasetLocatorAgent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
      A specialist agent that locates and returns the file path to financial datasets based on their common name and reporting period. It uses the find_dataset_path tool to query an internal data catalog.
    instructions: >
      Your only job is to find the path of a dataset when asked. Use the find_dataset_path tool. If the dataset is not found, clearly state that and list the available options provided by the tool.
    tools:
      - find_dataset_path
    ```

2.  **Create `agents/DataValidatorAgent.yaml`:**
    The core workhorse agent that performs the validation. Its description highlights its ability to run quality checks.

    ```yaml
    spec_version: v1
    kind: native
    name: DataValidatorAgent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
      A specialist agent that performs data quality checks on financial datasets. It can identify null values, detect outliers, and provide a summary report. It uses the run_quality_checks tool.
    instructions: >
      Your purpose is to validate datasets using the run_quality_checks tool. When you receive a file path, execute the tool and present the JSON results to the user in a clear, readable format. Do not interpret the results, just report them accurately.
    tools:
      - run_quality_checks
    ```

3.  **Create `agents/ValidationSupervisorAgent.yaml`:**
    The user-facing supervisor agent. Its instructions detail the logic for delegating tasks to its collaborators and for using its knowledge base.

    ```yaml
    spec_version: v1
    kind: native
    name: ValidationSupervisorAgent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
        An AI Co-Pilot for S&P Global analysts that validates financial datasets. It orchestrates the entire validation workflow by locating datasets, running quality checks, and answering questions about the validation process. It uses the DatasetLocatorAgent to find data and the DataValidatorAgent to perform checks.
    instructions: >
        You are an AI Co-Pilot for S&P Global data analysts. Your primary role is to help them validate financial datasets efficiently.

        Reasoning Workflow:
        1.  When an analyst asks to validate a dataset (e.g., "validate the Q4 holdings data"), your first step is ALWAYS to use the `DatasetLocatorAgent` to find the file path.
        2.  Once you have the file path from the `DatasetLocatorAgent`, immediately pass that path to the `DataValidatorAgent` to execute the quality checks.
        3.  After the `DataValidatorAgent` returns its findings, summarize the JSON report in a clear, concise, and business-friendly manner for the analyst. Highlight key numbers like total records, null counts, and outliers.
        4.  If an analyst asks a question about rules, standards, or processes (e.g., "what are the rules for market value?"), use your knowledge base to find the answer. Do not use other agents for this.
        5.  If the `DatasetLocatorAgent` reports an error that a dataset cannot be found, relay this information clearly to the analyst and provide the list of available datasets. Do not proceed to the validation step.
    collaborators:
      - DatasetLocatorAgent
      - DataValidatorAgent
    knowledge_base:
      - ValidationRulesKB
    ```

### Step 4.5: Deploy the Solution using the ADK CLI

With all assets created, deploy the solution to your watsonx Orchestrate environment using the following sequence of commands. The order is critical: tools must be imported first, followed by the knowledge base, then collaborator agents, and finally the supervisor.

Execute these commands from the root `spg-demo/` directory.

1.  **Import the Tools:**
    ```bash
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

```bash
orchestrate chat start --agent ValidationSupervisorAgent
```

Now, run through the three predefined scenarios to verify the complete workflow.

*   **Scenario 1: Successful Validation Workflow**
    *   **Analyst Input:** `Validate the Q4 institutional holdings dataset.`
    *   **Expected Orchestrate Flow:**
        1.  `ValidationSupervisorAgent` receives the request.
        2.  It calls `DatasetLocatorAgent` with "Q4 institutional holdings".
        3.  `DatasetLocatorAgent` finds and returns `./data/q4_institutional_holdings.csv`.
        4.  `ValidationSupervisorAgent` passes the path to `DataValidatorAgent`.
        5.  `DataValidatorAgent` runs `run_quality_checks` and returns a JSON report identifying 2 nulls in `market_value` and 1 outlier in `shares_held`.
    *   **Expected Output:** "I have validated the Q4 institutional holdings dataset. **Findings:** The analysis of 10 records is complete. 2 null values were found in the 'market_value' column and 1 potential outlier was detected in the 'shares_held' column. Would you like a more detailed report?"

*   **Scenario 2: Knowledge Base Inquiry**
    *   **Analyst Input:** `What are the validation rules for market value?`
    *   **Expected Orchestrate Flow:**
        1.  `ValidationSupervisorAgent` recognizes the query as a question.
        2.  It queries its `ValidationRulesKB` knowledge base.
        3.  It finds the relevant text from `validation_rules.md`.
    *   **Expected Output:** "Based on the S&P Global Data Validation Standards, the rule for market value is: 'The `market_value` column is critical for financial reporting and cannot be null or empty. It must be a positive numerical value representing the total market value of the shares held.'"

*   **Scenario 3: Failed Data Location**
    *   **Analyst Input:** `Can you check the Q3 M&A dataset?`
    *   **Expected Orchestrate Flow:**
        1.  `ValidationSupervisorAgent` receives the request.
        2.  It calls `DatasetLocatorAgent` with "Q3 M&A dataset".
        3.  `DatasetLocatorAgent` checks its catalog and does not find a match. It returns an error message with available datasets.
    *   **Expected Output:** "I'm sorry, I could not locate a dataset named 'Q3 M&A dataset'. Available datasets are: q4_institutional_holdings, q4_corporate_bonds, annual_earnings_report_2023."

## 6. Troubleshooting

*   **Tool Import Failure:**
    *   **Issue:** The `orchestrate tools import` command fails.
    *   **Solution:** Ensure `pandas` is installed (`pip install -r requirements.txt`). Check for syntax errors in the Python files. Verify that the `@tool` decorator is correctly applied.

*   **Agent Import Failure:**
    *   **Issue:** The `orchestrate agents import` command fails with an error like "collaborator not found" or "tool not found".
    *   **Solution:** This is almost always an import order issue. You **must** import tools and collaborator agents *before* importing the supervisor agent that depends on them. Rerun the import commands in the specified order. Also, check for YAML syntax errors.

*   **Incorrect Agent Routing:**
    *   **Issue:** The supervisor agent fails to call the correct collaborator or tries to use a tool directly.
    *   **Solution:** This is a prompt engineering issue. The quality of the `description` and `instructions` in the agent YAML files is paramount. Ensure the descriptions are specific and accurately reflect the agent's unique capabilities. The supervisor's instructions should be explicit about *which agent to use for which task*.

*   **Knowledge Base Not Returning Answers:**
    *   **Issue:** The agent responds with "I don't have that information" for questions that should be in the knowledge base.
    *   **Solution:** Verify the file path in `ValidationRulesKB.yaml` is correct relative to where you are running the command. Ensure the `orchestrate knowledge-bases import` command completed successfully. The content in the `.md` file might be too sparse; ensure it contains the keywords from the user's query.

## 7. Best Practices

*   **Descriptive Clarity:** The supervisor agent's ability to delegate tasks relies entirely on the quality of the collaborator agents' `description` fields. Make them unique, specific, and action-oriented.
*   **Structured Tool Outputs:** The `run_quality_checks` tool returns a JSON string. This is a best practice as it provides a structured, predictable output that the LLM can easily parse, summarize, and present to the user, reducing hallucinations.
*   **Error Handling in Tools:** Both tools include `try...except` blocks. This makes the tools robust and allows them to return user-friendly error messages to the agent, which can then be relayed to the user, rather than causing the entire sequence to fail silently.
*   **Idempotent Design:** The tools are designed to be idempotent; running them multiple times with the same input will produce the same output without causing unintended side effects. This is crucial for reliable automation.
*   **Version Control:** Store all project files (YAML, Python, data, docs) in a Git repository. This allows for tracking changes, collaboration, and easy rollback if an update causes issues.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
