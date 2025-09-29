#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python**: Python version 3.9 or higher is required.
*   **Environment Initialization**: Your ADK must be configured to point to your watsonx Orchestrate environment. If you haven't done so, run the `orchestrate env init` command and follow the prompts.
*   **Project Directory**: Create a dedicated directory structure to organize your files. This promotes maintainability and clarity.
    ```bash
    mkdir finsecure_demo
    cd finsecure_demo
    mkdir agents
    mkdir tools
    ```

## 3. Step-by-Step Instructions

### Step 1: Create Python Tools

The foundation of our agent capabilities lies in a set of well-defined Python tools. Each tool performs a discrete task, such as fetching data or executing a business rule. We will create four separate Python files, one for each functional area, and place them in the `tools/` directory.

---

#### 3.1. Data Harvester Tools (`data_harvester_tools.py`)

**Business Value**: These tools automate the critical first step of any compliance check: data aggregation. By automatically fetching real-time market data, client portfolio specifics, and instrument details, the `DataHarvesterAgent` eliminates the manual, error-prone process of analysts gathering information from disparate systems. This ensures the compliance check is always based on accurate, up-to-the-minute information, improving decision quality and speed.

**Technical Implementation**: The tools simulate API calls to various financial data systems. They generate realistic, synthetic data structures representing market prices, portfolio holdings, and security details. Each function is decorated with `@tool` and includes a detailed docstring that watsonx Orchestrate uses to understand its purpose, arguments, and return values.

Create the file `tools/data_harvester_tools.py`:

