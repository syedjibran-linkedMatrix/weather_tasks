import csv
import logging
from datetime import datetime
from ArgParser_class import ArgParser
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MonthlyTemperatureAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.filtered_data = []  # Store relevant rows with necessary data

    def read_filtered_data(self):
        """Read the CSV file and store relevant rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read data in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            # Store only relevant fields, filling missing average temperature with 0.0
                            avg_temp = row.get('Data.Temperature.Avg Temp')

                            # Fill missing values with 0.0 and convert to float
                            data = {
                                'date': date,
                                'avg_temp': float(avg_temp) if avg_temp is not None else 0.0
                            }
                            self.filtered_data.append(data)
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def calculate_monthly_avg_temp(self):
        """Calculate the average temperature for each month."""
        monthly_data = defaultdict(list)

        for row in self.filtered_data:
            try:
                month = row['date'].month  # Extract month from date
                year = row['date'].year    # Extract year from date
                avg_temp = row['avg_temp']

                # Store temperature data indexed by year and month
                monthly_data[(year, month)].append(avg_temp)  # Example: {(2016, 1): [39]}
            except Exception as e:
                logging.warning(f"Skipping row due to data error: {e}")

        # Calculate the average temperature for each month
        monthly_avg_temp = {}  # Contains average temperatures for each month
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

        return highest_month, highest_avg_temp  # ((year, month), highestAvgTemp)

    def export_to_csv(self, month, avg_temp):
        """Export the month and its average temperature to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Month', 'AverageTemperature'])  # Header
                writer.writerow([month[1], avg_temp])  # Month number and average temperature

            logging.info(f"Results exported to {self.output_file}")
        except Exception as e:
            logging.error(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()
        monthly_avg_temp = self.calculate_monthly_avg_temp()
        highest_month, highest_avg_temp_value = self.find_highest_avg_temp(monthly_avg_temp)

        if highest_month:
            logging.info(f"Month with highest average temperature: Month {highest_month[1]} "
                         f"of year {highest_month[0]} with an average temperature of {highest_avg_temp_value:.2f}°C")

            self.export_to_csv(highest_month, highest_avg_temp_value)
        else:
            logging.warning("No data available for the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of MonthlyTemperatureAnalyzer
    analyzer = MonthlyTemperatureAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
