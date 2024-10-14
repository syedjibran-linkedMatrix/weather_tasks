import argparse 
class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Weather Data Analysis")

        # Adding arguments for date range, input file, and output file
        self.parser.add_argument(
            '--start-date', type= str, required=True, help="Start date for the analysis (YYYY-MM-DD)"
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
        return self.parser.parse_args()

#To test this file independently we are using main --> dunder method
if __name__ == "__main__":
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    


