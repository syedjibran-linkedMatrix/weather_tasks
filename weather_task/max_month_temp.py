#Task: Find the month with highest temperature average
import pandas as pd
from ArgParser_class import ArgParser

# Initialize argument parser
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

# Extract the month from the date
df_filtered['Month'] = df_filtered['Date.Full'].dt.month
df_filtered['Year'] = df_filtered['Date.Full'].dt.year

# Calculate the average temperature for each month
monthly_avg_temp = df_filtered.groupby(['Year', 'Month'])['Data.Temperature.Avg Temp'].mean().reset_index()

# Find the month with the highest average temperature
highest_avg_temp_row = monthly_avg_temp.loc[monthly_avg_temp['Data.Temperature.Avg Temp'].idxmax()]

# Extract the month and its average temperature
highest_avg_temp_month = highest_avg_temp_row['Month']
highest_avg_temp_value = highest_avg_temp_row['Data.Temperature.Avg Temp']

# Print the result
print(f"Month with highest average temperature: Month {highest_avg_temp_month} with an average temperature of {highest_avg_temp_value:.2f}°C")

# Prepare data for exporting
output_data = pd.DataFrame({
    'Month': [highest_avg_temp_month],
    'AverageTemperature': [highest_avg_temp_value]
})

# Export the results to a CSV file
output_data.to_csv(args.output_file, index=False)

# Print a success message
print(f"Results exported to {args.output_file}")
