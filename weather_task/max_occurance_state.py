# Task: Find the state with maximum occurrences
import csv
import logging
from datetime import datetime
from ArgParser_class import ArgParser
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StateOccurrenceAnalyzer:
    def __init__(self, input_file, start_date, end_date, output_file):
        self.input_file = input_file
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.filtered_data = []  # Store relevant rows

    def read_filtered_data(self):
        """Read the CSV file and store relevant rows within the specified date range."""
        try:
            with open(self.input_file) as csvfile:
                reader = csv.DictReader(csvfile)  # Read data in key-value pairs
                for row in reader:
                    try:
                        date = datetime.strptime(row['Date.Full'], '%Y-%m-%d')
                        if self.start_date <= date <= self.end_date:
                            # Fill missing state values with 'Unknown'
                            state = row.get('Station.State', 'Unknown')
                            data = {
                                'date': date,
                                'state': state
                            }
                            self.filtered_data.append(data)
                    except ValueError as e:
                        logging.warning(f"Skipping row due to date parsing error: {e}")
        except FileNotFoundError:
            logging.error(f"Error: File {self.input_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error while reading file: {e}")

    def count_state_occurrences(self):
        """Count occurrences of each state in the filtered data."""
        state_counts = defaultdict(int)  # Default count is zero

        for row in self.filtered_data:
            state = row['state']
            state_counts[state] += 1  # Increment count for the state

        return state_counts  # e.g. {'NY': 100, 'CA': 782}

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

            logging.info(f"Results exported to {self.output_file}")
        except Exception as e:
            logging.error(f"Error exporting results: {e}")

    def analyze(self):
        """Run the analysis and export the results."""
        self.read_filtered_data()
        state_counts = self.count_state_occurrences()
        most_common_state, max_occurrences = self.find_most_common_state(state_counts)

        if most_common_state:
            logging.info(f"State with maximum occurrences: {most_common_state}")
            logging.info(f"Number of occurrences: {max_occurrences}")
            self.export_to_csv(most_common_state, max_occurrences)
        else:
            logging.warning("No data available for the specified date range.")

if __name__ == "__main__":
    # Parse command-line arguments
    args_parser = ArgParser()
    args = args_parser.parse_args()

    # Create an instance of StateOccurrenceAnalyzer
    analyzer = StateOccurrenceAnalyzer(args.input_file, args.start_date, args.end_date, args.output_file)

    # Run the analysis
    analyzer.analyze()
