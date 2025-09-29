#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
*   **Text Editor/IDE:** A code editor like Visual Studio Code, PyCharm, or Sublime Text for creating and editing Python and YAML files.
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment configured. Follow the official documentation to initialize your environment using the CLI.

## 3. Step-by-Step Instructions

### Step 3.1: Project Setup

First, create a structured directory for your project. This organization helps manage the various agent configurations and tool scripts cleanly.

1.  Create a main project folder:
    ```bash
    mkdir orchestrate-enterprise-demo
    cd orchestrate-enterprise-demo
    ```
2.  Create subdirectories for agents and tools:
    ```bash
    mkdir agents
    mkdir tools
    ```

Your project structure should look like this:

