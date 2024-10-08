# Task: Find the state with maximum occurrences
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

state_counts = df_filtered['Station.State'].value_counts()
most_common_state = state_counts.idxmax()  # Get the state with the most occurrences
max_occurrences = state_counts.max()  # Get the number of occurrences

# Print the result
print(f"State with maximum occurrences: {most_common_state}")
print(f"Number of occurrences: {max_occurrences}")

# Export the result to a CSV file
output_data = pd.DataFrame({
    'State': [most_common_state],
    'Occurrences': [max_occurrences]
})

output_data.to_csv(args.output_file, index=False)
print(f"Results exported to {args.output_file}")
