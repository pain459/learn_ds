import csv
import random
from datetime import datetime, timedelta

# Configuration
clients = [f"c{i}" for i in range(1, 9)]  # Clients c1 to c8
start_date = datetime(2023, 1, 1, 0, 0, 0)  # Start date
end_date = datetime(2024, 12, 31, 23, 59, 0)  # End date
output_file = "client_events.csv"

# Generate random events
def generate_random_events(start_date, end_date, clients):
    current_date = start_date
    events = []

    while current_date <= end_date:
        # Randomize the number of events for the day (1 to 10 events)
        num_events = random.randint(1, 10)

        for _ in range(num_events):
            # Randomize event time within the day
            event_time = current_date + timedelta(
                hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59)
            )
            if event_time > end_date:
                break

            # Randomize the client
            client = random.choice(clients)
            events.append([event_time.strftime("%Y-%m-%d %H:%M:%S"), client])

        # Move to the next day
        current_date += timedelta(days=1)

    return events

# Write to CSV
def write_to_csv(file_name, events):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["logged_date", "client"])
        writer.writerows(events)

# Main script execution
if __name__ == "__main__":
    random_events = generate_random_events(start_date, end_date, clients)
    write_to_csv(output_file, random_events)
    print(f"Data successfully generated and written to {output_file}")
