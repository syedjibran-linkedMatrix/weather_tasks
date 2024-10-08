# Task: Find average temperature and wind data, and export to CSV
import pandas as pd
from data_utils import *

# Initialize argument parser and load dataset
args = initialize_args()
df = load_dataset(args.input_file)


# Filter by date range
start_date = pd.to_datetime(args.start_date)
end_date = pd.to_datetime(args.end_date)
df_filtered = df[(df['Date.Full'] >= start_date) & (df['Date.Full'] <= end_date)]

# Function to find average (max & min) temperature, wind direction, and speed
def find_averages(df):
    avg_max_temp = df['Data.Temperature.Max Temp'].mean()
    avg_min_temp = df['Data.Temperature.Min Temp'].mean()
    avg_wind_dir = df['Data.Wind.Direction'].mean()
    avg_wind_speed = df['Data.Wind.Speed'].mean()
    
    return avg_max_temp, avg_min_temp, avg_wind_dir, avg_wind_speed

avg_max_temp, avg_min_temp, avg_wind_dir, avg_wind_speed = find_averages(df_filtered)

# Export the results to a CSV file
avg_data = pd.DataFrame({
    'Average Maximum Temperature': [avg_max_temp],
    'Average Minimum Temperature': [avg_min_temp],
    'Average Wind Direction': [avg_wind_dir],
    'Average Wind Speed': [avg_wind_speed]
})
avg_data.to_csv(args.output_file, index=False)

