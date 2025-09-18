import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock inventory database, simulating a real-time connection to a stock management system.
# We've included items with similar names to test ambiguity handling.
INVENTORY = {
    'espresso_beans_kg': 5.5,
    'oat_milk_cartons': 12,
    'vanilla_syrup_bottles': 3,
    'caramel_syrup_bottles': 6,
    'sugar_free_caramel_syrup_bottles': 2,
    'mocha_sauce_bottles': 4,
    'white_mocha_sauce_bottles': 0,
    'grande_hot_cups_sleeve': 8,
    'venti_cold_cups_sleeve': 11
}

@tool(name="check_inventory", permission=ToolPermission.ADMIN)
def check_inventory(item_name: str) -> str:
    """
    Checks the current stock level for a specific inventory item. Use this tool
    when a user asks about the quantity of an item, such as 'how many vanilla syrup bottles do we have'.

    Args:
        item_name (str): The specific name of the inventory item to check.
                         Example format: 'vanilla_syrup_bottles', 'espresso_beans_kg'.

    Returns:
        str: A message indicating the current stock level, asking for clarification if the item is ambiguous, or stating if the item is not found.
    """
    normalized_item = item_name.lower().replace(" ", "_")
    
    # First, try for an exact match
    if normalized_item in INVENTORY:
        stock_level = INVENTORY[normalized_item]
        return f"We currently have {stock_level} units of {normalized_item} in stock."

    # If no exact match, search for partial matches
    possible_matches = [key for key in INVENTORY.keys() if normalized_item in key]
    
    if len(possible_matches) == 1:
        found_key = possible_matches[0]
        stock_level = INVENTORY[found_key]
        return f"We currently have {stock_level} units of {found_key} in stock."
    elif len(possible_matches) > 1:
        # If multiple matches are found, ask the user for clarification.
        options = ", ".join(possible_matches)
        return f"I found multiple items matching '{item_name}'. Can you be more specific? Options are: {options}."
    else:
        return f"Sorry, I could not find the item '{item_name}' in the inventory system."

@tool(name="report_equipment_issue", permission=ToolPermission.ADMIN)
def report_equipment_issue(equipment_name: str, issue_description: str) -> str:
    """
    Logs a maintenance ticket for a piece of broken or malfunctioning equipment.
    Use this when a user reports a problem like 'the grinder is making a weird noise' or 'the espresso machine is leaking'.

    Args:
        equipment_name (str): The name of the equipment that is broken (e.g., 'Espresso Grinder', 'Main Ice Machine').
        issue_description (str): A detailed description of the problem.

    Returns:
        str: A confirmation message with a generated ticket number.
    """
    ticket_id = random.randint(10000, 99999)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # This print block simulates logging to a backend system or service desk application.
    print(f"--- MOCK TICKETING SYSTEM ---")
    print(f"Timestamp: {timestamp}")
    print(f"Equipment: {equipment_name}")
    print(f"Issue: {issue_description}")
    print(f"Ticket ID: {ticket_id}")
    print(f"---------------------------")
    
    return f"SUCCESS: I've logged the issue for '{equipment_name}' with description '{issue_description}'. Your ticket number is #{ticket_id}."