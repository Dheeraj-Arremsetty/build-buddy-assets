# tools/rca_tools.py
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def query_elasticsearch_logs(hostname: str, time_window_minutes: int = 15) -> str:
    """
    Queries ElasticSearch for logs related to a specific hostname within a given time window.

    This tool simulates a search against an ElasticSearch cluster to retrieve relevant log entries
    preceding and during an incident. Access to log data is fundamental for root cause analysis,
    allowing the RCA agent to identify error messages, stack traces, and anomalous activity
    that could indicate the source of the problem.

    Args:
        hostname (str): The hostname to filter logs by (e.g., "prod-db-01").
        time_window_minutes (int): The number of minutes to look back for logs. Defaults to 15.

    Returns:
        str: A JSON string containing a list of relevant log entries.
    """
    print(f"Querying ElasticSearch for logs from '{hostname}' in the last {time_window_minutes} minutes.")
    incident_time = datetime.utcnow()
    logs = [
        {"timestamp": (incident_time - timedelta(minutes=2, seconds=2)).isoformat() + "Z", "level": "ERROR", "host": "prod-db-01", "service": "Oracle Listener", "message": "TNS-12541: TNS:no listener"},
        {"timestamp": (incident_time - timedelta(minutes=1, seconds=30)).isoformat() + "Z", "level": "INFO", "host": "prod-db-01", "service": "HealthCheck", "message": "Listener health check failed."},
        {"timestamp": (incident_time - timedelta(seconds=59)).isoformat() + "Z", "level": "ERROR", "host": "prod-app-01", "service": "BillingService", "message": "Database connection pool exhausted."},
        {"timestamp": (incident_time - timedelta(seconds=2)).isoformat() + "Z", "level": "FATAL", "host": "prod-app-01", "service": "BillingService", "message": "Cannot connect to database: ORA-12541"},
        {"timestamp": (incident_time).isoformat() + "Z", "level": "CRITICAL", "host": "prod-db-01", "service": "Oracle DB Listener", "message": "Service is down"},
    ]
    return json.dumps(logs)

@tool(permission=ToolPermission.ADMIN)
def get_logicmonitor_metrics(hostname: str, metric: str = "cpu_utilization") -> str:
    """
    Retrieves performance metrics for a specific host from LogicMonitor.

    This tool simulates a request to a monitoring platform like LogicMonitor to fetch key
    performance indicators (KPIs) such as CPU utilization, memory usage, or network I/O.
    Correlating performance metrics with log data helps the RCA agent build a more complete
    picture of the system's state and pinpoint performance bottlenecks or resource exhaustion
    as potential root causes.

    Args:
        hostname (str): The hostname to retrieve metrics for (e.g., "prod-db-01").
        metric (str): The specific metric to retrieve. Defaults to "cpu_utilization".

    Returns:
        str: A JSON string containing time-series data for the requested metric.
    """
    print(f"Retrieving LogicMonitor metric '{metric}' for host '{hostname}'.")
    now = datetime.utcnow()
    metrics_data = {
        "hostname": hostname,
        "metric": metric,
        "data_points": [
            {"timestamp": (now - timedelta(minutes=10)).isoformat() + "Z", "value": random.uniform(10.5, 15.0)},
            {"timestamp": (now - timedelta(minutes=5)).isoformat() + "Z", "value": random.uniform(12.0, 18.0)},
            {"timestamp": (now - timedelta(minutes=2)).isoformat() + "Z", "value": 98.7},
            {"timestamp": (now - timedelta(minutes=1)).isoformat() + "Z", "value": 99.1},
        ]
    }
    return json.dumps(metrics_data)