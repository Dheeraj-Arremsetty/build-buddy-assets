import json
        import random
        from datetime import datetime, timedelta
        from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

        @tool(name="get_device_status", permission=ToolPermission.ADMIN)
        def get_device_status(device_name: str) -> str:
            """
            Retrieves the current operational status and key performance metrics for a specific device.

            This tool simulates a call to the LogicMonitor API to get real-time health data, which is essential for immediate diagnostics when a user reports an issue. It provides the foundational data needed to determine if a system is operational or experiencing a fault.

            Args:
                device_name (str): The unique hostname of the device to check (e.g., 'web-prod-01', 'db-cluster-01').

            Returns:
                str: A JSON string containing the device status, CPU load, memory usage, and a timestamp.
            """
            statuses = ["healthy", "warning", "critical"]
            if "web" in device_name:
                status = "critical"
                cpu_load = "98%"
                memory_usage = "92%"
            else:
                status = random.choice(statuses)
                cpu_load = f"{random.randint(20, 85)}%"
                memory_usage = f"{random.randint(40, 90)}%"

            data = {
                "deviceName": device_name,
                "status": status,
                "cpu_load": cpu_load,
                "memory_usage": memory_usage,
                "timestamp": datetime.utcnow().isoformat()
            }
            return json.dumps(data, indent=2)

        @tool(name="check_active_alerts", permission=ToolPermission.ADMIN)
        def check_active_alerts(min_severity: str = "P3") -> str:
            """
            Fetches a list of all active alerts from LogicMonitor that meet a minimum severity level.

            This tool is vital for understanding the broader context of system health. It allows the AIOps agent to correlate a user's reported issue with known system-wide problems, preventing duplicate incident creation and providing immediate awareness of ongoing outages.

            Args:
                min_severity (str, optional): The minimum severity to filter by (e.g., 'P1', 'P2', 'P3'). Defaults to 'P3'.

            Returns:
                str: A JSON string containing a list of active alerts with their severity and description.
            """
            alerts = [
                {"alertId": "LM-ALERT-101", "severity": "P1", "device": "web-prod-01", "description": "High CPU utilization detected", "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()},
                {"alertId": "LM-ALERT-102", "severity": "P2", "device": "api-gateway-01", "description": "Response time degradation", "timestamp": (datetime.utcnow() - timedelta(minutes=25)).isoformat()},
                {"alertId": "LM-ALERT-103", "severity": "P3", "device": "db-cluster-01", "description": "Disk space approaching capacity", "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()},
            ]
            return json.dumps(alerts, indent=2)

        @tool(name="fetch_performance_logs", permission=ToolPermission.ADMIN)
        def fetch_performance_logs(device_name: str) -> str:
            """
            Retrieves the last 100 lines of performance logs for a given device from LogicMonitor.

            Access to raw logs is critical for deep-dive technical analysis. This tool automates the log collection process, ensuring that when an incident ticket is created, it is immediately enriched with the necessary data for engineers to begin root cause analysis, drastically reducing MTTR.

            Args:
                device_name (str): The unique name of the device (e.g., 'web-prod-01').

            Returns:
                str: A formatted string containing the recent performance logs.
            """
            timestamp = datetime.utcnow().isoformat()
            logs = [
                f"{timestamp} [ERROR] High CPU usage detected: 98%. Threshold exceeded.",
                f"{timestamp} [WARN] Memory pressure at 92%.",
                f"{timestamp} [INFO] Request received on /api/v1/login.",
                f"{timestamp} [ERROR] Database connection timeout on pool-3-thread-1.",
            ]
            return f"Logs for {device_name}:\n" + "\n".join(logs)