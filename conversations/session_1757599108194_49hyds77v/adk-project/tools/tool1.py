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