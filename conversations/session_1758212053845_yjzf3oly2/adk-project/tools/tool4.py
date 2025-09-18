import json
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="device_monitor", permission=ToolPermission.ADMIN)
    def get_alerts(min_severity: str = "WARNING") -> list[dict]:
        """
        Retrieves alerts from the printer fleet monitoring system at or above a minimum severity.

        Args:
            min_severity (str, optional): The minimum severity to fetch ('INFO', 'WARNING', 'CRITICAL'). Defaults to 'WARNING'.

        Returns:
            list[dict]: A list of active alert dictionaries.
        """
        severity_map = {"INFO": 1, "WARNING": 2, "CRITICAL": 3}
        min_level = severity_map.get(min_severity.upper(), 2)
        
        try:
            with open(config.ALERTS_FILE, "r") as f:
                all_alerts = json.load(f)
            
            filtered_alerts = [
                alert for alert in all_alerts 
                if severity_map.get(alert.get("severity", "INFO").upper(), 1) >= min_level
            ]
            return filtered_alerts
        except FileNotFoundError:
            logging.error("Alerts data file not found.")
            return [{"error": "Alerts data file not found."}]
        except Exception as e:
            logging.error(f"An error occurred while fetching alerts: {e}")
            return [{"error": f"An error occurred: {str(e)}"}]