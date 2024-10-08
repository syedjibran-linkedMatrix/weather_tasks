# Task: Find maximum temperature and its corresponding location and state
import pandas as pd
from ArgParser_class import ArgParser

args_parser = ArgParser()
args = args_parser.parse_args()

# Load the dataset
df = pd.read_csv(args.input_file)

# Convert date column to datetime
df['Date.Full'] = pd.to_datetime(df['Date.Full'])

# Filter by date range
start_date = pd.to_datetime(args.start_date)
end_date = pd.to_datetime(args.end_date)
df_filtered = df[(df['Date.Full'] >= start_date) & (df['Date.Full'] <= end_date)]

max_temp_row = df_filtered.loc[df_filtered['Data.Temperature.Max Temp'].idxmax()]

# Extract the maximum temperature, location, and state
max_temp = max_temp_row['Data.Temperature.Max Temp']
location = max_temp_row['Station.Location']
state = max_temp_row['Station.State']

#print the results on the console
print(f"Maximum Temperature: {max_temp}°C")
print(f"Location: {location}")
print(f"State: {state}")

# Export the results to a CSV file
output_data = pd.DataFrame({
    'MaxTemperature': [max_temp],
    'Location': [location],
    'State': [state]
})

output_data.to_csv(args.output_file, index=False)
print(f"Results exported to {args.output_file}")
