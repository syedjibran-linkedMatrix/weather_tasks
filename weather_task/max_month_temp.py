#Task: Find the month with highest temperature average
import csv
from datetime import datetime
from ArgParser_class import ArgParser
from collections import defaultdict

class MonthlyTemperatureAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.output_file = output_file

    def read_filtered_data(self):
        """Read the CSV file and yield rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read data in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            yield row
                    except ValueError as e:
                        print(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.")
            return

    def calculate_monthly_avg_temp(self):
        """Calculate the average temperature for each month."""
        monthly_data = defaultdict(list)

        for row in self.read_filtered_data():
            try:
                date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                month = date.month #extract month from date
                year = date.year   #extract year from date
                avg_temp = float(row['Data.Temperature.Avg Temp'])

                # Store temperature data indexed by year and month
                monthly_data[(year, month)].append(avg_temp) # monthly_data becomes: {(2016, 1): [39]}
            except ValueError as e:
                print(f"Skipping row due to data conversion error: {e}")

        # Calculate the average temperature for each month
        monthly_avg_temp = {}  #this will contain contain average temperatures of each month i.e monthly_avg_temp = {(2016, 1): 6.0,(2016, 2): 11.0,(2016, 3): 14.0,}
        for (year, month), temps in monthly_data.items():
            monthly_avg_temp[(year, month)] = sum(temps) / len(temps)

        return monthly_avg_temp

    def find_highest_avg_temp(self, monthly_avg_temp):
        """Find the month with the highest average temperature."""
        highest_avg_temp = float('-inf')
        highest_month = None

        for (year, month), avg_temp in monthly_avg_temp.items():
            if avg_temp > highest_avg_temp:
                highest_avg_temp = avg_temp
                highest_month = (year, month)

        return highest_month, highest_avg_temp #((year, month), highestAvgTemp)

    def export_to_csv(self, month, avg_temp):
        """Export the month and its average temperature to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Month', 'AverageTemperature'])  # Header
                writer.writerow([month[1], avg_temp])  # Month number and average temperature

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        monthly_avg_temp = self.calculate_monthly_avg_temp()
        highest_month, highest_avg_temp_value = self.find_highest_avg_temp(monthly_avg_temp)

        if highest_month:
            print(f"Month with highest average temperature: Month {highest_month[1]} "
                  f"of year {highest_month[0]} with an average temperature of {highest_avg_temp_value:.2f}°C")

            self.export_to_csv(highest_month, highest_avg_temp_value)
        else:
            print("No data available for the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of MonthlyTemperatureAnalyzer
    analyzer = MonthlyTemperatureAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
