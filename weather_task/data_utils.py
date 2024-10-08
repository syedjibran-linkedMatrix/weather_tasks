import pandas as pd
from ArgParser_class import ArgParser

def initialize_args():
    # Initialize argument parser
    args_parser = ArgParser()
    return args_parser.parse_args()

def load_dataset(input_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    # Convert date column to datetime
    df['Date.Full'] = pd.to_datetime(df['Date.Full'])
    return df

def filter_by_date(df, start_date, end_date):
    # Filter by date range
    df_filtered = df[(df['Date.Full'] >= start_date) & (df['Date.Full'] <= end_date)]
    return df_filtered
