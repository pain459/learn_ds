import pandas as pd
from faker import Faker
import random

# Initialize faker
fake = Faker()

# Define car data lists based on existing data
makes = ["Toyota", "Honda", "BMW", "Nissan", "Ford"]
colors = ["White", "Red", "Blue", "Black", "Green", "CanyonRidge"]
door_options = [3, 4, 5]
price_ranges = {
    "Toyota": (4000, 8000),
    "Honda": (5000, 9000),
    "BMW": (15000, 30000),
    "Nissan": (3000, 10000),
    "Ford" : (4000, 25000)
}

# Generate synthetic data
def generate_car_data(num_records):
    data = []
    for _ in range(num_records):
        make = random.choice(makes)
        color = random.choice(colors)
        odometer_km = fake.random_int(min=10000, max=250000)
        doors = random.choice(door_options)
        price = random.uniform(*price_ranges[make])
        
        # Format the price with a dollar sign and two decimal points
        formatted_price = f"${price:,.2f}"
        
        data.append([make, color, odometer_km, doors, formatted_price])
        
    return pd.DataFrame(data, columns=["Make", "Colour", "Odometer (KM)", "Doors", "Price"])

# Function to save data to CSV
def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Generate 100 records as an example
car_data = generate_car_data(100000)

# Save to file with the specified filename
filename = "car-sales-custom.csv"  # Replace this with your desired filename
save_to_csv(car_data, filename)
