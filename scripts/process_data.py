import os
import pandas as pd
import argparse
import time
from config import get_config, VALID_CONFIGS
import logging
from preprocessing import process_expression_compendium
from preprocessing import process_clinical_compendium

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_tsv_files(directory):
    """
    Load all expression TSV files in the given directory into a dictionary of DataFrames. Data is stored in files in
    (gene, sample) format. The DataFrames are transposed to (sample, gene) format when read from file. (Sample, gene)
    format implies comparing samples instead of comparing genes.

    Args:
        directory (str): Path to the directory containing TSV files.

    Returns:
        dict: Dictionary where keys are file names (without extension) and values are DataFrames. The data frames are in
            (sample, gene) format.
    """
    expression_dict = {}

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    for file_name in os.listdir(directory):
        if file_name.endswith("_expression.tsv"):  # Only load expression files
            file_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(file_path, sep="\t", index_col=0)
                df = df.T  # Transpose so samples are rows and genes are columns
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

def main():
    """
    Main function to process genomic data files. Reads expression and clinical data files, processes them, merges them
    into one expression compendium and one clinical compendium, and saves them to files.

    Note: Expression data is stored in (gene, sample) format. This is counterintuitive because the goal is to compare
    samples, not genes. However, this format is used to maintain consistency with the original data files. There
    are also readability benefits to having fewer columns and more rows. The data is transposed to (sample, gene) format
    before processing, and is transposed back to (gene, sample) format before saving.
    """
    parser = argparse.ArgumentParser(description="Process genomic data files.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help=f"Configuration name (e.g., {', '.join(VALID_CONFIGS)})"
    )
    args = parser.parse_args()

    config = get_config(args.config)
    if config is None:
        print(f"Configuration not found. Available configurations are: {', '.join(VALID_CONFIGS)}")
        exit(1)

    raw_dir = config.raw_data_dir_path()
    expression_file_path = config.expression_file_path()
    clinical_file_path = config.clinical_file_path()

    logging.info("Starting data processing pipeline...")

    # Ensure the processed data directory exists
    os.makedirs(config.processed_dir_path(), exist_ok=True)

    # Load and process expression data
    logging.info(f"Reading expression data files from {raw_dir}...")
    start_time = time.time()
    expression_dict = load_tsv_files(raw_dir)
    logging.info("Processing expression data...")
    processed_compendium = process_expression_compendium(expression_dict, variance_threshold=20)
    logging.info(f"Writing processed expression data to {expression_file_path}...")
    processed_compendium.T.to_csv(expression_file_path, sep="\t")
    logging.info(f"Processed expression data saved to {expression_file_path}. Time taken: {time.time() - start_time:.2f}s")

    # Load, process, and merge clinical data
    logging.info("Reading clinical data files...")
    clinical_dict = load_clinical_files(raw_dir)
    logging.info("Processing clinical data...")
    processed_clinical = process_clinical_compendium(clinical_dict)
    logging.info(f"Writing processed clinical data to {clinical_file_path}...")
    processed_clinical.to_csv(clinical_file_path, sep="\t")
    logging.info(f"Merged clinical data saved to {clinical_file_path}")

if __name__ == "__main__":
    main()
