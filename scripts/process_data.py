import os
import pandas as pd
import numpy as np
import logging
from src.preprocessing import process_expression_compendium

#Removed sys.path.append(...),
# Configure logging (we can remove this its just for testing)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define directories
RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/processed")

def load_tsv_files(directory):
    """
    Load all TSV files in the given directory into a dictionary of DataFrames.

    Args:
        directory (str): Path to the directory containing TSV files.

    Returns:
        dict: Dictionary where keys are file names (without extension) and values are DataFrames.
    """
    expression_dict = {}

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for file_name in os.listdir(directory):
        if file_name.endswith(".tsv"):
            file_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(file_path, sep="\t", index_col=0)
                expression_dict[os.path.splitext(file_name)[0]] = df
                logging.info(f"Loaded {file_name} ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                logging.warning(f"Failed to load {file_name}: {e}")

    if not expression_dict:
        logging.error("No TSV files found in the directory.")
        raise ValueError("No data files were loaded. Please check your input directory.")

    return expression_dict

def main():
    logging.info("Starting data processing pipeline...")

    # Ensure the processed data directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # Load expression data
    expression_dict = load_tsv_files(RAW_DATA_DIR)

    # Process data
    logging.info("Processing expression data...")
    processed_compendium = process_expression_compendium(expression_dict)

    # Save processed data
    output_path = os.path.join(PROCESSED_DATA_DIR, "processed_compendium.tsv")
    processed_compendium.to_csv(output_path, sep="\t")

    logging.info(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    main()



#To-Do: need to install src to our working environment (setup.py)
