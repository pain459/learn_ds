import csv
import random
from datetime import datetime, timedelta

# Specifications
tickets = 10000  # Number of tickets to generate
clients = ["A", "B", "C", "D", "E"]
services = ["A1", "B1", "C1", "D1", "E1", "F1"]
statuses = ["assigned", "awaiting_response", "closed"]
assignees = ["member1", "member2", "member3", "member4"]
loggers = ["user1", "user2", "user3", "user4"]

# Start ticket ID
ticket_id_start = 1000

# Generate current datetime
def generate_datetime():
    start_date = datetime(2024, 1, 1, 0, 0)
    random_minutes = random.randint(0, 60 * 24 * 300)  # Random within 30 days
    return start_date + timedelta(minutes=random_minutes)

# Generate ticket data
def generate_tickets(ticket_count):
    data = []
    for i in range(ticket_count):
        ticket = {
            "ticket_id": ticket_id_start + i,
            "client": random.choice(clients),
            "service": random.choice(services),
            "logged_date": generate_datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "status": random.choice(statuses),
            "time_spent": random.randint(1, 8),  # Time spent in hours
            "assignee": random.choice(assignees),
            "logger": random.choice(loggers),
        }
        data.append(ticket)
    return data

# Write to CSV
def write_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Main
if __name__ == "__main__":
    ticket_data = generate_tickets(tickets)
    output_file = "tickets.csv"
    write_to_csv(output_file, ticket_data)
    print(f"CSV file '{output_file}' generated successfully with {tickets} tickets.")
