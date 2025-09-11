# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-11 14:07:50
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Partner Operations Assistant

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **AI-Powered Partner Operations Assistant** for the client. This solution directly addresses the client's primary business challenge: reducing the administrative burden on store managers to free up their time for high-value activities like partner coaching and customer engagement. By implementing a multi-agent system using the IBM watsonx Orchestrate Agent Development Kit (ADK), we will create a single, conversational interface for managers to access real-time operational data, retrieve partner information, and get instant answers to HR policy questions.

The architecture leverages a powerful **supervisor-collaborator pattern**. A primary `Partner_Ops_Assistant_Agent` will act as an intelligent router, understanding the manager's intent and delegating tasks to two specialized collaborator agents: the `Store_Data_Agent` for inventory and sales queries, and the `Partner_Support_Agent` for schedule lookups and policy questions via a knowledge base. This showcases Orchestrate's ability to create sophisticated, scalable AI solutions that streamline complex workflows and provide immediate, demonstrable business value. This plan is a complete, end-to-end implementation of the client's specified demo concept.

## Prerequisites

Before beginning, ensure your development environment is correctly configured to meet IBM's requirements.

1.  **Python Environment**: A working Python 3.9+ installation is required. This ensures compatibility with the ADK and its dependencies.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. This is the core library for building and deploying agents. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized and selected. This connects your local ADK to your Orchestrate instance. If not yet configured, run:
    ```bash
    # Log in to your IBM account
    orchestrate login
    
    # Select the environment where you will deploy the assets
    orchestrate env select
    ```
4.  **Required Python Libraries**: The tools we will build depend on the `pandas` library for data manipulation. We will create a `requirements.txt` file and install it to manage dependencies effectively.

## Step 1: Project Setup and Mock Data Creation

First, we will establish a clean project structure and create the synthetic data files that our tools will use to simulate real-world systems. This approach allows for a robust and realistic demonstration without needing direct integration with the client's backend systems, a key aspect of a successful Proof of Concept.

**1. Create the Directory Structure:**

Open your terminal and create the following directories. This organization separates our agents, tools, knowledge base definitions, and mock data for clarity, maintainability, and adherence to best practices.

```bash
mkdir -p orchestrate_demo/{agents,tools,kbs,mock_data,mock_docs}
cd orchestrate_demo
```

**2. Create Mock Data Files:**

These files contain realistic, synthetic data that mirrors the information a store manager would need. The data is structured to be easily parsed by our Python tools.

*   **`mock_data/inventory.csv`**: Contains current stock levels for various store items.
    ```csv
    item_sku,item_name,quantity_on_hand,reorder_level
    SKU-HC-GR-01,Grande Hot Cups,85,100
    SKU-CC-VN-01,Venti Cold Cups,120,150
    SKU-BN-ES-01,Espresso Beans,15,20
    SKU-MK-OT-01,Oat Milk,25,30
    SKU-SY-VN-01,Vanilla Syrup,18,24
    SKU-LD-GR-01,Grande Lids,75,100
    ```

*   **`mock_data/sales_report.json`**: A daily sales summary in a structured JSON format.
    ```json
    {
      "report_date": "2024-09-21",
      "total_sales": 4250.75,
      "transaction_count": 315,
      "average_ticket_value": 13.50,
      "peak_hours": "8:00 AM - 10:00 AM"
    }
    ```

*   **`mock_data/schedule.csv`**: The partner (employee) work schedule for the current week.
    ```csv
    partner_id,partner_name,shift_date,shift_start_time,shift_end_time
    EMP101,Alice Johnson,2024-09-21,06:00,14:00
    EMP102,Bob Williams,2024-09-21,08:00,16:00
    EMP103,Charlie Brown,2024-09-21,14:00,22:00
    EMP104,Diana Miller,2024-09-21,16:00,22:30
    EMP105,Eve Davis,2024-09-22,06:00,14:00
    ```

**3. Create Mock Policy Documents:**

These PDF files will be ingested into our knowledge base. For this demo, you can create simple text files, paste the content below, and use a "Print to PDF" or "Save as PDF" function from any text editor.

*   **`mock_docs/Partner_Handbook.pdf`**: Create a PDF containing the following text:
    > **Partner Handbook: Section 5 - Dress Code**
    > All partners are expected to maintain a professional appearance.
    >
    > **Footwear Policy:**
    > Approved footwear includes closed-toe, non-slip shoes in black, brown, or gray. Shoes must be clean and in good repair. Canvas shoes, sandals, and high heels are not permitted for safety reasons.
    >
    > **Sick Leave Policy:**
    > If you are unable to work your scheduled shift due to illness, please notify the store manager at least two hours before your shift begins.

