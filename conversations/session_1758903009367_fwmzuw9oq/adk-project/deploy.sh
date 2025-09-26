#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. If you haven't done so, run:
    ```bash
    orchestrate env init --name my-dev-env
    ```
    Follow the prompts to configure your environment.
*   **Project Structure:** Create the following directory structure to organize your files:
    ```
    barista_buddy_demo/
    |-- agents/
    |   |-- 1_hr_connect_agent.yaml
    |   |-- 2_onboarding_pro_agent.yaml
    |   |-- 3_recipe_and_ops_agent.yaml
    |   |-- 4_barista_buddy_agent.yaml
    |-- tools/
    |   |-- onboarding_tools.py
    |   |-- hr_tools.py
    |-- knowledge_base/
    |   |-- documents/
    |   |   |-- Barista_Recipe_Book.pdf
    |   |   |-- Espresso_Machine_Troubleshooting_Guide.pdf
    |   |   |-- Employee_Handbook.docx
    |   |-- barista_knowledge.yaml
    |-- requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Prepare Mock Data and Knowledge Base

The `Recipe_And_Ops_Agent` relies on a knowledge base for providing information on drink recipes, equipment, and company policies. We will create this using the built-in Milvus vector database provided by watsonx Orchestrate.

**A. Create Mock Documents:**

In the `barista_buddy_demo/knowledge_base/documents/` directory, create the following files with sample content. These will be ingested into the knowledge base.

*   `Barista_Recipe_Book.pdf`: A PDF containing recipes. (e.g., "Caramel Macchiato: 1 shot espresso, 2 pumps vanilla syrup, steamed milk, caramel drizzle.")
*   `Espresso_Machine_Troubleshooting_Guide.pdf`: A PDF with common issues. (e.g., "Problem: Low pressure. Solution: Check the water tank and ensure the portafilter is sealed correctly.")
*   `Employee_Handbook.docx`: A document with store policies. (e.g., "Dress Code: All employees must wear a company-provided apron and non-slip shoes.")

**B. Create the Knowledge Base Configuration File:**

This YAML file defines the knowledge base, its description, and the documents to be ingested. The description is crucial as it helps agents understand what information this knowledge base contains.

`barista_buddy_demo/knowledge_base/barista_knowledge.yaml`

