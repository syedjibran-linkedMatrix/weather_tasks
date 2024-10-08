# Task: Find the state with maximum temperature, maximum wind speed, minimum temperature, and minimum wind speed
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


# 1. Find the row with the maximum temperature
max_temp_row = df_filtered.loc[df_filtered['Data.Temperature.Max Temp'].idxmax()]

# 2. Find the row with the maximum wind speed
max_wind_speed_row = df_filtered.loc[df_filtered['Data.Wind.Speed'].idxmax()]

# 3. Find the row with the minimum temperature
min_temp_row = df_filtered.loc[df_filtered['Data.Temperature.Min Temp'].idxmin()]

# 4. Find the row with the minimum wind speed
min_wind_speed_row = df_filtered.loc[df_filtered['Data.Wind.Speed'].idxmin()]

# Extract the required information (city, location, code, state)
data = {
    'Category': ['Max Temperature', 'Max Wind Speed', 'Min Temperature', 'Min Wind Speed'],
    'City': [max_temp_row['Station.City'], max_wind_speed_row['Station.City'], min_temp_row['Station.City'], min_wind_speed_row['Station.City']],
    'Location': [max_temp_row['Station.Location'], max_wind_speed_row['Station.Location'], min_temp_row['Station.Location'], min_wind_speed_row['Station.Location']],
    'Code': [max_temp_row['Station.Code'], max_wind_speed_row['Station.Code'], min_temp_row['Station.Code'], min_wind_speed_row['Station.Code']],
    'State': [max_temp_row['Station.State'], max_wind_speed_row['Station.State'], min_temp_row['Station.State'], min_wind_speed_row['Station.State']]
}

# Create a DataFrame with the extracted information
output_data = pd.DataFrame(data)

# Export the results to a CSV file
output_data.to_csv(args.output_file, index=False)

# Print a success message
print(f"Results exported to {args.output_file}")
