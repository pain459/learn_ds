import random
import datetime
import csv

# -----------------------------------------------------------
# Configuration
# -----------------------------------------------------------
START_INCIDENT_ID = 2025011000

# Number of incidents per weekday (Mon=1, Tue=2, ..., Sun=7)
INCIDENTS_PER_DAY = {
    1: 10,  # Monday
    2: 9,   # Tuesday
    3: 8,   # Wednesday
    4: 7,   # Thursday
    5: 6,   # Friday
    6: 5,   # Saturday
    7: 4    # Sunday
}

# Departments (1–10), Issue types (1–6), Clients (1–10)
DEPARTMENTS = list(range(1, 11))
ISSUE_TYPES = list(range(1, 7))
CLIENTS = list(range(1, 11))

# We define weeks in January 2025 as:
# Week 1: Jan 1–5
# Week 2: Jan 6–12
# Week 3: Jan 13–19
# Week 4: Jan 20–26
# Week 5: Jan 27–31
def get_week_number(day_of_month):
    if 1 <= day_of_month <= 5:
        return 1
    elif 6 <= day_of_month <= 12:
        return 2
    elif 13 <= day_of_month <= 19:
        return 3
    elif 20 <= day_of_month <= 26:
        return 4
    else:
        return 5

# -----------------------------------------------------------
# Generate data
# -----------------------------------------------------------
def generate_january_incidents():
    """
    Generate incident rows for January 2025 based on the rules:
     - day_in_week: Monday=1, ..., Sunday=7
     - random times between 08:00 and (say) 18:00 for first_symptom
     - random offsets for create, detect, mitigate, close
     - various random picks for department, issue_type, impacted_clients
    """
    current_incident_id = START_INCIDENT_ID
    # Start date: 2025-01-01
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 1, 31)

    delta = datetime.timedelta(days=1)

    all_rows = []

    # We'll iterate from Jan 1 to Jan 31
    d = start_date
    while d <= end_date:
        # Determine day_in_week (Monday=1, Sunday=7)
        day_of_week = (d.isoweekday() % 7) or 7  # isoweekday() gives Mon=1..Sun=7
        # Number of incidents for this day:
        num_incidents = INCIDENTS_PER_DAY[day_of_week]

        # For each incident of the day:
        for _ in range(num_incidents):
            # Randomly pick a base start time between 08:00 and 14:00 for the first symptom
            hour_fs = random.randint(8, 14)
            minute_fs = random.randint(0, 59)
            # Construct datetime for first symptom
            fs_dt = datetime.datetime(d.year, d.month, d.day, hour_fs, minute_fs)

            # We'll create offsets (in minutes) for subsequent events
            # ensure they are increasing
            create_offset = random.randint(5, 30)     # after first_symptom
            detect_offset = random.randint(create_offset + 5, create_offset + 45)
            mitigate_offset = random.randint(detect_offset + 10, detect_offset + 60)
            close_offset = random.randint(mitigate_offset + 30, mitigate_offset + 120)

            # Now build actual datetimes
            create_dt = fs_dt + datetime.timedelta(minutes=create_offset)
            detect_dt = fs_dt + datetime.timedelta(minutes=detect_offset)
            mitigate_dt = fs_dt + datetime.timedelta(minutes=mitigate_offset)
            close_dt = fs_dt + datetime.timedelta(minutes=close_offset)

            # Calculate derived differences
            time_to_create_minutes = (create_dt - fs_dt).total_seconds() / 60
            time_to_detect_minutes = (detect_dt - fs_dt).total_seconds() / 60
            time_to_closure_minutes = (close_dt - fs_dt).total_seconds() / 60

            # Random picks
            department = random.choice(DEPARTMENTS)
            issue_type = random.choice(ISSUE_TYPES)
            impacted_client = random.choice(CLIENTS)

            # Week number
            week_number = get_week_number(d.day)

            # Build a row (as a dict for clarity)
            row = {
                "incident_id": current_incident_id,
                "time_to_first_symptom": fs_dt.strftime("%Y-%m-%d %H:%M"),
                "time_to_create": create_dt.strftime("%Y-%m-%d %H:%M"),
                "time_to_detect": detect_dt.strftime("%Y-%m-%d %H:%M"),
                "time_to_mitigate": mitigate_dt.strftime("%Y-%m-%d %H:%M"),
                "time_to_close": close_dt.strftime("%Y-%m-%d %H:%M"),
                "department": department,
                "issue_type": issue_type,
                "time_to_create_minutes": int(time_to_create_minutes),
                "time_to_detect_minutes": int(time_to_detect_minutes),
                "time_to_closure_minutes": int(time_to_closure_minutes),
                "week_number": week_number,
                "day_in_week": day_of_week,
                "quarter_of_year": 1,  # January -> Q1
                "month_of_year": 1,    # January
                "impacted_clients": impacted_client
            }
            all_rows.append(row)

            current_incident_id += 1  # increment for next incident

        d += delta

    return all_rows

# -----------------------------------------------------------
# Main Execution: Generate and print CSV
# -----------------------------------------------------------
if __name__ == "__main__":
    data = generate_january_incidents()

    # Define CSV header in the desired order
    fieldnames = [
        "incident_id",
        "time_to_first_symptom",
        "time_to_create",
        "time_to_detect",
        "time_to_mitigate",
        "time_to_close",
        "department",
        "issue_type",
        "time_to_create_minutes",
        "time_to_detect_minutes",
        "time_to_closure_minutes",
        "week_number",
        "day_in_week",
        "quarter_of_year",
        "month_of_year",
        "impacted_clients"
    ]

    # Print CSV to stdout (you can redirect to a file, e.g. > january_incidents.csv)
    writer = csv.DictWriter(open("january_incidents.csv", "w", newline=''), fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    print(f"CSV generated with {len(data)} incidents.")
