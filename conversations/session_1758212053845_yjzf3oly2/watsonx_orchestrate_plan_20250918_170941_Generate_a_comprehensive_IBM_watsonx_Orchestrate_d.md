# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 17:09:41
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Support Assistant POC

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building the "Xerox Support Assistant" Proof of Concept (POC) using IBM watsonx Orchestrate. The plan is tailored specifically to Xerox's business needs, demonstrating how a multi-agent AI system can automate first-level customer support to enhance efficiency and customer satisfaction.

The core of this solution is a **Supervisor Agent** (`XeroxSupportAssistant`) that intelligently manages customer interactions. It first attempts to resolve issues by leveraging a Retrieval-Augmented Generation (RAG) pattern with a specialized **Collaborator Agent** (`ProductKnowledgeAgent`) that queries a knowledge base of Xerox product manuals and FAQs. If self-service resolution fails or is inappropriate, the supervisor seamlessly escalates the issue to another **Collaborator Agent** (`ServiceDeskAgent`), which uses a custom tool to create a support ticket in a simulated service desk system. This architecture directly addresses Xerox's goals of providing 24/7 instant support, reducing operational costs, and increasing first-contact resolution rates.

## 2. Prerequisites

Before beginning the implementation, ensure your environment is correctly configured.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate[all]" --upgrade
    ```
*   **Python**: A recent version of Python (3.9 or higher) is required.
*   **Orchestrate Environment**: You must be logged into your watsonx Orchestrate environment. If you are not logged in, run `orchestrate login` and follow the prompts.
*   **Project Structure**: Create a root folder for the project (e.g., `xerox-poc`) and establish the following directory structure to organize your files. This structure is critical for the commands to work correctly.

    ```
    xerox-poc/
    ├── mock_data/
    │   ├── AltaLink_C8055_Manual.pdf
    │   ├── VersaLink_B7030_Manual.pdf
    │   └── Xerox_FAQs.txt
    ├── knowledge_bases/
    │   └── xerox_knowledge_base.yaml
    ├── tools/
    │   └── ticketing.py
    ├── agents/
    │   ├── ProductKnowledgeAgent.yaml
    │   ├── ServiceDeskAgent.yaml
    │   └── XeroxSupportAssistant.yaml
    └── requirements.txt
    ```

## 3. Step-by-Step Implementation

This section details the creation of all components, from the underlying data and tools to the final supervisor agent.

### Step 3.1: Prepare Mock Data and Knowledge Base

The `ProductKnowledgeAgent` relies on a knowledge base to answer customer questions. We will create mock documents that simulate real Xerox support materials and configure a knowledge base to ingest them.

1.  **Create Mock Documents**: In the `mock_data/` directory, create the following three files.
    *   **`Xerox_FAQs.txt`**: This file contains answers to common, general questions.
        ```text
        // mock_data/Xerox_FAQs.txt

        Q: How do I order more toner for my printer?
        A: You can order new toner cartridges directly from the Xerox website at xerox.com/supplies. Please have your printer's model and serial number ready. You can also sign up for our automated supplies replenishment program.

        Q: How do I set up scan-to-email?
        A: To set up scan-to-email, access the printer's Embedded Web Server by typing its IP address into a browser. Navigate to Properties > Connectivity > Protocols > Email Settings. Enter your SMTP server details, port, and authentication credentials.
        ```
    *   **`AltaLink_C8055_Manual.pdf`**: Create a simple PDF document containing the following text. This file simulates a product-specific manual with technical error codes.
        ```text
        // Content for mock_data/AltaLink_C8055_Manual.pdf

        Xerox AltaLink C8055 Series - Troubleshooting Guide

        Error Code Table:
        - Code: 077-900, Description: Paper Jam in Fuser, Solution: Open Door C and carefully remove the jammed paper.
        - Code: 077-901, Description: Paper Jam in Tray 2, Solution: 1. Pull out Tray 2 completely. 2. Remove any jammed paper. Ensure the paper guides are set correctly. 3. Re-insert the tray firmly.
        - Code: 116-324, Description: Internal System Error, Solution: Power the device off and on again. If the error persists, contact support.
        ```
    *   **`VersaLink_B7030_Manual.pdf`**: Create a second PDF document with different content.
        ```text
        // Content for mock_data/VersaLink_B7030_Manual.pdf

        Xerox VersaLink B7030 Series - User Manual

        Feature Overview:
        - Mobile Printing: Supported via Apple AirPrint, Mopria, and the Xerox Print Portal app.
        - Security: Includes Secure Print, user authentication, and network encryption.
        ```

2.  **Define the Knowledge Base**: In the `knowledge_bases/` directory, create the `xerox_knowledge_base.yaml` file. This configuration tells Orchestrate to ingest the mock documents into a built-in Milvus vector database, making them searchable.

    ```yaml
    # knowledge_bases/xerox_knowledge_base.yaml
    spec_version: v1
    kind: knowledge_base
    name: XeroxProductKnowledge
    description: >
      Contains technical manuals, troubleshooting guides, and FAQs for Xerox printers, including AltaLink and VersaLink series. This knowledge base is the primary source for resolving technical errors and answering product feature questions.
    documents:
      - "mock_data/AltaLink_C8055_Manual.pdf"
      - "mock_data/VersaLink_B7030_Manual.pdf"
      - "mock_data/Xerox_FAQs.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 3.2: Develop the Service Desk Tool

