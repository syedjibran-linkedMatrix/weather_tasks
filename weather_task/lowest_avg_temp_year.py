# Task: Find the year with lowest temperature average
import csv
from datetime import datetime
from collections import defaultdict
from ArgParser_class import ArgParser

class LowestTemperatureAverageFinder:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.output_file = output_file

    def read_filtered_data(self):
        """Read the CSV file and yield rows within the date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile) # Read CSV in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            yield date.year, float(row['Data.Temperature.Avg Temp'])
                    except ValueError as e:
                        print(f"Skipping row due to error: {e}")
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.")
            return  # Return an empty generator if the file is not found

    def calculate_lowest_average_temperature(self):
        """Calculate the year with the lowest average temperature."""
        
        #If year doesn’t exist, it automatically initializes yearly_temperatures[year] to an empty list before appending.
        yearly_temperatures = defaultdict(list)  #defaultdict will hold list of temperatures for each year

        # Collect temperatures by year
        for year, temp in self.read_filtered_data():
            yearly_temperatures[year].append(temp) #appends the temperature to the corresponding year in yearly_temperatures dict

        # Find the year with the lowest average temperature
        lowest_avg_temp_year = None
        lowest_avg_temp_value = float('inf')

        for year, temps in yearly_temperatures.items():
            avg_temp = sum(temps) / len(temps)  # Calculate average temperature
            if avg_temp < lowest_avg_temp_value:
                lowest_avg_temp_value = avg_temp
                lowest_avg_temp_year = year

        return lowest_avg_temp_year, lowest_avg_temp_value

    def export_results(self, year, avg_temp):
        """Export the results to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Year', 'LowestAverageTemperature'])  # Write header
                writer.writerow([year, f"{avg_temp:.2f}"])  # Write data

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export results."""
        year, avg_temp = self.calculate_lowest_average_temperature()

        if year is not None:
            print(f"Year with lowest average temperature: {year} with an average temperature of {avg_temp:.2f}°C")
            self.export_results(year, avg_temp)
        else:
            print("No data found in the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of LowestTemperatureAverageFinder
    temp_finder = LowestTemperatureAverageFinder(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    temp_finder.analyze()
