import pandas as pd
import random
from datetime import datetime, timedelta

# Initialize the date range for November 2024
start_date = datetime(2024, 11, 1)
end_date = datetime(2024, 11, 30)

# Generate a list of dates
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Define clients
clients = [f"c{i}" for i in range(1, 8)]

# Function to generate a row of data
def generate_data(date, client):
    triggers = random.randint(1, 3)
    retriggers = random.randint(0, 20)
    notifications = triggers + retriggers
    
    # Distribute triggers and retriggers across components
    remaining = triggers + retriggers
    component1 = random.randint(0, remaining)
    remaining -= component1
    component2 = random.randint(0, remaining)
    component3 = remaining - component2
    
    return {
        "date": date.strftime("%Y%m%d"),
        "client": client,
        "triggers": triggers,
        "retriggers": retriggers,
        "notifications": notifications,
        "component1": component1,
        "component2": component2,
        "component3": component3,
    }

# Generate the dataset
data = []
for date in date_list:
    for client in clients:
        data.append(generate_data(date, client))

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
output_file = "november_2024_data.csv"
df.to_csv(output_file, index=False)