*   **`mock_docs/Store_Ops_Manual.pdf`**: Create a PDF containing the following text:
    > **Store Operations Manual: Section 2 - Opening Procedures**
    > 1.  Deactivate alarm system.
    > 2.  Perform cash count in the safe.
    > 3.  Calibrate espresso machines.
    > 4.  Check milk and dairy temperatures.

**4. Create `requirements.txt`:**

This file lists the Python dependencies for our tools. This is a critical best practice for ensuring a reproducible environment.

*   **`requirements.txt`**:
    ```text
    pandas
    ```

## Step 2: Create Python Tools

Now, we will implement the Python functions that our collaborator agents will use. These tools encapsulate the logic for accessing our mock data sources, following the exact `@tool` decorator pattern from the IBM documentation. Each tool includes a detailed docstring, which is crucial for the agent's ability to understand its function, arguments, and return values.

### Tool Set 1: Store Data Agent Tools

These tools provide access to operational data like sales and inventory. Create the following file:

*   **`tools/store_data_tools.py`**

    This file contains tools for querying inventory and sales data. The `get_inventory_level` tool allows for precise stock checks, preventing stockouts, while `get_daily_sales_report` provides a quick snapshot of business performance, enabling managers to make informed decisions on staffing and promotions. These tools are designed to be stateless and return simple, JSON-serializable dictionaries, ensuring compatibility and reliability.

    ```python
    import json
    import pandas as pd
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="get_inventory_level")
    def get_inventory_level(item_name: str) -> dict:
        """
        Retrieves the current on-hand quantity for a specific inventory item from the store's inventory system.

        Args:
            item_name (str): The name of the inventory item to look up (e.g., "Oat Milk", "Grande Hot Cups").

        Returns:
            dict: A dictionary containing the item name and its quantity on hand, or an error if the item is not found.
        """
        try:
            inventory_df = pd.read_csv('./mock_data/inventory.csv')
            # Case-insensitive search to make the tool more robust to user input variations
            item = inventory_df[inventory_df['item_name'].str.contains(item_name, case=False, na=False)]
            if not item.empty:
                result = item.iloc[0]
                return {"item_name": result['item_name'], "quantity_on_hand": int(result['quantity_on_hand'])}
            else:
                return {"error": f"Item '{item_name}' not found in inventory."}
        except FileNotFoundError:
            return {"error": "Inventory data file not found. Please ensure it is in the 'mock_data' directory."}
        except Exception as e:
            return {"error": f"An unexpected error occurred while reading inventory: {str(e)}"}

    @tool(name="get_daily_sales_report")
    def get_daily_sales_report() -> dict:
        """
        Fetches the most recent daily sales report, including total sales, transaction count, and peak hours.

        Returns:
            dict: A dictionary containing the key metrics from the latest sales report, or an error if the report is unavailable.
        """
        try:
            with open('./mock_data/sales_report.json', 'r') as f:
                sales_data = json.load(f)
            return sales_data
        except FileNotFoundError:
            return {"error": "Sales report file not found. Please ensure it is in the 'mock_data' directory."}
        except json.JSONDecodeError:
            return {"error": "Error decoding sales report JSON. The file may be corrupted."}
        except Exception as e:
            return {"error": f"An unexpected error occurred while reading sales report: {str(e)}"}
    ```

### Tool Set 2: Partner Support Agent Tools

This tool helps managers with staffing and scheduling queries. Create the following file:

