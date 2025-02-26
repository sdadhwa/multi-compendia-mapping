import os
import requests
import argparse
from config import get_config, VALID_CONFIGS
from paths import RAW_DATA_DIR

"""
Script to download genomic data and outputs both clinical and expression data files as TSV.
"""

def download_file(url: str, file_path: str):
    """
    Downloads a file from the given URL and saves it in the specified file path.

    Parameters:
    url (str): The file URL.
    file_path (str): The full file path to save the file.
    """
    try:
        # Bypass SSL verification
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_path}: {e}")

def download_files(file_dict):
    """
    Downloads multiple files from a dictionary. The keys are file paths and the values are URLs.

    Args:
        file_dict (dict): Dictionary where keys are file paths and values are URLs.
    """

    for file_path, url in file_dict.items():
        filename = os.path.basename(file_path)
        print(f"Downloading {filename} from {url}...")
        download_file(url, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download genomic data files.")
    # Create an argument for the configuration name
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help=f"Configuration name (e.g., {', '.join(VALID_CONFIGS)})"
    )
    args = parser.parse_args()

    # Get the configuration class based on the configuration name
    config = get_config(args.config)
    if config is None:
        # If the configuration is not found, indicate which configurations are available and exit.
        print(f"Configuration not found. Available configurations are:{VALID_CONFIGS}")
        exit(1)

    # Create the raw data directory if it does not exist
    os.makedirs(config.raw_data_dir_path(), exist_ok=True)

    # Merge expression and clinical file paths and url targets into a single dictionary
    files_to_download = {**config.get_path_expression_url_targets(), **config.get_path_clinical_url_targets()}

    print(f"Files will be saved in: {config.raw_data_dir_path()}\n")
    download_files(files_to_download)