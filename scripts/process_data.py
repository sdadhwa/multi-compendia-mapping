import os
import pandas as pd
import numpy as np
import logging
from src.preprocessing import process_expression_compendium
#Removed sys.path.append(...),
#Configure logging (we can remove this its just for testing)
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

def merge_clinical_data(directory):
    """
    Load and merge all clinical TSV files in the given directory into a single DataFrame.

    Args:
        directory (str): Path to the directory containing clinical TSV files.

    Returns:
        pd.DataFrame: Merged clinical data.
    """
    clinical_files = [file for file in os.listdir(directory) if "clinical" in file and file.endswith(".tsv")]
    
    if not clinical_files:
        raise FileNotFoundError("No clinical data files found in the directory.")

    clinical_dfs = []
    for file_name in clinical_files:
        file_path = os.path.join(directory, file_name)
        try:
            df = pd.read_csv(file_path, sep="\t", index_col=0)
            df["Source_File"] = file_name  # Add column to track origin
            clinical_dfs.append(df)
        except Exception as e:
            logging.warning(f"Failed to load {file_name}: {e}")

    merged_clinical = pd.concat(clinical_dfs, axis=0, ignore_index=False)
    logging.info(f"Merged clinical data shape: {merged_clinical.shape}")

    return merged_clinical

def main():
    logging.info("Starting data processing pipeline...")

    # Ensure the processed data directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # Load and process expression data
    expression_dict = load_tsv_files(RAW_DATA_DIR)
    logging.info("Processing expression data...")
    processed_compendium = process_expression_compendium(expression_dict)
    expression_output_path = os.path.join(PROCESSED_DATA_DIR, "processed_compendium.tsv")     #Processed Expression data
    processed_compendium.to_csv(expression_output_path, sep="\t")
    logging.info(f"Processed expression data saved to {expression_output_path}")

    # Merge and save clinical data
    merged_clinical = merge_clinical_data(RAW_DATA_DIR)
    clinical_output_path = os.path.join(PROCESSED_DATA_DIR, "processed_clinical_data.tsv")    #Processed Clinical dataa
    merged_clinical.to_csv(clinical_output_path, sep="\t")
    logging.info(f"Merged clinical data saved to {clinical_output_path}")

if __name__ == "__main__":
    main()


#To-Do: need to install src to our working environment (setup.py)
