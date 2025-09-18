import json
    import datetime
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="create_service_now_incident", permission=ToolPermission.ADMIN)
    def create_service_now_incident(description: str, device_id: str, priority: str, required_part: str = None) -> dict:
        """
        Creates a new service incident ticket in a mock ServiceNow system.

        Args:
            description (str): A detailed description of the incident.
            device_id (str): The unique identifier of the affected device.
            priority (str): The priority of the ticket (e.g., 'High', 'Medium', 'Low').
            required_part (str, optional): The part number required for the repair, if known.

        Returns:
            dict: A confirmation dictionary containing the new incident number and status.
        """
        try:
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Simulate ticket number generation
            with open(config.TICKETS_LOG_FILE, "a+") as f:
                f.seek(0)
                ticket_count = len(f.readlines())
                incident_number = f"INC{1001 + ticket_count:07d}"

            ticket_data = {
                "incident_number": incident_number, "timestamp": timestamp, "device_id": device_id,
                "description": description, "priority": priority, "required_part": required_part, "status": "New"
            }

            with open(config.TICKETS_LOG_FILE, "a") as f:
                f.write(json.dumps(ticket_data) + "\n")
            
            logging.info(f"Successfully created ticket {incident_number} for device {device_id}.")
            return {"status": "success", "incident_number": incident_number}
        except Exception as e:
            logging.error(f"Failed to create ServiceNow incident for device {device_id}: {e}")
            return {"status": "error", "message": str(e)}

    @tool(name="get_my_service_now_incidents", permission=ToolPermission.ADMIN)
    def get_my_service_now_incidents(location_filter: str = None) -> list[dict]:
        """
        Retrieves a list of service incidents. Can be filtered by a location string in the device ID.

        Args:
            location_filter (str, optional): A location code (e.g., 'Boston' or 'BOS') to filter incidents.

        Returns:
            list[dict]: A list of incident dictionaries matching the filter.
        """
        incidents = []
        try:
            with open(config.TICKETS_LOG_FILE, "r") as f:
                for line in f:
                    ticket = json.loads(line)
                    if location_filter and location_filter.lower() in ticket.get("device_id", "").lower():
                        incidents.append(ticket)
                    elif not location_filter:
                        incidents.append(ticket)
            return incidents
        except FileNotFoundError:
            logging.warning("ServiceNow tickets log file not found. Returning empty list.")
            return []
        except Exception as e:
            logging.error(f"Failed to retrieve incidents: {e}")
            return [{"error": f"Failed to retrieve incidents: {str(e)}"}]