#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves initializing the ADK and logging in. If this is your first time, follow the official documentation to run `orchestrate login` and `orchestrate env create`.
4.  **Project Directory Structure**: To organize all assets for this demo, create the following directory structure in your local development environment:

    ```
    corepower_demo/
    ├── agents/
    │   ├── member_concierge_agent.yaml
    │   ├── wellness_advisor_agent.yaml
    │   └── class_scheduler_agent.yaml
    ├── tools/
    │   └── corepower_tools.py
    ├── knowledge_base/
    │   └── corepower_kb.yaml
    ├── mock_data/
    │   ├── Class_Descriptions.pdf
    │   ├── Wellness_and_Nutrition_Guide.pdf
    │   ├── Membership_FAQs.txt
    │   ├── class_schedule.json
    │   └── member_profiles.json
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Project Files

The foundation of this demo is realistic, domain-specific data that simulates CorePower's operational environment. We will create the necessary data files that our knowledge base and tools will use.

1.  **Create Mock Knowledge Base Documents**:
    *   Create two PDF files, `Class_Descriptions.pdf` and `Wellness_and_Nutrition_Guide.pdf`, with relevant content about CorePower's offerings.
    *   In the `mock_data/` directory, create `Membership_FAQs.txt` with the following content:

    ```txt
    # mock_data/Membership_FAQs.txt

    Q: What is the All Access membership?
    A: The All Access membership grants you unlimited access to all CorePower Yoga studios nationwide, including all class formats and online content.

    Q: How do I freeze my membership?
    A: You can freeze your membership for up to 90 days by contacting our support team through the member portal. A small monthly freeze fee applies.

    Q: What is the cancellation policy?
    A: We require a 30-day written notice for all membership cancellations. Please submit your request via the online member portal to ensure it is processed correctly.
    ```

2.  **Create Mock JSON Data for Tools**:
    *   In the `mock_data/` directory, create `class_schedule.json`:

    ```json
    // mock_data/class_schedule.json
    [
      {"class_id": "YS101", "class_name": "Yoga Sculpt", "studio": "Downtown", "instructor": "Alex Ray", "start_time": "2024-10-28T18:00:00Z", "duration_minutes": 60, "day": "tomorrow"},
      {"class_id": "C2-102", "class_name": "C2 CorePower Yoga", "studio": "Downtown", "instructor": "Maria Garcia", "start_time": "2024-10-28T09:00:00Z", "duration_minutes": 60, "day": "tomorrow"},
      {"class_id": "HPF-103", "class_name": "Hot Power Fusion", "studio": "Northside", "instructor": "Sam Chen", "start_time": "2024-10-27T19:00:00Z", "duration_minutes": 75, "day": "today"},
      {"class_id": "C2-104", "class_name": "C2 CorePower Yoga", "studio": "Northside", "instructor": "Emily White", "start_time": "2024-10-27T17:30:00Z", "duration_minutes": 60, "day": "today"}
    ]
    ```

    *   In the `mock_data/` directory, create `member_profiles.json`:

    ```json
    // mock_data/member_profiles.json
    [
      {"member_id": "CP7890", "name": "Jane Doe", "membership_level": "All Access", "join_date": "2023-01-15", "next_billing_date": "2024-11-01"},
      {"member_id": "CP1234", "name": "John Smith", "membership_level": "Studio Pass", "join_date": "2024-03-20", "next_billing_date": "2024-11-20"}
    ]
    ```

3.  **Create the `requirements.txt` file**:
    *   This file lists the Python dependencies for our tools. In this case, we only need the `requests` library for demonstrating a common pattern, though our local implementation doesn't strictly require it.

    ```txt
    # requirements.txt
    requests
    ```

## Step 2: Create the Knowledge Base Configuration

The `Wellness_Advisor_Agent` will use a knowledge base to provide accurate, brand-consistent answers. This is achieved through Retrieval-Augmented Generation (RAG), where the agent retrieves information from CorePower's documents before generating a response.

Create the file `knowledge_base/corepower_kb.yaml` with the following configuration. This file defines a built-in Milvus knowledge base that will ingest the documents we created.

