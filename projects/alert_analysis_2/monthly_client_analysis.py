import pandas as pd

# Configuration
input_file = "client_events.csv"
output_file = "monthly_client_analysis.csv"

# Read data from CSV
def read_data(file_name):
    return pd.read_csv(file_name)

# Process data for monthly analysis
def process_data(data):
    # Convert logged_date to datetime
    data['logged_date'] = pd.to_datetime(data['logged_date'])

    # Extract month and year for grouping
    data['year_month'] = data['logged_date'].dt.to_period('M')

    # Pivot table to count occurrences per client per month
    monthly_data = data.pivot_table(index='year_month', columns='client', aggfunc='size', fill_value=0)

    # Reset index for better readability
    monthly_data.reset_index(inplace=True)
    monthly_data['year_month'] = monthly_data['year_month'].astype(str)  # Convert Period to string for output

    # Rename columns for clarity
    monthly_data.rename(columns={'year_month': 'month'}, inplace=True)

    # Rearrange data to interleave same months from different years
    monthly_data['month_order'] = pd.to_datetime(monthly_data['month']).dt.month
    monthly_data['year'] = pd.to_datetime(monthly_data['month']).dt.year
    monthly_data.sort_values(by=['month_order', 'year'], inplace=True)
    monthly_data.drop(columns=['month_order', 'year'], inplace=True)

    return monthly_data

# Write processed data to CSV
def write_data(file_name, data):
    data.to_csv(file_name, index=False)

# Main script execution
if __name__ == "__main__":
    # Read the data
    data = read_data(input_file)

    # Process the data
    monthly_analysis = process_data(data)

    # Write the result to CSV
    write_data(output_file, monthly_analysis)

    print(f"Monthly client analysis successfully written to {output_file}")
