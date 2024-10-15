# Task: Find the year with lowest temperature average
import csv
import logging
from datetime import datetime
from collections import defaultdict
from ArgParser_class import ArgParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LowestTemperatureAverageFinder:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.filtered_data = defaultdict(list)  # Store temperatures by year

    def read_filtered_data(self):
        """Read the CSV file and store filtered rows with relevant data."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read CSV in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
                        continue  # Skip if date parsing fails

                    if self.start_date <= date <= self.end_date:
                        try:
                            # Store only relevant fields
                            data = {
                                'year': date.year,
                                'avg_temp': float(row.get('Data.Temperature.Avg Temp', 0.0) or 0.0)
                            }
                            self.filtered_data[data['year']].append(data['avg_temp'])
                        except (TypeError, ValueError) as e:
                            logging.warning(f"Skipping row due to data conversion error: {e}")

            logging.info(f"Finished reading data with temperatures from {len(self.filtered_data)} years.")

        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def calculate_lowest_average_temperature(self):
        """Find the year with the lowest average temperature."""
        lowest_avg_temp_year = None
        lowest_avg_temp_value = float('inf')

        for year, temps in self.filtered_data.items():
            avg_temp = sum(temps) / len(temps)  # Calculate average temperature
            if avg_temp < lowest_avg_temp_value:
                lowest_avg_temp_value = avg_temp
                lowest_avg_temp_year = year

        if lowest_avg_temp_year is not None:
            logging.info(f"Year with lowest average temperature: {lowest_avg_temp_year} ({lowest_avg_temp_value:.2f}°C)")
        else:
            logging.warning("No valid data found for the given date range.")

        return lowest_avg_temp_year, lowest_avg_temp_value

    def export_results(self, year, avg_temp):
        """Export the results to a CSV file."""
        if year is None:
            logging.error("No data to export.")
            return

        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Year', 'LowestAverageTemperature'])  # Write header
                writer.writerow([year, f"{avg_temp:.2f}"])  # Write data

            logging.info(f"Results successfully exported to {self.output_file}")

        except PermissionError:
            logging.error(f"Error: Permission denied for file {self.output_file}.")
        except Exception as e:
            logging.error(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()
        year, avg_temp = self.calculate_lowest_average_temperature()
        self.export_results(year, avg_temp)

if __name__ == "__main__":
    # Parse command-line arguments
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    # Create an instance of LowestTemperatureAverageFinder
    temp_finder = LowestTemperatureAverageFinder(
        args.input_file, args.start_date, args.end_date, args.output_file
    )

    # Run the analysis
    temp_finder.analyze()
