import json
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="order_supplies", permission=ToolPermission.ADMIN)
    def order_supplies(part_number: str, quantity: int) -> dict:
        """
        Orders a specific part number and quantity from the supply chain inventory system.

        Args:
            part_number (str): The unique identifier for the part or supply to order.
            quantity (int): The number of units to order.

        Returns:
            dict: A confirmation message with the order details and status.
        """
        try:
            with open(config.INVENTORY_FILE, "r") as f:
                inventory = json.load(f)

            if part_number not in inventory:
                logging.warning(f"Order failed: Part number {part_number} not found.")
                return {"status": "error", "message": f"Part number {part_number} not found."}

            if inventory[part_number]["stock_level"] < quantity:
                logging.info(f"Insufficient stock for {part_number}. Order backordered.")
                return {"status": "backordered", "message": f"Insufficient stock for {part_number}."}

            inventory[part_number]["stock_level"] -= quantity
            with open(config.INVENTORY_FILE, "w") as f:
                json.dump(inventory, f, indent=2)

            logging.info(f"Order placed for {quantity} of {part_number}.")
            return {"status": "success", "message": f"Order placed for {quantity} of {part_number}."}
        except Exception as e:
            logging.error(f"Failed to process order for part {part_number}: {e}")
            return {"status": "error", "message": str(e)}