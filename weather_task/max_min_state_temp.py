# Task: Find the state with maximum temperature, maximum wind speed, minimum temperature, and minimum wind speed
import csv
from datetime import datetime
from ArgParser_class import ArgParser

class StateWeatherAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.output_file = output_file

    def read_filtered_data(self):
        """Read the CSV file and yield rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile) #read data in key value pairs
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

    def find_extreme_values(self):
        """Find the states with maximum/minimum temperature and wind speed."""
        max_temp = max_wind = float('-inf') 
        min_temp = min_wind = float('inf')

        max_temp_row = max_wind_row = min_temp_row = min_wind_row = None  #These store the rows with the extreme values

        for row in self.read_filtered_data(): #iterate over rows
            try:
                #converting values from string to float
                temp_max = float(row['Data.Temperature.Max Temp'])
                temp_min = float(row['Data.Temperature.Min Temp'])
                wind_speed = float(row['Data.Wind.Speed'])

                #If the current row's max temperature is greater than max_temp, update max_temp and store the row.
                if temp_max > max_temp:
                    max_temp = temp_max
                    max_temp_row = row
                #If the current row's min temperature is smaller than min_temp, update min_temp and store the row.
                if temp_min < min_temp:
                    min_temp = temp_min
                    min_temp_row = row
                #If the current row's wind speed is greater than max_wind, update max_wind and store the row.
                if wind_speed > max_wind:
                    max_wind = wind_speed
                    max_wind_row = row
                #If the current row's wind speed is smaller than min_wind, update min_wind and store the row.
                if wind_speed < min_wind:
                    min_wind = wind_speed
                    min_wind_row = row
            except ValueError as e:
                print(f"Skipping row due to data conversion error: {e}")

        return max_temp_row, max_wind_row, min_temp_row, min_wind_row

    def extract_data(self, rows):
        """Extract relevant information from the given rows."""
        categories = ['Max Temperature', 'Max Wind Speed', 'Min Temperature', 'Min Wind Speed']
        data = [] #This list will store the extracted data for each category.

        for category, row in zip(categories, rows):  #zip combines two iterable such as data and categories
            if row:
                data.append([      
                    category,
                    row['Station.City'],
                    row['Station.Location'],
                    row['Station.Code'],
                    row['Station.State']
                ])

                #data = [['Max Temperature', 'New York', 'NY-001', 'NYC001', 'New York'],['Max Wind Speed', 'Chicago', 'IL-003', 'CHI003', 'Illinois']]
            else:
                print(f"No data available for {category}.")
                data.append([category, 'N/A', 'N/A', 'N/A', 'N/A'])

        return data

    def export_to_csv(self, data):
        """Export the extracted information to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Category', 'City', 'Location', 'Code', 'State'])  # Header
                writer.writerows(data)  # Write rows

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        rows = self.find_extreme_values()
        data = self.extract_data(rows)
        print(f"Result is: {data}")
        self.export_to_csv(data)

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of StateWeatherAnalyzer
    analyzer = StateWeatherAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