This Python tool simulates creating a support ticket. The agent will use the function's docstring to understand its purpose and parameters, enabling it to conversationally gather the required information from the user.

1.  **Create the Python Tool**: In the `tools/` directory, create the file `ticketing.py`.

    ```python
    # tools/ticketing.py
    import random
    from datetime import datetime
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="create_support_ticket", permission=ToolPermission.ADMIN)
    def create_support_ticket(customer_name: str, printer_model: str, serial_number: str, problem_description: str) -> str:
        """
        Creates a new support ticket in the Xerox service desk system when a customer's issue cannot be resolved through the knowledge base.

        Args:
            customer_name (str): The full name of the customer requesting support.
            printer_model (str): The model of the Xerox printer (e.g., 'AltaLink C8055').
            serial_number (str): The unique serial number of the printer, usually found on a sticker on the back.
            problem_description (str): A detailed description of the issue the customer is facing, including any error codes and steps already tried.

        Returns:
            str: A confirmation message with the newly created ticket number.
        """
        # This function simulates an API call to a real service desk system like ServiceNow or Zendesk.
        # In a real implementation, this would involve an HTTP request with authentication.
        try:
            ticket_id = f"XRX-{random.randint(90000, 99999)}"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{timestamp}] INFO: Creating ticket {ticket_id} for {customer_name} regarding {printer_model} (S/N: {serial_number})...")
            print(f"[{timestamp}] INFO: Problem: {problem_description}")

            # Simulate a successful API call
            confirmation_message = f"Success! Your support ticket {ticket_id} has been created. A Xerox support specialist will contact you shortly."
            return confirmation_message

        except Exception as e:
            error_message = f"An error occurred while creating the support ticket: {str(e)}"
            print(f"[{timestamp}] ERROR: {error_message}")
            return error_message
    ```

2.  **Create `requirements.txt`**: In the project root, create this file. While our simple tool has no external dependencies beyond the ADK, it's a best practice to include it.

    ```text
    # requirements.txt
    # No external packages required for this specific tool.
    # If using libraries like 'requests', they would be listed here.
    requests
    ```

### Step 3.3: Define the Collaborator Agents

Collaborator agents are specialists that perform specific tasks. We will create two: one for knowledge retrieval and one for ticket creation.

