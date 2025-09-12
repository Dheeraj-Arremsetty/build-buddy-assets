#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment Configuration**: Your ADK must be configured to connect to an IBM watsonx Orchestrate environment. Follow the official documentation for `orchestrate login` or setting up environment variables.
4.  **Project Directory**: Create a dedicated project folder to keep all files organized.

    ```bash
    # Create the main project directory
    mkdir barista_buddy_poc
    cd barista_buddy_poc

    # Create subdirectories for assets
    mkdir agents
    mkdir tools
    mkdir mock_data
    mkdir mock_data/docs
    ```

## Step 1: Create Mock Operational Documents and Knowledge Base

The `Operations_Knowledge_Agent` will use a knowledge base to answer questions about store procedures. This demonstrates the powerful RAG capabilities of watsonx Orchestrate, allowing the agent to provide accurate answers from your company's official documentation.

First, create the mock documents that will be ingested into the knowledge base.

1.  **Create `Espresso_Machine_Cleaning_Guide.txt`**:
    *   Path: `barista_buddy_poc/mock_data/docs/Espresso_Machine_Cleaning_Guide.txt`
    *   Content:
        ```text
        End-of-Day Espresso Machine Cleaning Protocol

        1. Backflush each group head with a blind filter basket and cleaning detergent. Run a 10-second cycle 5 times.
        2. Remove and clean the portafilters and baskets with hot water and a designated brush. Soak overnight in a detergent solution.
        3. Purge the steam wands to clear any milk residue. Wipe down with a sanitized cloth.
        4. Clean the drip tray and grate. Wash with soap and hot water, then sanitize.
        5. Wipe down all external surfaces of the machine with a clean, damp cloth.
        ```

2.  **Create `Customer_Complaint_Policy.txt`**:
    *   Path: `barista_buddy_poc/mock_data/docs/Customer_Complaint_Policy.txt`
    *   Content:
        ```text
        Customer Complaint Handling Policy

        Our policy is to Listen, Acknowledge, Solve, and Thank (LAST).
        - Listen: Give the customer your full attention.
        - Acknowledge: Acknowledge their frustration and apologize for their experience.
        - Solve: Offer a solution. This could be remaking their drink, offering a refund, or providing a voucher for their next visit. Empower yourself to make the customer happy.
        - Thank: Thank the customer for bringing the issue to our attention.
        ```

Now, create the YAML configuration for the knowledge base.

### Configuration File: `operations_kb.yaml`

This file defines the knowledge base, names it, describes its purpose, and points to the documents to be ingested. The `embeddings_model_name` specifies the model used to create vector embeddings for efficient searching.

*   Path: `barista_buddy_poc/knowledge_bases/operations_kb.yaml`

