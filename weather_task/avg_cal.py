# Task: Find average temperature and wind data, and export to CSV

import pandas as pd
from ArgParser_class import ArgParser

class WeatherDataAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.output_file = output_file
        self.df = pd.read_csv(self.input_file)

        # Convert date column to datetime
        self.df['Date.Full'] = pd.to_datetime(self.df['Date.Full'])
        self.df_filtered = self.filter_by_date_range()

    def filter_by_date_range(self):
        return self.df[(self.df['Date.Full'] >= self.start_date) & (self.df['Date.Full'] <= self.end_date)]

    def calculate_averages(self):
        sum_max_temp = sum_min_temp = sum_wind_dir = sum_wind_speed = count = 0
        
        for _, row in self.df_filtered.iterrows():
            sum_max_temp += row['Data.Temperature.Max Temp']
            sum_min_temp += row['Data.Temperature.Min Temp']
            sum_wind_dir += row['Data.Wind.Direction']
            sum_wind_speed += row['Data.Wind.Speed']
            count += 1
        
        if count > 0:
            yield (sum_max_temp / count, 
                   sum_min_temp / count, 
                   sum_wind_dir / count, 
                   sum_wind_speed / count)
        else:
            yield (None, None, None, None)

    def export_to_csv(self, averages):
        header = ['Average Maximum Temperature', 'Average Minimum Temperature', 'Average Wind Direction', 'Average Wind Speed']
        data = list(averages)

        with open(self.output_file, 'w') as file:
            file.write(','.join(header) + '\n')
            file.write(','.join(map(str, data)) + '\n')

        print(f"Results are: {data}")
        print(f"Averages exported to {self.output_file}")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of the WeatherDataAnalyzer class
    analyzer = WeatherDataAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Calculate averages and export to CSV
    averages = analyzer.calculate_averages()
    avg_values = next(averages)  # Get the averages from the generator
    analyzer.export_to_csv(avg_values)
