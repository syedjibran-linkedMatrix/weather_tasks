import argparse
import os
from datetime import datetime

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Weather Data Analysis")

        # Adding arguments for date range, input file, and output file
        self.parser.add_argument(
            '--start-date', type=str, required=True, help="Start date for the analysis (YYYY-MM-DD)"
        )
        self.parser.add_argument(
            '--end-date', type=str, required=True, help="End date for the analysis (YYYY-MM-DD)"
        )
        self.parser.add_argument(
            '--input-file', type=str, required=True, help="Input CSV file with weather data"
        )
        self.parser.add_argument(
            '--output-file', type=str, required=True, help="Output CSV file for results"
        )

    def parse_args(self):
        args = self.parser.parse_args()
        
        # Validate date formats
        try:
            args.start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
            args.end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError as e:
            self.parser.error(f"Invalid date format: {e}")

        # Check if start date is greater than end date
        if args.start_date > args.end_date:
            self.parser.error("Start date must be less than or equal to end date.")

        # Check if input file exists
        if not os.path.isfile(args.input_file):
            self.parser.error(f"Input file '{args.input_file}' does not exist.")

        return args
