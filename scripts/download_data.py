import os
import requests
import argparse
import logging
from config import get_config, VALID_CONFIGS
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import time  

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def format_size(bytes_size):
    """Convert bytes to MB or GB for readability."""
    mb_size = bytes_size / (1024 * 1024)
    return f"{mb_size / 1024:.2f} GB" if mb_size > 1024 else f"{mb_size:.2f} MB"

def download_file(url: str, file_path: str):
    """
    Downloads a file from the given URL and logs progress without external libraries.

    Parameters:
    url (str): The file URL.
    file_path (str): The full file path to save the file.
    """
    try:
        # Get file size
        response = requests.head(url, allow_redirects=True, verify=False)
        file_size = int(response.headers.get('content-length', 0))  # Get file size in bytes
        file_size_str = format_size(file_size) if file_size else "Unknown size"

        logging.info(f"Starting download: {os.path.basename(file_path)} ({file_size_str}) from {url}")

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Download file with progress tracking
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        downloaded_size = 0  # Track downloaded bytes
        start_time = time.time()  # Track download time

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # 8KB chunks
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Calculate percentage
                    if file_size:
                        percent_done = (downloaded_size / file_size) * 100
                        progress_bar = f"[{'=' * int(percent_done // 2)}{' ' * (50 - int(percent_done // 2))}]"
                        elapsed_time = time.time() - start_time
                        speed = (downloaded_size / (1024 * 1024)) / elapsed_time if elapsed_time > 0 else 0
                        print(f"\r{progress_bar} {percent_done:.2f}% - {format_size(downloaded_size)} downloaded - {speed:.2f} MB/s", end="")

        logging.info(f"\nDownload complete: {file_path}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download {file_path}: {e}")

def download_files(file_dict):
    """Downloads multiple files with real-time progress tracking."""
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
