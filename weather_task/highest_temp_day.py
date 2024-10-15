# Task: Find the day with highest temperature
import csv
import logging
from datetime import datetime
from ArgParser_class import ArgParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HighestTemperatureFinder:
    def __init__(self, input_file: str, start_date: datetime, end_date: datetime, output_file: str):
        self.input_file = input_file
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.filtered_data = []  # Store filtered data here
        self.highest_temp_info = None

    def read_filtered_data(self):
        """Read the CSV file and store relevant rows with valid data."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
                        continue  # Skip this row if date parsing fails

                    if self.start_date <= date <= self.end_date:
                        try:
                            data = {
                                'date': row['Date.Full'],
                                'max_temp': float(row.get('Data.Temperature.Max Temp', 0.0) or 0.0),
                                'city': row.get('Station.City', 'N/A'),
                                'state': row.get('Station.State', 'N/A')
                            }
                            self.filtered_data.append(data)
                        except (TypeError, ValueError) as e:
                            logging.warning(f"Skipping row due to data conversion error: {e}")

            logging.info(f"Finished reading and storing {len(self.filtered_data)} rows of filtered data.")

        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def find_highest_temperature(self):
        """Identify the highest temperature from the filtered data."""
        max_temp = float('-inf')  # Initialize max_temp to a very low value

        for data in self.filtered_data:
            if data['max_temp'] > max_temp:
                max_temp = data['max_temp']
                self.highest_temp_info = {
                    'Date': data['date'],
                    'MaxTemperature': max_temp,
                    'City': data['city'],
                    'State': data['state']
                }

        if self.highest_temp_info:
            logging.info(f"Highest temperature found: {self.highest_temp_info}")
        else:
            logging.warning("No valid data found in the specified date range.")

    def export_to_csv(self):
        """Export the highest temperature info to a CSV file."""
        if not self.highest_temp_info:
            logging.error("No data available to export.")
            return

        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'MaxTemperature', 'City', 'State'])  # Write header
                writer.writerow([
                    self.highest_temp_info['Date'],
                    self.highest_temp_info['MaxTemperature'],
                    self.highest_temp_info['City'],
                    self.highest_temp_info['State']
                ])  # Write data

            logging.info(f"Results successfully exported to {self.output_file}")

        except PermissionError:
            logging.error(f"Error: Permission denied for file {self.output_file}.")
        except Exception as e:
            logging.error(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()
        self.find_highest_temperature()
        self.export_to_csv()

if __name__ == "__main__":
    # Parse command-line arguments
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    # Create an instance of HighestTemperatureFinder
    temp_finder = HighestTemperatureFinder(
        args.input_file, args.start_date, args.end_date, args.output_file
    )

    # Run the analysis
    temp_finder.analyze()
