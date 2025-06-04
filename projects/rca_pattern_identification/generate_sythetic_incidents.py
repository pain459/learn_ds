import random
import uuid
from datetime import datetime, timedelta
import pandas as pd

# Sample domains
apps = [f"App{i}" for i in range(1, 31)]
clients = [f"Client{i}" for i in range(1, 11)]
teams = [f"Team{i}" for i in range(1, 16)]
categories = ["Infra", "Application", "Integration", "Network", "Security"]
incident_types = [
    "Storage Failure", "Misconfiguration", "Session Handling Error",
    "Third-party API Change", "Deployment Issue", "Code Regression",
    "Memory Leak", "DNS Failure", "Cache Inconsistency", "Timeout Error"
]
rca_templates = [
    "Database node crashed due to {} in {}.",
    "Deployment caused {} in {}.",
    "Service {} faced {} during operation.",
    "{} configuration led to {} errors.",
    "Intermittent issue caused by {} in {} layer.",
    "{} threshold exceeded in {}.",
    "{} failure impacted multiple clients in {} module.",
]

# Generate synthetic incidents
incidents = []
start_date = datetime(2025, 1, 1)

for _ in range(100):
    incident = {
        "incident_id": str(uuid.uuid4()),
        "date_reported": (start_date + timedelta(days=random.randint(0, 150),
                                                  hours=random.randint(0, 23),
                                                  minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S"),
        "app_name": random.choice(apps),
        "client_name": random.choice(clients),
        "impacted_clients": ", ".join(random.sample(clients, random.randint(1, 4))),
        "reported_by": "client",
        "ttd": random.randint(1, 60),
        "ttk": random.randint(1, 30),
        "ttm": random.randint(5, 90),
        "ttc": random.randint(30, 300),
        "rca_summary": random.choice(rca_templates).format(
            random.choice(["high I/O", "bad config", "latency spikes", "missing patch", "cache eviction", "network timeout"]),
            random.choice(["database", "API gateway", "frontend", "backend", "auth layer", "reporting module"])
        ),
        "rca_tags": ", ".join(random.sample(["DB", "Cache", "Network", "Latency", "Config", "API", "OAuth", "Disk", "Session"], 3)),
        "team_owning": random.choice(teams),
        "severity": random.choice([0, 1, 2, 3]),
        "category": random.choice(categories),
        "incident_type": random.choice(incident_types)
    }
    incidents.append(incident)

# Convert to DataFrame
df = pd.DataFrame(incidents)

# Save to CSV
output_path = "synthetic_incident_rca_dataset.csv"
df.to_csv(output_path, index=False)

print(f"Synthetic RCA data saved to: {output_path}")