*   **`tools/partner_support_tools.py`**

    The `lookup_partner_schedule` tool is essential for agile workforce management. When a partner calls in sick or a shift becomes unexpectedly busy, the manager can instantly find out who is scheduled to work, enabling them to quickly arrange for cover or reassign tasks without having to log into a separate HR system. The tool's logic correctly handles time-based queries to find any overlapping shifts, providing a realistic and useful function.

    ```python
    import pandas as pd
    from datetime import datetime
    from typing import List
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="lookup_partner_schedule")
    def lookup_partner_schedule(shift_start_time: str, shift_end_time: str) -> List[dict]:
        """
        Looks up partners scheduled to work within a specific time window on the current day.

        Args:
            shift_start_time (str): The start of the time window to check, in HH:MM 24-hour format (e.g., "16:00").
            shift_end_time (str): The end of the time window to check, in HH:MM 24-hour format (e.g., "22:00").

        Returns:
            list[dict]: A list of partners scheduled during that time, including their name and shift details. Returns an empty list if no one is scheduled or an error dictionary on failure.
        """
        try:
            schedule_df = pd.read_csv('./mock_data/schedule.csv')
            # Use today's date for the query, matching the demo scenario
            today_str = '2024-09-21'
            
            # Filter for today's schedule
            today_schedule = schedule_df[schedule_df['shift_date'] == today_str].copy()
            if today_schedule.empty:
                return []

            # Convert times for comparison
            query_start = datetime.strptime(shift_start_time, '%H:%M').time()
            query_end = datetime.strptime(shift_end_time, '%H:%M').time()

            today_schedule['start'] = pd.to_datetime(today_schedule['shift_start_time'], format='%H:%M').dt.time
            today_schedule['end'] = pd.to_datetime(today_schedule['shift_end_time'], format='%H:%M').dt.time

            # Find overlapping shifts using the standard interval overlap formula: (StartA <= EndB) and (EndA >= StartB)
            result_df = today_schedule[
                (today_schedule['start'] < query_end) & (today_schedule['end'] > query_start)
            ]

            if result_df.empty:
                return []

            return result_df[['partner_name', 'shift_start_time', 'shift_end_time']].to_dict('records')

        except FileNotFoundError:
            return [{"error": "Schedule data file not found. Please ensure it is in the 'mock_data' directory."}]
        except Exception as e:
            return [{"error": f"An unexpected error occurred while looking up schedule: {str(e)}"}]
    ```

## Step 3: Create the Knowledge Base

The knowledge base allows the `Partner_Support_Agent` to answer unstructured questions by performing Retrieval-Augmented Generation (RAG) on the provided documents. This is the ideal pattern for HR and policy questions, ensuring managers provide consistent and accurate information directly from source-of-truth documents.

*   **`kbs/store_operations_kb.yaml`**

    This configuration file defines our knowledge base. It instructs Orchestrate to use its built-in Milvus vector database, ingest the two specified PDF documents, and use a default IBM embedding model (`ibm/slate-125m-english-rtrvr-v2`) to create vector representations for efficient semantic searching. The description is crucial, as it helps the agent understand what kind of information is contained within.

    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: Store_Operations_KB
    description: >
       Contains official documents for store operations, including the Partner Handbook for HR policies (like dress code and sick leave) and the Store Operations Manual for procedures (like opening and closing). Use this to answer any questions about company policy or standard operating procedures.
    documents:
       - "./mock_docs/Partner_Handbook.pdf"
       - "./mock_docs/Store_Ops_Manual.pdf"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 4: Create Agent Configurations (YAML)

With the tools and knowledge base defined, we now create the YAML configurations for our three agents, defining their roles, capabilities, and instructions according to the supervisor-collaborator pattern.

### Collaborator Agent 1: Store Data Agent

This agent is a specialist, focused exclusively on operational data. Its description is crafted to attract queries related to sales, inventory, and stock levels, making it the clear choice for the supervisor when such a request is made.

*   **`agents/store_data_agent.yaml`**

    ```yaml
    spec_version: v1
    kind: native
    name: Store_Data_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        An agent specializing in retrieving store operational data. Use this agent for any questions related to current inventory levels, stock quantities of items, and daily sales performance reports. It connects directly to the store's data systems.
    instructions: >
        You are an expert at querying store data systems. Your purpose is to provide precise, factual data.
        - Phase 1: Understand the user's data request. Identify if they are asking for inventory or sales data.
        - Phase 2: Use the 'get_inventory_level' tool when the user asks about the quantity of a specific item.
        - Phase 3: Use the 'get_daily_sales_report' tool when the user asks for sales figures or the day's performance summary.
        - Phase 4: Review the output from the tool for accuracy.
        - Phase 5: Present only the requested data to the user in a clear, concise format. Do not add any extra commentary unless an error occurred.
    collaborators: []
    tools:
      - get_inventory_level
      - get_daily_sales_report
    ```

### Collaborator Agent 2: Partner Support Agent

This RAG agent handles all partner-related tasks. Its description highlights its ability to look up schedules (a structured task using a tool) and answer policy questions (an unstructured task using the knowledge base), making it the designated expert for HR-related queries.

