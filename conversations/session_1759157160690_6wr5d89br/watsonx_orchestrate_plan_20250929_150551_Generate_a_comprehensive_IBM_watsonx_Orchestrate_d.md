# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 15:05:51
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Nespresso Launchpad

## Overview

This execution plan provides a comprehensive, step-by-step guide for building and demonstrating the **Nespresso Launchpad**, an AI-powered marketing campaign assistant using IBM watsonx Orchestrate. This solution is tailored specifically for Nespresso's business needs, demonstrating how a system of collaborating AI agents can automate and enhance the entire marketing campaign lifecycle, from initial market research to final performance analysis.

The plan details the creation of a supervisor agent, the **Marketing Campaign Manager**, which orchestrates a team of specialized collaborator agents for market research, content creation, social media management, and performance analytics. By leveraging custom tools with realistic synthetic Nespresso data and a knowledge base for brand information, this demo will showcase how watsonx Orchestrate can significantly improve campaign efficiency, data-driven decision-making, and brand consistency for Nespresso.

## Prerequisites

Before beginning, ensure your environment is set up with the following components. This setup is crucial for developing, importing, and running the agents and tools defined in this plan.

1.  **Python and pip**: Ensure Python (version 3.10 or later) and its package manager, `pip`, are installed on your system.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) is the core command-line tool used to build and manage Orchestrate assets. Install it using pip:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Active watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This could be the SaaS version or the local Developer Edition. Activate your environment using the CLI:
    ```bash
    orchestrate login
    orchestrate env activate <your_env_name>
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing the required Python and YAML files.

## Step 1: Project Setup

First, create a structured directory to organize all the assets for the Nespresso Launchpad demo. This organization is crucial for managing the different components as the project scales.

Open your terminal and execute the following commands:

```bash
# Create the main project directory
mkdir nespresso_launchpad_demo
cd nespresso_launchpad_demo

# Create subdirectories for agents, tools, and knowledge base documents
mkdir agents
mkdir tools
mkdir knowledge_docs
```

This structure will house the agent YAML files, Python tool scripts, and any documents for the knowledge base, respectively.

## Step 2: Create and Import the Knowledge Base

The knowledge base will provide the agent system with grounded, factual information about Nespresso's products, brand guidelines, and common customer questions (e.g., sustainability practices). This ensures brand-consistent and accurate responses for customer-facing content.

1.  **Create Mock Nespresso Documents**

    Inside the `knowledge_docs` directory, create a file named `nespresso_faqs.txt`. This file will contain synthetic data representing common customer inquiries.

    **File:** `knowledge_docs/nespresso_faqs.txt`
    ```txt
    NESPRESSO FREQUENTLY ASKED QUESTIONS

    Q: How do I recycle Nespresso pods?
    A: Nespresso offers several convenient ways to recycle your used aluminum capsules. You can drop them off at a Nespresso Boutique, a partner collection point, or mail them back to us using a free recycling bag. Our capsules are made from aluminum, an infinitely recyclable material.

    Q: What is the difference between Vertuo and Original coffee machines?
    A: The Original line brews classic espresso and lungo sizes, using high-pressure extraction. The Vertuo line uses Centrifusion™ technology to brew a wider range of coffee sizes, from single espresso to a large 14 oz. Alto, each with a rich, generous crema.

    Q: Are Nespresso coffees ethically sourced?
    A: Yes, over 95% of our coffee is sourced through our AAA Sustainable Quality™ Program, developed in partnership with the Rainforest Alliance. This program helps improve the yield and quality of harvests while protecting the environment and improving livelihoods of farmers.
    ```

2.  **Define the Knowledge Base YAML**

    Create a YAML file in the root project directory to define the knowledge base configuration. This file tells Orchestrate the name of the knowledge base and which documents to ingest.

    **File:** `nespresso_knowledge_base.yaml`
    ```yaml
    spec_version: v1
    kind: knowledge_base 
    name: nespresso_brand_knowledge
    description: >
       Contains essential Nespresso brand information, including product details for Vertuo and Original lines, official answers to frequently asked questions (FAQs), and guidelines on sustainability and pod recycling. Use this to answer specific customer questions or verify brand facts.
    documents:
       - "./knowledge_docs/nespresso_faqs.txt"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

3.  **Import the Knowledge Base**

    Use the ADK CLI to import this configuration into your watsonx Orchestrate environment.

    ```bash
    orchestrate knowledge-bases import -f nespresso_knowledge_base.yaml
    ```
    You can check the ingestion status with `orchestrate knowledge-bases status --name nespresso_brand_knowledge`.

## Step 3: Develop Python Tools

Tools are the executable skills that allow agents to perform actions. We will create a suite of tools for each specialized function within the marketing campaign lifecycle. Each tool will generate realistic, synthetic data relevant to Nespresso's business context.

1.  **Create `requirements.txt`**

    Create this file in the root project directory to manage Python dependencies.
    **File:** `requirements.txt`
    ```text
    requests
    ```

2.  **Market Research Tools**

    These tools help the `Market_Research_Agent` gather intelligence on market trends and competitor activities, providing a data-driven foundation for campaign strategy.

    **File:** `tools/market_research_tools.py`
    ```python
    import json
    import random
    from datetime import datetime, timedelta
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(permission=ToolPermission.ADMIN)
    def analyze_market_trends(topic: str) -> str:
        """
        Analyzes current market trends for a given topic, such as 'sustainable coffee' or 'at-home cafe experience'. 
        It provides insights on consumer interest, emerging keywords, and demographic engagement.

        Args:
            topic (str): The marketing topic to analyze (e.g., 'iced coffee recipes').

        Returns:
            str: A JSON string summarizing market trends, including search volume, sentiment, and key demographics.
        """
        trends = {
            "topic": topic,
            "analysis_date": datetime.now().isoformat(),
            "trend_summary": {
                "search_volume_growth": f"{random.uniform(5.5, 25.5):.2f}% MoM",
                "sentiment": {
                    "positive": f"{random.randint(70, 95)}%",
                    "neutral": f"{random.randint(5, 20)}%",
                    "negative": f"{random.randint(1, 10)}%"
                },
                "key_demographics": ["Millennials (25-40)", "Urban Dwellers", "Health-conscious consumers"],
                "emerging_keywords": ["cold brew at home", "sustainable pods", "espresso tonic", "coffee subscriptions"]
            },
            "recommendation": "High consumer interest in sustainability and convenience. Campaign should highlight N

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
