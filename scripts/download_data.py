import os
import requests
import argparse
import logging
from config import get_config, VALID_CONFIGS
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def format_size(bytes_size):
    """Convert bytes to a human-readable format in MB or GB."""
    mb_size = bytes_size / (1024 * 1024)  # Convert bytes to MB
    if mb_size > 1024:
        return f"{mb_size / 1024:.2f} GB"
    return f"{mb_size:.2f} MB"

def download_file(url: str, file_path: str):
    """
    Downloads a file from the given URL and logs its progress with size in MB/GB.

    Parameters:
    url (str): The file URL.
    file_path (str): The full file path to save the file.
    """
    try:
        # Send a HEAD request to get the file size
        response = requests.head(url, allow_redirects=True, verify=False)
        file_size = response.headers.get('content-length')

        if file_size:
            file_size = int(file_size)
            file_size_str = format_size(file_size)
        else:
            file_size_str = "Unknown size"

        logging.info(f"Starting download: {os.path.basename(file_path)} ({file_size_str}) from {url}")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Download file
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Download complete: {file_path}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download {file_path}: {e}")

def download_files(file_dict):
    """
    Downloads multiple files from a dictionary. The keys are file paths and the values are URLs.

    Args:
        file_dict (dict): Dictionary where keys are file paths and values are URLs.
    """
    for file_path, url in file_dict.items():
        filename = os.path.basename(file_path)
        logging.info(f"Downloading {filename} from {url}...")
        download_file(url, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download genomic data files.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help=f"Configuration name (e.g., {', '.join(VALID_CONFIGS)})"
    )
    args = parser.parse_args()
    
    config = get_config(args.config)
    if config is None:
        logging.error(f"Configuration not found. Available configurations are: {', '.join(VALID_CONFIGS)}")
        exit(1)

    os.makedirs(config.raw_data_dir_path(), exist_ok=True)

    files_to_download = {**config.get_path_expression_url_targets(), **config.get_path_clinical_url_targets()}

    logging.info(f"Files will be saved in: {config.raw_data_dir_path()}\n")
    download_files(files_to_download)
