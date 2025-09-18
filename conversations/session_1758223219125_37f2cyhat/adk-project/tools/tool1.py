import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_store_procedure", permission=ToolPermission.ADMIN)
def get_store_procedure(procedure_name: str) -> str:
    """
    Retrieves the official, step-by-step instructions for a given store operating procedure. Use this tool to answer questions about how to perform operational tasks like cleaning equipment, following checklists, or handling specific situations.

    Args:
        procedure_name (str): The name of the procedure to look up. Examples include "closing checklist", "clean espresso machine", or "calibrate the grinder".

    Returns:
        str: The detailed steps for the procedure, or a message indicating the procedure was not found.
    """
    try:
        # It's important to use a relative path that works from where the orchestrate command is run
        with open('./tools/procedures.json', 'r') as f:
            procedures = json.load(f)
        # Use case-insensitive matching for robustness
        return procedures.get(procedure_name.lower(), f"I'm sorry, I couldn't find a procedure named '{procedure_name}'.")
    except FileNotFoundError:
        return "Error: The procedures data file could not be found. Please check the system configuration."
    except json.JSONDecodeError:
        return "Error: The procedures data file is not formatted correctly."