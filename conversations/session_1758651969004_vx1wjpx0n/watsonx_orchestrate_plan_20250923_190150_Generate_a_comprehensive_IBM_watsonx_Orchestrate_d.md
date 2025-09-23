# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 19:01:50
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Document Assistant

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Document Assistant" for the client. The solution directly addresses the client's need to make document interaction more efficient and intuitive by transforming static documents into dynamic, conversational knowledge sources. We will construct a multi-agent system using the IBM watsonx Orchestrate Agent Development Kit (ADK) that allows users to summarize, translate, and ask specific questions about their documents using natural language.

The architecture leverages a core IBM watsonx Orchestrate pattern: a **Supervisor Agent** (`Document_Orchestrator_Agent`) that intelligently routes user requests to specialized **Collaborator Agents** (`Summarization_Agent`, `Translation_Agent`) and a **Knowledge Base** (`Company_Reports_KB`). This modular design demonstrates a scalable and powerful approach to building sophisticated AI assistants, delivering significant business value through productivity gains, enhanced data accessibility, and accelerated decision-making.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured.

*   **Python:** Python version 3.10 or higher installed.
*   **IBM watsonx Orchestrate ADK:** The ADK must be installed and configured. If you haven't installed it, run:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. If not, run `orchestrate env init` and follow the prompts.
*   **Project Directory:** Create a dedicated project folder to organize all configuration files, tools, and mock data. We recommend the following structure:
    ```
    document-assistant-demo/
    ├── agents/
    ├── tools/
    ├── knowledge_bases/
    ├── mock_data/
    └── requirements.txt
    ```

## 3. Step 1: Create Mock Data and Knowledge Base

The foundation of our demo is the ability to reason over specific documents. We will create a knowledge base to ingest our mock data, making it searchable for the Q&A use case.

**Business Value:** A knowledge base provides the agent with "ground truth" information, enabling it to answer questions with high accuracy and provide citations back to the source documents. This Retrieval-Augmented Generation (RAG) pattern is crucial for enterprise-grade AI assistants that must rely on factual, proprietary data.

### 3.1. Create Mock Documents

Inside the `mock_data/` directory, create the following three files with sample content.

**`mock_data/Q4_Annual_Report.pdf`** (Create a simple text file and save as PDF, or use an existing one)
*Content Idea:*
> **Q4 2024 Financial Highlights:**
> - Total Revenue: $1.2 Billion, an increase of 15% year-over-year.
> - Net Profit: $250 Million, beating analyst expectations.
> - Key Growth Driver: Strong performance in the AI solutions division, which grew by 40%.
> **Executive Outlook:** We are optimistic about the upcoming year, with planned expansion into the European market and continued investment in R&D.

**`mock_data/Partner_Agreement.docx`** (Create a simple text file and save as DOCX)
*Content Idea:*
> **Termination Clause:**
> This Agreement may be terminated by either party upon ninety (90) days written notice to the other party. In the event of a material breach, the non-breaching party may terminate the Agreement with thirty (30) days written notice if the breach is not cured within that period.

**`mock_data/HR_Policy_Guide.txt`**
*Content Idea:*
> **Remote Work Policy:**
> Eligible employees may work remotely up to three (3) days per week, subject to manager approval. All remote work must be conducted from the employee's primary residence within the country. Employees are required to maintain a designated, safe, and ergonomic workspace.

### 3.2. Define the Knowledge Base YAML

Create a file named `company_reports_kb.yaml` inside the `knowledge_bases/` directory. This file configures a built-in Milvus knowledge base that will ingest and index the documents we just created.

**File: `knowledge_bases/company_reports_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: Company_Reports_KB
description: >
  Contains internal company documents like annual reports, legal agreements, and HR policies. Use this to answer specific questions about document contents.
documents:
  - "mock_data/Q4_Annual_Report.pdf"
  - "mock_data/Partner_Agreement.docx"
  - "mock_data/HR_Policy_Guide.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## 4. Step 2: Implement Specialist Tools

Tools are the building blocks that give agents their capabilities. We will create Python-based tools for document processing and an OpenAPI-based tool for translation.

### 4.1. Create Document Processing Tools (Python)

**Business Value:** These tools encapsulate complex logic (like parsing different file formats and summarizing text) into simple, reusable skills. By creating a dedicated `extract_text_from_file` tool, we make the system extensible to new document types without changing the core agent logic. The `generate_summary` tool directly addresses the client's need for rapid insights from dense reports.

Create a file named `summarizer_tools.py` in the `tools/` directory. This file will contain two tools.
*(Note: For a real implementation, you would install libraries like `pypdf` and `python-docx`. For this demo, we will mock the file reading to ensure it runs without extra installations, but include commented-out code showing the real approach.)*

**File: `tools/summarizer_tools.py`**
```python
import os
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="extract_text_from_file", description="Extracts raw text content from a specified file (PDF, DOCX, TXT).", permission=ToolPermission.ADMIN)
def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from various document formats.

    Args:
        file_path (str): The local path to the file (e.g., 'mock_data/HR_Policy_Guide.txt').

    Returns:
        str: The extracted text content from the file.
    """
    try:
        # This is a simplified mock for demo purposes.
        # In a real implementation, you would use libraries to parse file types.
        if not os.path.exists(file_path):
            return f"Error: File not found at path '{file_path}'"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

        # Example for a real implementation:
        # from pypdf import PdfReader
        # from docx import Document
        #
        # if file_path.endswith('.pdf'):
        #     reader = PdfReader(file_path)
        #     text = ""
        #     for page in reader.pages:
        #         text += page.extract_text()
        #     return text
        # elif file_path.endswith('.docx'):
        #     doc = Document(file_path)
        #     return "\\n".join([para.text for para in doc.paragraphs])
        # elif file_path.endswith('.txt'):
        #     with open(file_path, 'r') as f:
        #         return f.read()
        # else:
        #     return "Error: Unsupported file format."

    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


@tool(name="generate_summary", description="Generates a concise summary of a given block of text.", permission=ToolPermission.ADMIN)
def generate_summary(text: str, length: str = "medium", points: int = 3) -> str:
    """
    Generates a summary of the provided text.

    Args:
        text (str): The text content to be summarized.
        length (str): The desired length of the summary ('short', 'medium', 'long').
        points (int): The number of bullet points for the summary.

    Returns:
        str: The generated summary.
    """
    # Mock logic for summarization. In a real scenario, this would call a summarization model.
    summary_intro = f"Here is a {length}, {points}-bullet point summary of the document:\n"
    
    # Simple logic to grab first few lines as a mock summary
    lines = text.strip().split('\n')
    bullet_points = [f"- {line.strip()}" for line in lines[:points] if line.strip()]
    
    if not bullet_points:
        return "Could not generate a summary from the provided text."
        
    return summary_intro + "\n".join(bullet_points)

```

### 4.2. Create Translation Tool (OpenAPI)

**Business Value:** This demonstrates how watsonx Orchestrate can seamlessly integrate with existing external services and APIs (like IBM Watson Language Translator or a third-party service). This pattern is essential for extending the assistant's capabilities beyond Python-based logic and connecting to enterprise systems.

Create a file named `translator_api.yaml` in the `tools/` directory. This OpenAPI specification defines the `translate_text` tool.

**File: `tools/translator_api.yaml`**
```yaml
openapi: 3.0.0
info:
  title: Mock Translation API
  version: 1.0.0
  description: API for translating text between languages.
servers:
  - url: https://mock-translation-service.com/api # This is a placeholder and will not be called.
paths:
  /translate:
    post:
      operationId: translate_text
      summary: Translates text to a target language.
      description: Provides multilingual translation capabilities. Takes text and a target language as input and returns the translated content.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                  description: The text to be translated.
                target_language:
                  type: string
                  description: The target language (e.g., 'Spanish', 'French').
              required:
                - text
                - target_language
      responses:
        '200':
          description: Successful translation
          content:
            application/json:
              schema:
                type: object
                properties:
                  translated_text:
                    type: string
                    example: "Este es un texto traducido."
```

### 4.3. Create `requirements.txt`

For a full implementation, you'd need libraries to parse documents. Create a `requirements.txt` file at the root of your project folder.

**File: `requirements.txt`**
```
# For a full implementation, uncomment the following lines:
# pypdf
# python-docx
requests
```

## 5. Step 3: Configure Agents

With the tools and knowledge base defined, we now configure the agents that will use them. We will create two specialist agents and one supervisor agent to manage them.

### 5.1. Configure Specialist Agents

These agents are experts in a single domain (summarization or translation). They are not user-facing but are called by the supervisor.

**File: `agents/summarization_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Summarization_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  An expert agent for processing and summarizing text. It can extract text from various document formats (PDF, DOCX, TXT) and generate concise summaries based on user specifications.
instructions: >
  Your sole purpose is to summarize documents.
  1. First, use the 'extract_text_from_file' tool to get the content from the file path provided.
  2. Then, use the 'generate_summary' tool on the extracted text to create the summary.
  3. Return only the final summary. Do not add any conversational text.
tools:
  - extract_text_from_file
  - generate_summary
```

**File: `agents/translation_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Translation_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  A specialized agent that provides multilingual translation capabilities. It takes text and a target language as input and returns the translated content by using the translate_text tool.
instructions: >
  Your only job is to translate text. Use the 'translate_text' tool to perform the translation. Respond only with the translated text.
tools:
  - translate_text
```

### 5.2. Configure the Supervisor Agent

This is the primary, user-facing agent. Its main role is to understand the user's intent and delegate the task to the correct collaborator agent or knowledge base.

**File: `agents/document_orchestrator.yaml`**
```yaml
spec_version: v1
kind: native
name: Document_Orchestrator_Agent
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
description: >
  Your primary assistant for document tasks. You can summarize, translate, and answer questions about uploaded documents by collaborating with other specialized agents and searching a knowledge base.
instructions: >
  You are a helpful AI Document Assistant. Your goal is to help users with their documents.
  - When a user asks for a summary of a document, you MUST use the Summarization_Agent. Provide the file path to the agent.
  - When a user asks for a translation, you MUST use the Translation_Agent.
  - For general questions about the content of a document (e.g., "What is the policy on X?"), you MUST first consult the Company_Reports_KB knowledge base to find the answer.
  - Be polite and confirm the action you are taking.
collaborators:
  - Summarization_Agent
  - Translation_Agent
knowledge_base:
  - Company_Reports_KB
```

## 6. Step 4: Deploy the Solution

Now we will use the ADK's Command Line Interface (CLI) to import all our assets into the watsonx Orchestrate environment. The order is important to resolve dependencies correctly.

**Open your terminal, navigate to your project's root directory (`document-assistant-demo/`), and run these commands in sequence:**

1.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/company_reports_kb.yaml
    ```
    *This command registers the knowledge base and begins the process of ingesting and indexing the documents in the `mock_data` folder.*

2.  **Import the Python Tools:**
    ```bash
    orchestrate tools import -k python -f tools/summarizer_tools.py
    ```
    *This command parses the Python file, identifies the functions decorated with `@tool`, and makes them available as skills in Orchestrate.*

3.  **Import the OpenAPI Tool:**
    ```bash
    orchestrate tools import -k openapi -f tools/translator_api.yaml
    ```
    *This command registers the tool defined in the OpenAPI specification.*

4.  **Import the Specialist Agents:**
    ```bash
    orchestrate agents import -f agents/summarization_agent.yaml
    orchestrate agents import -f agents/translation_agent.yaml
    ```
    *This imports the collaborator agents, linking them to the tools we just imported.*

5.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/document_orchestrator.yaml
    ```
    *Finally, this imports the main agent, linking it to its collaborators and knowledge base.*

## 7. Step 5: Verification and Demo Execution

With everything deployed, you can now interact with the assistant and test the demo scenarios.

**Start the chat interface:**
```bash
orchestrate chat start --agent Document_Orchestrator_Agent
```

This will open a chat window in your browser. Use the following prompts to test each scenario:

#### **Scenario 1: Executive Summary on Demand**
*   **User Prompt:** `"Give me a three-bullet point summary of the key financial highlights from 'mock_data/Q4_Annual_Report.pdf'."`
*   **Expected Behind-the-Scenes Flow:**
    1.  `Document_Orchestrator_Agent` receives the request and identifies the intent to "summarize".
    2.  It delegates the task to its collaborator, `Summarization_Agent`, passing the file path.
    3.  `Summarization_Agent` uses its `extract_text_from_file` tool on the PDF.
    4.  It then passes the extracted text to its `generate_summary` tool.
    5.  The final summary is returned to the user through the orchestrator.
*   **Expected Output:** A message similar to "Here is a medium, 3-bullet point summary of the document..." followed by the key points from the mock report.

#### **Scenario 2: Cross-Border Contract Review**
*   **User Prompt:** `"Translate the 'Termination Clause' section from 'mock_data/Partner_Agreement.docx' into Spanish for our legal team in Madrid."`
*   **Expected Behind-the-Scenes Flow:**
    1.  `Document_Orchestrator_Agent` identifies the intent to "translate".
    2.  It delegates to the `Translation_Agent`.
    3.  `Translation_Agent` calls the `translate_text` tool. Since the tool is a mock, it will return a placeholder response.
*   **Expected Output:** A mock translated text, such as `"La cláusula de terminación ha sido traducida al español."`

#### **Scenario 3: Instant Policy Q&A**
*   **User Prompt:** `"What is the company policy on remote work?"`
*   **Expected Behind-the-Scenes Flow:**
    1.  `Document_Orchestrator_Agent` identifies this as a general question.
    2.  Following its instructions, it queries the `Company_Reports_KB` knowledge base.
    3.  The knowledge base performs a vector search and finds the relevant passage in `HR_Policy_Guide.txt`.
    4.  The agent synthesizes an answer based on the retrieved information and presents it to the user, likely with a citation.
*   **Expected Output:** An answer summarizing the remote work policy, such as "Eligible employees may work remotely up to three days per week, subject to manager approval."

## 8. Troubleshooting

*   **Import Fails:** If an import command fails, double-check the YAML syntax (especially indentation) and file paths. Ensure you are running the commands from the project's root directory. Use the `--debug` flag (e.g., `orchestrate agents import -f ... --debug`) for more detailed error logs.
*   **Incorrect Agent Routing:** If the supervisor agent doesn't delegate correctly, review its `instructions` and the `description` of the collaborator agents. The supervisor relies heavily on these descriptions to choose the right collaborator. Make them clear and distinct.
*   **Tool Not Found:** If an agent reports it cannot find a tool, ensure the tool was imported *before* the agent that uses it. Check the `tools` list in the agent's YAML file for typos in the tool name.
*   **Knowledge Base No Answer:** If the KB doesn't answer a question, check the `orchestrate knowledge-bases status --name Company_Reports_KB` command to ensure the documents have been indexed successfully. The process can take a few minutes. Also, ensure your question is specific enough to match the content in the mock documents.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
