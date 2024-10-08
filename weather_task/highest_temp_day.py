#Task: Find the day with highest temperature
import pandas as pd
from data_utils import *

# Initialize argument parser and load dataset
args = initialize_args()
df = load_dataset(args.input_file)

# Filter by date range
start_date = pd.to_datetime(args.start_date)
end_date = pd.to_datetime(args.end_date)
df_filtered = df[(df['Date.Full'] >= start_date) & (df['Date.Full'] <= end_date)]

# Find the day with the highest temperature
highest_temp_row = df_filtered.loc[df_filtered['Data.Temperature.Max Temp'].idxmax()]

# Extract information
highest_temp_date = highest_temp_row['Date.Full']
highest_temp_value = highest_temp_row['Data.Temperature.Max Temp']
highest_temp_city = highest_temp_row['Station.City']
highest_temp_state = highest_temp_row['Station.State']

# Prepare data for exporting
output_data = pd.DataFrame({
    'Date': [highest_temp_date.date()],
    'MaxTemperature': [highest_temp_value],
    'City': [highest_temp_city],
    'State': [highest_temp_state]
})

# Export the results to a CSV file
output_data.to_csv(args.output_file, index=False)

# Print a success message
print(f"Results exported to {args.output_file}")
