import os
import requests

"""
Script to download genomic data for the project as .tsv files using a requests library.


"""

# Define RAW_PATH to target the project-level data/raw directory
RAW_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/raw")

def ensure_dirs():
    """Ensure required directories exist before writing files."""
    os.makedirs(RAW_PATH, exist_ok=True)  # Creates if not exists

def download_file(url: str, filename: str):
    """
    Downloads a file from the given URL and saves it in the RAW_PATH directory.

    Parameters:
    url (str): The URL to download the file from.
    filename (str): The name to save the file as.
    """
    file_path = os.path.join(RAW_PATH, filename)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for failed requests

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")

def download_files(file_dict):
    """
    Downloads multiple files based on a dictionary of URLs and filenames.

    Parameters:
    file_dict (dict): A dictionary where keys are filenames and values are URLs.
    """
    for filename, url in file_dict.items():
        print(f"Downloading {filename} from {url}...")
        download_file(url, filename)

if __name__ == "__main__":
    ensure_dirs()

    # Dictionary of files to download (Replace with actual URLs)
    files_to_download = {
        "genome1.tsv": "https://example.com/genome1.tsv",
        "genome2.tsv": "https://example.com/genome2.tsv",
        "genome3.tsv": "https://example.com/genome3.tsv",
    }

    download_files(files_to_download)
    # TODO: Use requests library to download data here.