1.  **Create the `ProductKnowledgeAgent`**: This agent's sole purpose is to use the knowledge base. In the `agents/` directory, create `ProductKnowledgeAgent.yaml`.

    ```yaml
    # agents/ProductKnowledgeAgent.yaml
    spec_version: v1
    kind: native
    name: ProductKnowledgeAgent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent for retrieving information from Xerox's technical documentation. Use this agent to answer questions about product features, troubleshooting steps, and specific error codes found in product manuals and FAQs.
    instructions: >
      You are an expert at searching and synthesizing information from technical documents. Your goal is to provide clear, accurate answers based ONLY on the content within the provided knowledge base. If the answer is not in the documents, state that you cannot find the information.
    tools: []
    collaborators: []
    knowledge_base:
      - XeroxProductKnowledge
    ```

2.  **Create the `ServiceDeskAgent`**: This agent is a specialist that uses the `create_support_ticket` tool. In the `agents/` directory, create `ServiceDeskAgent.yaml`.

    ```yaml
    # agents/ServiceDeskAgent.yaml
    spec_version: v1
    kind: native
    name: ServiceDeskAgent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A specialist agent that interfaces with the support ticketing system. Its only function is to create support tickets when a user's problem requires human intervention.
    instructions: >
      Your purpose is to create support tickets. Use the create_support_ticket tool to do this. Before calling the tool, ensure you have gathered all necessary information from the user: their full name, the printer model, the serial number, and a detailed description of the problem. Be polite and conversational while collecting these details.
    tools:
      - create_support_ticket
    collaborators: []
    ```

### Step 3.4: Define the Supervisor Agent

The `XeroxSupportAssistant` is the main, customer-facing agent. It doesn't perform tasks itself but intelligently routes requests to its specialist collaborators based on the user's intent.

1.  **Create the `XeroxSupportAssistant`**: In the `agents/` directory, create `XeroxSupportAssistant.yaml`. The `instructions` are critical here as they define the core business logic for escalation.

    ```yaml
    # agents/XeroxSupportAssistant.yaml
    spec_version: v1
    kind: native
    name: XeroxSupportAssistant
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        A primary customer support assistant for Xerox products. It acts as a first point of contact, capable of answering product questions using a knowledge base and creating support tickets for complex issues.
    instructions: >
        You are the Xerox Support Assistant. Your primary goal is to help Xerox customers solve their problems efficiently.
        1.  First, always try to answer the user's question or resolve their technical issue by using the ProductKnowledgeAgent. This agent has access to all product manuals and FAQs.
        2.  If the user indicates that the solution provided by the ProductKnowledgeAgent did not work, or if they explicitly ask to speak to a human, create a ticket, or request further assistance, you must escalate.
        3.  To escalate, use the ServiceDeskAgent to create a support ticket. Do not use this agent for any other purpose.
    collaborators:
      - ProductKnowledgeAgent
      - ServiceDeskAgent
    tools: []
    ```

### Step 3.5: Deploy the Solution using the ADK CLI

With all configuration files in place, you can now import them into watsonx Orchestrate. The order of these commands is **critical**. You must import dependencies (knowledge bases, tools) before the agents that rely on them, and collaborator agents before the supervisor that uses them.

Execute these commands from the root of your `xerox-poc/` directory.

