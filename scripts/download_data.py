import os
import requests
import argparse
import logging
from config import get_config, VALID_CONFIGS
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Suppress HTTPS warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Logging set up
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_file_size(url):
    """
    Get the size of a file from a given URL before downloading.

    Args:
        url (str): File URL.

    Returns:
        str: File size in MB or "Unknown MB" if not retrievable.
    """
    try:
        response = requests.head(url, verify=False)
        size = int(response.headers.get('content-length', -1)) / (1024 * 1024)
        return f"{size:.2f} MB" if size > 0 else "Unknown MB"
    except Exception:
        return "Unknown MB"

def download_file(url: str, file_path: str):
    """
    Downloads a file from the given URL and saves it in the specified file path.

    Args:
        url (str): The file URL.
        file_path (str): The full file path to save the file.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Get file size before downloading
        file_size = get_file_size(url)
        filename = os.path.basename(file_path)

        logger.info(f"Starting download: {filename} ({file_size}) from {url}")

        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logger.info(f"Download complete: {file_path}\n")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {file_path}: {e}")

def download_files(file_dict):
    """
    Downloads multiple files from a dictionary.

    Args:
        file_dict (dict): Dictionary where keys are file paths and values are URLs.
    """
    for file_path, url in file_dict.items():
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
        logger.error(f"Configuration not found. Available configurations are: {VALID_CONFIGS}")
        exit(1)

    # Create the raw data directory if it does not exist
    os.makedirs(config.raw_data_dir_path(), exist_ok=True)

    # Merge expression and clinical file paths and url targets into a single dictionary
    files_to_download = {**config.get_path_expression_url_targets(), **config.get_path_clinical_url_targets()}

    logger.info(f"\nFiles will be saved in: {config.raw_data_dir_path()}\n")
    download_files(files_to_download)
