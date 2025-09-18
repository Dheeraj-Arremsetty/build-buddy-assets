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