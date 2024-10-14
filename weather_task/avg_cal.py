import csv
import logging
import os  # Import os to check for file existence
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
        self.averages = None

    def read_filtered_data(self):
        """Read the CSV file and yield rows that match the date filter."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            yield {  # Yielding each valid row
                                'max_temp': float(row.get('Data.Temperature.Max Temp', 0)),
                                'min_temp': float(row.get('Data.Temperature.Min Temp', 0)),
                                'wind_dir': float(row.get('Data.Wind.Direction', 0)),
                                'wind_speed': float(row.get('Data.Wind.Speed', 0))
                            }
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")

    def calculate_averages(self):
        """Calculate average temperature and wind data."""
        total_max_temp = total_min_temp = total_wind_dir = total_wind_speed = 0.0
        count = 0

        for data in self.read_filtered_data():
            total_max_temp += data['max_temp']
            total_min_temp += data['min_temp']
            total_wind_dir += data['wind_dir']
            total_wind_speed += data['wind_speed']
            count += 1

        if count > 0:  # Only calculate averages if count is greater than zero
            self.averages = (
                round(total_max_temp / count, 2),
                round(total_min_temp / count, 2),
                round(total_wind_dir / count, 2),
                round(total_wind_speed / count, 2)
            )
        else:
            self.averages = None
            logging.warning("No data available for the given date range.")

    def export_results(self):
        """Export the calculated averages to a CSV file."""
        if self.averages:
            try:
                with open(self.output_file, mode='w') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(['Average Maximum Temperature', 'Average Minimum Temperature', 'Average Wind Direction', 'Average Wind Speed'])
                    writer.writerow(self.averages)

                logging.info(f"Results are: {self.averages}")
                logging.info(f"Averages exported to {self.output_file}")
            except Exception as e:
                logging.error(f"Error exporting results: {e}")
        else:
            logging.warning("No data available for the given date range.")

if __name__ == "__main__":
    args_parser = ArgParser()
    args = args_parser.parse_args()

    processor = WeatherDataProcessor(args.input_file, args.output_file, args.start_date, args.end_date)
    processor.calculate_averages()
    processor.export_results()
    