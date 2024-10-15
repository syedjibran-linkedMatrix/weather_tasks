# Task: Find the state with maximum temperature, maximum wind speed, minimum temperature, and minimum wind speed
import csv
import logging
from datetime import datetime
from ArgParser_class import ArgParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StateWeatherAnalyzer:
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
                            # Store only relevant fields, filling missing values with 0.0
                            max_temp = row.get('Data.Temperature.Max Temp')
                            min_temp = row.get('Data.Temperature.Min Temp')
                            wind_speed = row.get('Data.Wind.Speed')

                            # Fill missing values with 0.0 and convert to float
                            data = {
                                'city': row.get('Station.City', 'N/A'),
                                'location': row.get('Station.Location', 'N/A'),
                                'code': row.get('Station.Code', 'N/A'),
                                'state': row.get('Station.State', 'N/A'),
                                'max_temp': float(max_temp) if max_temp is not None else 0.0,
                                'min_temp': float(min_temp) if min_temp is not None else 0.0,
                                'wind_speed': float(wind_speed) if wind_speed is not None else 0.0
                            }
                            self.filtered_data.append(data)
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def find_extreme_values(self):
        """Find the states with maximum/minimum temperature and wind speed."""
        max_temp = max_wind = float('-inf') 
        min_temp = min_wind = float('inf')

        max_temp_row = max_wind_row = min_temp_row = min_wind_row = None  # Store rows with extreme values

        for row in self.filtered_data:  # Iterate over relevant rows
            # Extract relevant values from filtered data
            temp_max = row['max_temp']
            temp_min = row['min_temp']
            wind_speed = row['wind_speed']

            # Update max temperature and store corresponding row
            if temp_max > max_temp:
                max_temp = temp_max
                max_temp_row = row
            # Update min temperature and store corresponding row
            if temp_min < min_temp:
                min_temp = temp_min
                min_temp_row = row
            # Update max wind speed and store corresponding row
            if wind_speed > max_wind:
                max_wind = wind_speed
                max_wind_row = row
            # Update min wind speed and store corresponding row
            if wind_speed < min_wind:
                min_wind = wind_speed
                min_wind_row = row

        return max_temp_row, max_wind_row, min_temp_row, min_wind_row

    def extract_data(self, rows):
        """Extract relevant information from the given rows."""
        categories = ['Max Temperature', 'Max Wind Speed', 'Min Temperature', 'Min Wind Speed']
        data = []  # List to store extracted data for each category

        for category, row in zip(categories, rows):  # Combine categories with corresponding rows
            if row:
                data.append([      
                    category,
                    row['city'],
                    row['location'],
                    row['code'],
                    row['state']
                ])
            else:
                logging.warning(f"No data available for {category}.")
                data.append([category, 'N/A', 'N/A', 'N/A', 'N/A'])

        return data

    def export_to_csv(self, data):
        """Export the extracted information to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Category', 'City', 'Location', 'Code', 'State'])  # Header
                writer.writerows(data)  # Write rows

            logging.info(f"Results exported to {self.output_file}")
        except Exception as e:
            logging.error(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()
        rows = self.find_extreme_values()
        data = self.extract_data(rows)
        logging.info(f"Result is: {data}")
        self.export_to_csv(data)

if __name__ == "__main__":
    # Parse command-line arguments
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    # Create an instance of StateWeatherAnalyzer
    analyzer = StateWeatherAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
