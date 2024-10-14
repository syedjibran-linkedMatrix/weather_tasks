# Task: Find the state with maximum occurrences
import csv
from datetime import datetime
from ArgParser_class import ArgParser
from collections import defaultdict

class StateOccurrenceAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.output_file = output_file

    def read_filtered_data(self):
        """Read the CSV file and yield rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read data in key-value pairs
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

    def count_state_occurrences(self):
        """Count occurrences of each state in the filtered data."""
        state_counts = defaultdict(int) #creates default key (state) as zero

        for row in self.read_filtered_data(): 
            state = row['Station.State']
            state_counts[state] += 1  # Increment count for the state

        return state_counts #{'NY': 100, 'CA' : 782}

    def find_most_common_state(self, state_counts):
        """Find the state with the maximum occurrences."""
        most_common_state = None
        max_occurrences = 0

        for state, count in state_counts.items():
            if count > max_occurrences:
                max_occurrences = count
                most_common_state = state

        return most_common_state, max_occurrences

    def export_to_csv(self, state, occurrences):
        """Export the state and its occurrences to a CSV file."""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['State', 'Occurrences'])  # Header
                writer.writerow([state, occurrences])  # State and occurrence count

            print(f"Results exported to {self.output_file}")
        except Exception as e:
            print(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        state_counts = self.count_state_occurrences()
        most_common_state, max_occurrences = self.find_most_common_state(state_counts)

        if most_common_state:
            print(f"State with maximum occurrences: {most_common_state}")
            print(f"Number of occurrences: {max_occurrences}")
            self.export_to_csv(most_common_state, max_occurrences)
        else:
            print("No data available for the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of StateOccurrenceAnalyzer
    analyzer = StateOccurrenceAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
