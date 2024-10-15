import csv
from datetime import datetime
from ArgParser_class import ArgParser

class MaxTemperatureAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.filtered_data = []  # Store relevant rows

    def read_filtered_data(self):
        """Read the CSV file and yield rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read data in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            self.filtered_data.append(row)  # Collect relevant rows
                    except ValueError as e:
                        print(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.")
            return

    def find_max_temperature(self):
        """Find the maximum temperature and its corresponding location and state."""
        max_temp = float('-inf')
        max_temp_row = None

        for row in self.filtered_data:
            try:
                # Convert temperature to float, fill with 0.0 if missing
                temp = float(row.get('Data.Temperature.Max Temp', 0.0))
                
                # Update max temperature and corresponding row if found a new max
                if temp > max_temp:
                    max_temp = temp
                    max_temp_row = row
            except ValueError as e:
                print(f"Skipping row due to data conversion error: {e}")

        return max_temp, max_temp_row

    def export_to_csv(self, max_temp, location, state):
        """Export the maximum temperature, location, and state to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['MaxTemperature', 'Location', 'State'])  # Header
                writer.writerow([max_temp, location, state])  # Data row

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()  # Read and filter data
        max_temp, max_temp_row = self.find_max_temperature()

        if max_temp_row is not None:
            location = max_temp_row['Station.Location']
            state = max_temp_row['Station.State']

            # Print the results on the console
            print(f"Maximum Temperature: {max_temp}°C")
            print(f"Location: {location}")
            print(f"State: {state}")

            # Export the results
            self.export_to_csv(max_temp, location, state)
        else:
            print("No data available for the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of MaxTemperatureAnalyzer
    analyzer = MaxTemperatureAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
