#Task: Find the year with lowest temperature average
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

# Extract the year from the date
df_filtered.loc[:, 'Year'] = df_filtered['Date.Full'].dt.year

# Calculate the average temperature for each year
yearly_avg_temp = df_filtered.groupby('Year')['Data.Temperature.Avg Temp'].mean().reset_index()

# Find the year with the lowest average temperature
lowest_avg_temp_row = yearly_avg_temp.loc[yearly_avg_temp['Data.Temperature.Avg Temp'].idxmin()]

# Extract the year and its average temperature
lowest_avg_temp_year = lowest_avg_temp_row['Year']
lowest_avg_temp_value = lowest_avg_temp_row['Data.Temperature.Avg Temp']

# Print the result
print(f"Year with lowest average temperature: {lowest_avg_temp_year} with an average temperature of {lowest_avg_temp_value:.2f}°C")

# Prepare data for exporting
output_data = pd.DataFrame({
    'Year': [lowest_avg_temp_year],
    'AverageTemperature': [lowest_avg_temp_value]
})

# Export the results to a CSV file
output_data.to_csv(args.output_file, index=False)

# Print a success message
print(f"Results exported to {args.output_file}")

