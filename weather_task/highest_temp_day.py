# Task: Find the day with highest temperature
import csv
from datetime import datetime
from ArgParser_class import ArgParser

class HighestTemperatureFinder:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.output_file = output_file

    def read_filtered_data(self):
        """Read the CSV file and yield rows that match the date filter."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read CSV in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            yield row  # Yield only rows that fall within the date range
                    except ValueError as e:
                        print(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.")
            return  # Return an empty generator if file not found

    def find_highest_temperature(self):
        """Find the day with the highest temperature."""
        max_temp = float('-inf')  # Initialize max_temp to a very low value
        highest_temp_info = {}

        # Iterate over filtered data
        for row in self.read_filtered_data():
            try:
                current_temp = float(row['Data.Temperature.Max Temp'])
                # Check if the current row has a higher max temperature
                if current_temp > max_temp:
                    max_temp = current_temp
                    highest_temp_info = {
                        'Date': row['Date.Full'],
                        'MaxTemperature': current_temp,
                        'City': row['Station.City'],
                        'State': row['Station.State']
                    }
            except ValueError as e:
                print(f"Skipping row due to data conversion error: {e}")

        # Return the highest temperature info, or None if no data was found
        return highest_temp_info if highest_temp_info else None

    def export_to_csv(self, highest_temp_info):
        """Export the highest temperature info to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'MaxTemperature', 'City', 'State'])  # Write header
                writer.writerow([highest_temp_info['Date'], highest_temp_info['MaxTemperature'], highest_temp_info['City'], highest_temp_info['State']])  # Write data

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export results."""
        highest_temp_info = self.find_highest_temperature()

        if highest_temp_info:
            print(f"Result is: {highest_temp_info}")
            self.export_to_csv(highest_temp_info)
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