1.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/xerox_knowledge_base.yaml
    ```
    *This command starts the ingestion process. It may take a few minutes for the documents to be processed and indexed. You can check the status with `orchestrate knowledge-bases status --name XeroxProductKnowledge`.*

2.  **Import the Tool**:
    ```bash
    orchestrate tools import -f tools/ticketing.py
    ```

3.  **Import the Collaborator Agents**:
    ```bash
    orchestrate agents import -f agents/ProductKnowledgeAgent.yaml
    orchestrate agents import -f agents/ServiceDeskAgent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/XeroxSupportAssistant.yaml
    ```

## 4. Verification and Demo Scenarios

After successfully importing all components, you can test the complete workflow by interacting with the supervisor agent.

**Start the Chat Session:**
Run the following command to start a chat session directly with your main agent.

```bash
orchestrate chat start --agent XeroxSupportAssistant
```

Now, run through the following demo scenarios to verify the functionality.

*   **Scenario 1: Simple FAQ Query**
    *   **User Input:** `How do I order more toner for my printer?`
    *   **Expected Behavior:** The `XeroxSupportAssistant` should recognize this as an informational query and route it to the `ProductKnowledgeAgent`.
    *   **Expected Output:** The agent should respond with the answer from `Xerox_FAQs.txt`, explaining how to order toner from the Xerox website.

*   **Scenario 2: Specific Error Code Resolution**
    *   **User Input:** `My AltaLink printer is showing error 077-901. How do I fix it?`
    *   **Expected Behavior:** The `XeroxSupportAssistant` routes the technical query to the `ProductKnowledgeAgent`.
    *   **Expected Output:** The agent should find the specific error code in the `AltaLink_C8055_Manual.pdf` content and provide the step-by-step troubleshooting instructions.

*   **Scenario 3: Escalation to Human Agent**
    *   **User Input (after trying Scenario 2):** `I tried the steps for error 077-901, but it's still not working.`
    *   **Expected Behavior:** The `XeroxSupportAssistant`'s instructions will trigger an escalation. It will invoke the `ServiceDeskAgent`. The `ServiceDeskAgent` will then start a conversation to gather the necessary information for the `create_support_ticket` tool.
    *   **Example Interaction:**
        *   **Agent:** "I'm sorry to hear that didn't resolve the issue. I can create a support ticket for you. What is your full name?"
        *   **User:** `John Doe`
        *   **Agent:** "Thank you, John. And what is the serial number of your AltaLink C8055?"
        *   **User:** `X123456789`
        *   **Agent:** "Got it. I'm creating the ticket now."
    *   **Expected Output:** The agent will provide a confirmation message like: `"Success! Your support ticket XRX-98765 has been created. A Xerox support specialist will contact you shortly."`

## 5. Troubleshooting

*   **Issue: Agent cannot find information in the knowledge base.**
    *   **Solution:**
        1.  Verify the knowledge base is ready by running `orchestrate knowledge-bases status --name XeroxProductKnowledge`. The status should be `Ready`.
        2.  Check that the file paths in `xerox_knowledge_base.yaml` are correct relative to your project root.
        3.  For PDF documents with complex tables or layouts, the default chunking may not be optimal. For a production scenario, consider converting complex tables to a more structured format like CSV or simplifying the PDF layout.

*   **Issue: Supervisor agent fails to escalate to the `ServiceDeskAgent`.**
    *   **Solution:**
        1.  The quality of the `instructions` in `XeroxSupportAssistant.yaml` is paramount. Ensure they are explicit about the conditions for escalation (e.g., "If the user says the solution didn't work...").
        2.  The `description` of the `ServiceDeskAgent` must clearly state its purpose. The supervisor LLM uses these descriptions to make routing decisions.

*   **Issue: Agent import fails with "collaborator not found" or "tool not found".**
    *   **Solution:** This is almost always due to an incorrect import order. Ensure you import knowledge bases and tools first, followed by the collaborator agents that use them, and finally the supervisor agent.

## 6. Best Practices

*   **Modular Design**: The supervisor-collaborator pattern is a powerful best practice. It keeps agents focused on a single responsibility, making the system easier to build, test, and maintain. You can add new capabilities simply by creating a new specialist agent and updating the supervisor's instructions.
*   **Descriptive Metadata**: The LLM relies heavily on the `name`, `description`, and `instructions` of agents, as well as the docstrings of tools, to make decisions. Write clear, descriptive, and action-oriented text for these fields.
*   **Explicit Instructions**: When designing a supervisor agent, be as explicit as possible in the instructions. Define the "rules of engagement" for when to use each collaborator to guide the LLM's reasoning process and ensure predictable behavior.
*   **Knowledge Base Curation**: For a real-world implementation, the quality of the documents in your knowledge base is the most critical factor for RAG success. Ensure documents are well-structured, up-to-date, and free of unnecessary clutter.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
