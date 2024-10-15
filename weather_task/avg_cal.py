# Task: Find average temperature and wind data, and export to CSV
import csv
import logging
from datetime import datetime
from ArgParser_class import ArgParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherDataProcessor:
    def __init__(self, input_file: str, output_file: str, start_date: datetime, end_date: datetime):
        self.input_file = input_file
        self.output_file = output_file
        self.start_date = start_date
        self.end_date = end_date
        self.filtered_data = []  # Store filtered data here
        self.averages = None

    def read_filtered_data(self):
        """Read the CSV file and store filtered rows."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
                        continue  # Move to the next row if date parsing fails

                    if self.start_date <= date <= self.end_date:
                        try:
                            data = {
                                'max_temp': float(row.get('Data.Temperature.Max Temp', 0.0) or 0.0),
                                'min_temp': float(row.get('Data.Temperature.Min Temp', 0.0) or 0.0),
                                'wind_dir': float(row.get('Data.Wind.Direction', 0.0) or 0.0),
                                'wind_speed': float(row.get('Data.Wind.Speed', 0.0) or 0.0)
                            }
                            self.filtered_data.append(data)
                        except (TypeError, ValueError) as e:
                            logging.warning(f"Skipping row due to data conversion error: {e}")

            logging.info(f"Finished reading and storing {len(self.filtered_data)} rows of filtered data.")

        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def calculate_averages(self):
        """Calculate averages using the filtered data."""
        total_max_temp = total_min_temp = total_wind_dir = total_wind_speed = 0.0
        count = len(self.filtered_data)  # Get the number of filtered data entries

        if count == 0:
            logging.warning("No data available for the given date range.")
            self.averages = None
            return

        for data in self.filtered_data:
            total_max_temp += data['max_temp']
            total_min_temp += data['min_temp']
            total_wind_dir += data['wind_dir']
            total_wind_speed += data['wind_speed']

        self.averages = (
            round(total_max_temp / count, 2),
            round(total_min_temp / count, 2),
            round(total_wind_dir / count, 2),
            round(total_wind_speed / count, 2)
        )
        logging.info(f"Calculated averages: {self.averages}")

    def export_results(self):
        """Export the calculated averages to a CSV file."""
        if self.averages:
            try:
                with open(self.output_file, mode='w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow([
                        'Average Maximum Temperature',
                        'Average Minimum Temperature',
                        'Average Wind Direction',
                        'Average Wind Speed'
                    ])
                    writer.writerow(self.averages)

                logging.info(f"Averages successfully exported to {self.output_file}")
            except PermissionError:
                logging.error(f"Error: Permission denied for file {self.output_file}.")
            except Exception as e:
                logging.error(f"Error exporting results: {e}")
        else:
            logging.error("No data available to export.")

if __name__ == "__main__":
    args_parser = ArgParser()
    args = args_parser.parse_args()

    processor = WeatherDataProcessor(
        args.input_file, args.output_file, args.start_date, args.end_date
    )

    # Read filtered data first
    processor.read_filtered_data()

    # Calculate averages using the stored filtered data
    processor.calculate_averages()

    # Export the results
    processor.export_results()