*   **`agents/partner_support_agent.yaml`**

    ```yaml
    spec_version: v1
    kind: native
    name: Partner_Support_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        An agent specializing in partner (employee) support tasks. Use this agent for questions about partner work schedules and for looking up official company policies in the Partner Handbook and operational manuals. It can answer questions about dress code, sick leave, and other HR topics.
    instructions: >
        You are an assistant for supporting store partners with scheduling and policy questions.
        - For questions about who is working at specific times, you MUST use the 'lookup_partner_schedule' tool.
        - For all questions about policies, procedures, dress code, benefits, or operational standards, you MUST search the 'Store_Operations_KB' knowledge base to find the official answer.
        - Always provide accurate information based on your tools and knowledge base. Cite the source document when answering policy questions if possible.
    collaborators: []
    tools:
      - lookup_partner_schedule
    knowledge_base:
      - Store_Operations_KB
    ```

### Supervisor Agent: Partner Ops Assistant

This is the main agent the manager interacts with. It has no tools or knowledge base of its own. Its sole purpose is to understand the user's request and delegate it to the correct collaborator based on their descriptions and its own explicit instructions. This demonstrates the core orchestration capability of the platform.

*   **`agents/partner_ops_assistant_agent.yaml`**

    ```yaml
    spec_version: v1
    kind: native
    name: Partner_Ops_Assistant_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        A digital assistant for store managers. It can answer questions about daily sales, inventory, and partner schedules. It can also look up company policies from the Partner Handbook and operational manuals. It orchestrates tasks by delegating to specialized agents.
    instructions: >
        You are the Partner Operations Assistant, a digital assistant for store managers. Your primary role is to understand the user's request and route it to the correct specialist agent to get the answer. You must follow these rules:
        - For any questions about sales figures, business performance, inventory levels, or stock quantities, you MUST use the 'Store_Data_Agent'.
        - For any questions about partner schedules, who is working, or official HR policies like dress code or sick leave, you MUST use the 'Partner_Support_Agent'.
        - If a user asks a complex question that involves multiple areas (e.g., "What were our sales and how many grande cups do we have?"), you must use the appropriate agents sequentially to gather all the information and then synthesize a single, comprehensive answer for the user. Do not respond until you have all the pieces of information.
    collaborators:
      - Store_Data_Agent
      - Partner_Support_Agent
    ```

## Step 5: Build and Deploy the Solution

Now we will use the ADK's command-line interface to install dependencies and import all our assets into watsonx Orchestrate in the correct, logical order: dependencies, then tools, then knowledge bases, then collaborator agents, and finally the supervisor agent.

Execute these commands from the `orchestrate_demo` root directory.

```bash
# 1. Install Python dependencies from the requirements file
pip install -r requirements.txt

# 2. Import all tools for the collaborator agents. The ADK will register these tools
# and make them available for agents to use.
echo "Importing tools..."
orchestrate tools import -f ./tools/store_data_tools.py
orchestrate tools import -f ./tools/partner_support_tools.py

# 3. Import the knowledge base. This command uploads the documents and starts the
# ingestion process in the background.
echo "Importing knowledge base... this may take a few minutes for ingestion."
orchestrate knowledge-bases import -f ./kbs/store_operations_kb.yaml

# 4. Check the knowledge base status to ensure it's ready. Ingestion can take
# a few minutes. You may need to run this command a few times until the status is "Ready: True".
echo "Checking knowledge base status..."
orchestrate knowledge-bases status --name Store_Operations_KB

# 5. Import the collaborator agents. These must be imported before the supervisor
# so that the supervisor can find them when it is imported.
echo "Importing collaborator agents..."
orchestrate agents import -f ./agents/store_data_agent.yaml
orchestrate agents import -f ./agents/partner_support_agent.yaml

# 6. Import the main supervisor agent. This agent links to the collaborators.
echo "Importing supervisor agent..."
orchestrate agents import -f ./agents/partner_ops_assistant_agent.yaml

echo "Deployment complete! All agents, tools, and knowledge bases are now available."
```

## Step 6: Verification and Demo Execution

With the solution deployed, you can now interact with the assistant and test the defined demo scenarios, showcasing the full capabilities of the solution.

**1. Start the Chat Interface:**

Run the following command to launch the Orchestrate chat client. A browser window will open where you can interact with your agents.

```bash
orchestrate chat start
```

