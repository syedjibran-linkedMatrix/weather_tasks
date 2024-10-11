# Task: Find the day with highest temperature
import pandas as pd
from ArgParser_class import ArgParser

class HighestTemperatureFinder:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.output_file = output_file
        self.df = pd.read_csv(input_file)

    def filter_data(self):
        # Convert the date column to datetime format
        self.df['Date.Full'] = pd.to_datetime(self.df['Date.Full'])
        # Filter the dataset by the date range
        self.df_filtered = self.df[(self.df['Date.Full'] >= self.start_date) & (self.df['Date.Full'] <= self.end_date)]

    def find_highest_temperature(self):
        # Initialize variables to keep track of the highest temperature and corresponding row
        max_temp = float('-inf')
        highest_temp_info = {}

        # Iterate through the rows manually
        for _, row in self.df_filtered.iterrows():
            current_temp = row['Data.Temperature.Max Temp']
            
            # Check if the current row has a higher maximum temperature
            if current_temp > max_temp:
                max_temp = current_temp
                highest_temp_info = {
                    'Date': row['Date.Full'].date(),
                    'MaxTemperature': row['Data.Temperature.Max Temp'],
                    'City': row['Station.City'],
                    'State': row['Station.State']
                }

        # If no rows are found, return None
        if not highest_temp_info:
            return None

        return highest_temp_info

    def export_to_csv(self, highest_temp_info):
        # Prepare data for export
        with open(self.output_file, 'w') as file:
            # Write the header
            file.write('Date,MaxTemperature,City,State\n')
            # Write the data
            file.write(f"{highest_temp_info['Date']},{highest_temp_info['MaxTemperature']},{highest_temp_info['City']},{highest_temp_info['State']}\n")

    def analyze(self):
        self.filter_data()
        highest_temp_info = self.find_highest_temperature()

        if highest_temp_info:
            self.export_to_csv(highest_temp_info)
            # Print results
            print(f"Result is: {highest_temp_info}")
            print(f"Results exported to {self.output_file}")
        else:
            print("No data found in the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    # Create an instance of HighestTemperatureFinder
    temp_finder = HighestTemperatureFinder(args.input_file, args.start_date, args.end_date, args.output_file)
    # Run the analysis
    temp_finder.analyze()
