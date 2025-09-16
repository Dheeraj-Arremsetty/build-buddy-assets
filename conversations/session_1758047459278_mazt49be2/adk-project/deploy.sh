#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate-sdk
    ```
3.  **Orchestrate CLI Authentication**: You must be logged into your watsonx Orchestrate environment via the CLI. If you have not configured this, follow the official documentation to set up your credentials. You can test your connection with:
    ```bash
    orchestrate whoami
    ```
4.  **Project Directory**: Create a dedicated folder for this demo to keep all files organized. This plan assumes you are running all commands from the root of this directory.

## Step 1: Set Up the Project Structure

A well-organized file structure is essential for managing agents and their associated tools. Create the following directory structure within your main project folder (e.g., `fincorp_demo`). This structure separates agent definitions from tool implementations, making the project scalable and easier to maintain.

