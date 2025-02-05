import os
import pandas as pd
import numpy as np
from src.preprocessing import process_expression_compendium

# Define the path to the raw data directory
RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/raw")

# Define the path to the processed data directory
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/processed")

def load_tsv_files(directory):
    """
    Load all TSV files in the given directory into a dictionary of dataframes.

    Args:
        directory (str): Path to the directory containing TSV files.

    Returns:
        dict: Dictionary where keys are file names (without extension) and values are dataframes.
    """
    expression_dict = {}
    for file_name in os.listdir(directory):
        if file_name.endswith(".tsv"):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path, sep="\t", index_col=0)
            expression_dict[os.path.splitext(file_name)[0]] = df
    return expression_dict

def main():
    # Ensure RAW_DATA_DIR exists
    if not os.path.exists(RAW_DATA_DIR):
        raise FileNotFoundError(f"Raw data directory '{RAW_DATA_DIR}' does not exist.")

    # Ensure PROCESSED_DATA_DIR exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # Load all TSV files from the raw data directory
    expression_dict = load_tsv_files(RAW_DATA_DIR)

    # Call the process_expression_compendium function with the built dictionary
    processed_compendium = process_expression_compendium(expression_dict)

    # Save the processed compendium to a CSV file
    processed_compendium.to_csv(os.path.join(PROCESSED_DATA_DIR, "processed_compendium.csv"), sep="\t")

if __name__ == "__main__":
    main()