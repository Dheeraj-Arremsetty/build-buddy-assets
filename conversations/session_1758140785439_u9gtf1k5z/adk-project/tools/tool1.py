# tools/recipe_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="unit_converter_tool", description="Converts between common kitchen measurement units.")
def unit_converter_tool(quantity: float, from_unit: str, to_unit: str) -> str:
    """
    Converts between common kitchen measurement units like grams, ounces, cups.

    Args:
        quantity (float): The amount to convert.
        from_unit (str): The starting unit (e.g., 'cups', 'grams').
        to_unit (str): The target unit (e.g., 'ounces', 'ml').
    Returns:
        str: The converted quantity and unit as a string.
    """
    # Mock conversion logic for the demo
    # A real implementation would use a conversion library.
    if from_unit.lower() == "cups" and to_unit.lower() == "ml":
        converted_quantity = quantity * 236.588
        return f"{quantity} {from_unit} is approximately {converted_quantity:.2f} {to_unit}."
    elif from_unit.lower() == "ounces" and to_unit.lower() == "grams":
        converted_quantity = quantity * 28.35
        return f"{quantity} {from_unit} is approximately {converted_quantity:.2f} {to_unit}."
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported in this mock tool. A real tool would handle this."