# flight_crew_tools.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock database of pre-flight procedures
PROCEDURE_DATABASE = {
    "de-icing_communications_check": {
        "name": "De-Icing Communications Check",
        "source": "FCOM Vol 2, Section 5.3, Page 12",
        "steps": [
            "1. Establish communication with de-icing crew on designated frequency.",
            "2. Confirm aircraft type and tail number.",
            "3. State the required de-icing fluid type (e.g., Type I, Type IV).",
            "4. Verbally confirm critical surfaces to be treated (wings, tail, stabilizers).",
            "5. Receive confirmation from de-icing crew that procedure is understood.",
            "6. Await 'De-icing complete' call before continuing pre-flight."
        ]
    },
    "cold_weather_engine_start": {
        "name": "Cold Weather Engine Start Procedure (OAT < 0°C)",
        "source": "FCOM Vol 1, Section 3.2, Page 45",
        "steps": [
            "1. Verify engine oil quantity is within limits.",
            "2. Ensure APU bleed is ON.",
            "3. Set Engine Start selectors to IGN/START.",
            "4. Monitor N2 rotation; must be at least 20% before introducing fuel.",
            "5. At 20% N2, move Engine Master Switch to ON.",
            "6. Monitor EGT, N1, and oil pressure for normal parameters during start sequence."
        ]
    }
}

@tool(name="get_preflight_procedure", permission=ToolPermission.ADMIN)
def get_preflight_procedure(procedure_name: str) -> str:
    """
    Retrieves a specific, step-by-step pre-flight procedure from the operations manual.

    Args:
        procedure_name (str): The standardized name of the procedure to retrieve, e.g., 'de-icing_communications_check' or 'cold_weather_engine_start'.

    Returns:
        str: A JSON string containing the detailed procedure steps and source reference, or a message if not found.
    """
    # Normalize the input to handle variations
    lookup_key = procedure_name.lower().replace(" ", "_")
    
    procedure = PROCEDURE_DATABASE.get(lookup_key)
    
    if procedure:
        return json.dumps(procedure, indent=2)
    else:
        return json.dumps({"error": "Procedure not found.", "available_procedures": list(PROCEDURE_DATABASE.keys())})