**2. Select the Supervisor Agent:**

In the chat UI's agent selection dropdown, ensure you select the `Partner_Ops_Assistant_Agent` to begin the conversation.

**3. Run Demo Scenarios:**

*   **Scenario 1: Morning Operations Check (Synthesizing from multiple tools)**
    *   **User Prompt:** `What were yesterday's total sales and how many grande hot cups do we have in stock?`
    *   **Expected Behavior:** The `Partner_Ops_Assistant_Agent` will receive this prompt. Its instructions will guide it to delegate the "total sales" part to the `Store_Data_Agent` (which uses `get_daily_sales_report`) and the "grande hot cups" part to the same agent (which uses `get_inventory_level`). It will then receive both pieces of information and combine them into a single, cohesive answer.
    *   **Expected Output:** "Yesterday's total sales were $4250.75. We currently have 85 Grande Hot Cups in stock."

*   **Scenario 2: Mid-Shift Staffing Query (Tool Use)**
    *   **User Prompt:** `Who is scheduled to work from 4 PM to close today?`
    *   **Expected Behavior:** The supervisor will identify the keywords "scheduled" and "work," routing the query to the `Partner_Support_Agent`. This agent will then execute its `lookup_partner_schedule` tool with the parameters `16:00` and `22:00`, querying the `schedule.csv` file.
    *   **Expected Output:** "The partners scheduled from 4 PM to close are: Charlie Brown (14:00 - 22:00) and Diana Miller (16:00 - 22:30)."

*   **Scenario 3: Real-Time Policy Guidance (RAG with Knowledge Base)**
    *   **User Prompt:** `What is the policy on approved footwear for partners?`
    *   **Expected Behavior:** The supervisor will recognize this as a policy question and route it to the `Partner_Support_Agent`. This agent will not use a tool but will instead query its `Store_Operations_KB`. It will find the relevant section in the `Partner_Handbook.pdf` and generate a natural language answer based on that content.
    *   **Expected Output:** "According to the Partner Handbook, the policy on approved footwear is: Approved footwear includes closed-toe, non-slip shoes in black, brown, or gray. Shoes must be clean and in good repair. Canvas shoes, sandals, and high heels are not permitted for safety reasons."

## Troubleshooting

*   **Issue: Supervisor agent fails to route the request correctly or says it cannot help.**
    *   **Solution:** This is almost always due to ambiguous agent `description` or supervisor `instructions`. Review the YAML files. Ensure the collaborator descriptions are distinct and clearly state their capabilities. Make the supervisor's `instructions` more explicit, using strong language like "For any task involving inventory, you MUST use the 'Store_Data_Agent'". Re-import the modified agent YAML to apply changes.
*   **Issue: A tool returns a "File not found" error.**
    *   **Solution:** The ADK executes tools from the directory where you run the `orchestrate chat start` command. Ensure you are in the `orchestrate_demo` root directory when starting the chat. Verify that the file paths in the Python tool code (e.g., `./mock_data/inventory.csv`) are correct relative to this root directory.
*   **Issue: The knowledge base isn't providing answers or says it can't find information.**
    *   **Solution:** The knowledge base ingestion process can take a few minutes. Run `orchestrate knowledge-bases status --name Store_Operations_KB` to confirm the `Ready` status is `True`. Also, ensure the PDF documents are not image-based and contain searchable text. If the problem persists, check the `description` of the knowledge base to ensure it accurately reflects the content.

## Best Practices

*   **Descriptive and Distinct Agent Descriptions**: The success of the supervisor-collaborator pattern hinges on the supervisor's ability to distinguish between its collaborators. Write clear, detailed descriptions for each collaborator agent that highlight their unique skills and the types of tasks they are responsible for.
*   **Explicit Supervisor Instructions**: Don't leave routing to chance. In the supervisor's `instructions`, be directive. Use strong language like "For any task involving X, you MUST use Agent Y" to guide the LLM's reasoning process and ensure reliable delegation.
*   **Modular and Specialized Agents**: Keep collaborator agents focused on a specific domain (e.g., data, HR). This makes the system easier to maintain, test, and scale. If you need to add a new capability, you can add a new specialized agent without modifying existing ones.
*   **Stateless and Robust Tools**: Design your Python tools to be stateless and include comprehensive error handling. They should take inputs, perform an action, and return a structured output (or error) without relying on memory from previous calls. This makes them more reliable and predictable.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
