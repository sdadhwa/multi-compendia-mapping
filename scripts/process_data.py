import os
import pandas as pd
import numpy as np
import logging
from src.preprocessing import process_expression_compendium

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define directories
RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/processed")

def load_tsv_files(directory):
    """
    Load all expression TSV files in the given directory into a dictionary of DataFrames.

    Args:
        directory (str): Path to the directory containing TSV files.

    Returns:
        dict: Dictionary where keys are file names (without extension) and values are DataFrames.
    """
    expression_dict = {}

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for file_name in os.listdir(directory):
        if file_name.endswith("_expression.tsv"):  # Only load expression files
            file_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(file_path, sep="\t", index_col=0)
                expression_dict[os.path.splitext(file_name)[0]] = df
                logging.info(f"Loaded {file_name} ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                logging.warning(f"Failed to load {file_name}: {e}")

    if not expression_dict:
        logging.error("No expression TSV files found in the directory.")
        raise ValueError("No expression data files were loaded. Please check your input directory.")

    return expression_dict

def load_clinical_files(directory):
    """
    Load all clinical TSV files in the given directory into a dictionary of DataFrames.

    Args:
        directory (str): Path to the directory containing clinical TSV files.

    Returns:
        dict: Dictionary where keys are compendium names and values are DataFrames.
    """
    clinical_dict = {}

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for file_name in os.listdir(directory):
        if "clinical" in file_name and file_name.endswith(".tsv"):  # Only load clinical files
            file_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(file_path, sep="\t", index_col=0)
                compendium_name = os.path.splitext(file_name)[0]  # Use filename as key
                clinical_dict[compendium_name] = df
                logging.info(f"Loaded {file_name} ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                logging.warning(f"Failed to load {file_name}: {e}")

    if not clinical_dict:
        logging.error("No clinical TSV files found in the directory.")
        raise ValueError("No clinical data files were loaded. Please check your input directory.")

    return clinical_dict

def process_clinical_compendium(clinical_dict):
    """
    Process a dictionary of clinical dataframes and return a merged compendium dataframe.

    Args:
        clinical_dict (dict): Dictionary where keys are compendium names and values are DataFrames containing clinical data.

    Returns:
        pd.DataFrame: Merged clinical data with compendium labels.
    """
    clinical_datasets = []

    for compendium, clinical_df in clinical_dict.items():
        # Add compendium label to clinical data
        clinical_df["Compendium"] = compendium
        clinical_datasets.append(clinical_df)

    # Merge all clinical datasets into a single DataFrame
    compendia_df = pd.concat(clinical_datasets, axis=0, ignore_index=False)
    logging.info(f"Merged clinical data shape: {compendia_df.shape}")

    return compendia_df

def main():
    logging.info("Starting data processing pipeline...")

    # Ensure the processed data directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # Load and process expression data
    expression_dict = load_tsv_files(RAW_DATA_DIR)
    logging.info("Processing expression data...")
    processed_compendium = process_expression_compendium(expression_dict)
    expression_output_path = os.path.join(PROCESSED_DATA_DIR, "processed_compendium.tsv")
    processed_compendium.to_csv(expression_output_path, sep="\t")
    logging.info(f"Processed expression data saved to {expression_output_path}")

    # Load, process, and merge clinical data
    clinical_dict = load_clinical_files(RAW_DATA_DIR)
    processed_clinical = process_clinical_compendium(clinical_dict)
    clinical_output_path = os.path.join(PROCESSED_DATA_DIR, "processed_clinical_data.tsv")
    processed_clinical.to_csv(clinical_output_path, sep="\t")
    logging.info(f"Merged clinical data saved to {clinical_output_path}")

if __name__ == "__main__":
    main()


#To-Do: need to install src to our working environment (setup.py)
