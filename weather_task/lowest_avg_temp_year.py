# Task: Find the year with the lowest temperature average
import pandas as pd
from ArgParser_class import ArgParser

class LowestTemperatureAverageFinder:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.output_file = output_file
        self.df = pd.read_csv(input_file)

    def filter_data(self):
        # Convert date column to datetime
        self.df['Date.Full'] = pd.to_datetime(self.df['Date.Full'])

        # Filter by date range
        self.df_filtered = self.df[(self.df['Date.Full'] >= self.start_date) & (self.df['Date.Full'] <= self.end_date)]

        # Extract the year from the date
        self.df_filtered['Year'] = self.df_filtered['Date.Full'].dt.year

    def calculate_lowest_average_temperature(self):
        # Calculate average temperature for each year
        yearly_temperatures = {}
        for _, row in self.df_filtered.iterrows():
            year = row['Year']
            temp = row['Data.Temperature.Avg Temp']
            if year in yearly_temperatures:
                yearly_temperatures[year].append(temp)
            else:
                yearly_temperatures[year] = [temp]

        # Calculate the average temperature for each year and find the lowest average
        lowest_avg_temp_year = None
        lowest_avg_temp_value = float('inf')

        for year, temps in yearly_temperatures.items():
            avg_temp = sum(temps) / len(temps)  # Calculate average temperature
            if avg_temp < lowest_avg_temp_value:
                lowest_avg_temp_value = avg_temp
                lowest_avg_temp_year = year

        return lowest_avg_temp_year, lowest_avg_temp_value

    def export_results(self, year, avg_temp):
        # Prepare data for exporting
        with open(self.output_file, 'w') as file:
            # Write the header
            file.write('Year,LowestAverageTemperature\n')
            # Write the data
            file.write(f"{year},{avg_temp:}\n")

    def analyze(self):
        self.filter_data()
        lowest_avg_temp_year, lowest_avg_temp_value = self.calculate_lowest_average_temperature()
        
        if lowest_avg_temp_year is not None:
            self.export_results(lowest_avg_temp_year, lowest_avg_temp_value)
            print(f"Year with lowest average temperature: {lowest_avg_temp_year} with an average temperature of {lowest_avg_temp_value:.2f}°C")
            print(f"Results exported to {self.output_file}")
        else:
            print("No data found in the specified date range.")

if __name__ == "__main__":
    # Initialize argument parser
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of LowestTemperatureAverageFinder
    temp_finder = LowestTemperatureAverageFinder(args.input_file, args.start_date, args.end_date, args.output_file)
    
    # Run the analysis
    temp_finder.analyze()
