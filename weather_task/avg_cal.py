# Task: Find average temperature and wind data, and export to CSV
import csv
from datetime import datetime
from ArgParser_class import ArgParser

class WeatherDataProcessor:
    def __init__(self, input_file, output_file, start_date, end_date):
        self.input_file = input_file
        self.output_file = output_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.averages = None

    def read_filtered_data(self):
        """Read the CSV file and yield rows that match the date filter."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile) #read file in key value pairs --> DictReader
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d') #convert date string to date object --> strptime 
                        if self.start_date <= date <= self.end_date: #This condition checks if the date (converted from the CSV string) falls within the specified date range.
                            yield row
                    except ValueError as e:
                        print(f"Skipping row due to date parsing error: {e}") #catch error if any row in not processed i.e: date format is incorrect
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.") # raise error if input file do not found
            return  # Return an empty generator if file not found

    def calculate_averages(self):
        """Calculate average temperature and wind data."""
        total_max_temp = total_min_temp = total_wind_dir = total_wind_speed = 0
        count = 0

        for row in self.read_filtered_data():
            try:
                total_max_temp += float(row['Data.Temperature.Max Temp'])
                total_min_temp += float(row['Data.Temperature.Min Temp'])
                total_wind_dir += float(row['Data.Wind.Direction'])
                total_wind_speed += float(row['Data.Wind.Speed'])
                count += 1
            except ValueError as e:
                print(f"Error converting data to float: {e}")

        if count == 0:
            self.averages = None  # No data available
            return

        avg_max_temp = total_max_temp / count
        avg_min_temp = total_min_temp / count
        avg_wind_dir = total_wind_dir / count
        avg_wind_speed = total_wind_speed / count
        
        self.averages = (avg_max_temp, avg_min_temp, avg_wind_dir, avg_wind_speed)

    def export_results(self):
        """Export the calculated averages to a CSV file."""
        if self.averages: #if averages are not none
            try:
                with open(self.output_file, mode='w') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(['Average Maximum Temperature', 'Average Minimum Temperature', 'Average Wind Direction', 'Average Wind Speed'])
                    writer.writerow(self.averages)

                print(f"Results are: {self.averages}")
                print(f"Averages exported to {self.output_file}")
            except Exception as e:
                print(f"Error exporting results: {e}")
        else:
            print("No data available for the given date range.") #if start date or end date is not in the dataset

def main():
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of the WeatherDataProcessor class
    processor = WeatherDataProcessor(args.input_file, args.output_file, args.start_date, args.end_date)

    # Calculate averages
    processor.calculate_averages()

    # Export results to CSV
    processor.export_results()

if __name__ == "__main__":  #checks whether current file code is running as a main program --> dunder method
    main()
