import os
import requests
from paths import RAW_DATA_DIR

"""
Script to download genomic data and outputs both clinical and expression data files as TSV.
"""

def ensure_dirs():
    """Ensure the download directory exists."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

def download_file(url: str, filename: str):
    """
    Downloads a file from the given URL and saves it in the RAW_DATA_DIR directory.

    Parameters:
    url (str): The file URL.
    filename (str): The filename to save as.
    """
    file_path = os.path.join(RAW_DATA_DIR, filename)

    try:
        # Bypass SSL verification
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")

def download_files(file_dict):
    """
    Downloads multiple files from a dictionary of URLs and filenames.

    Parameters:
    file_dict (dict): Dictionary where keys are filenames and values are URLs.
    """
    for filename, url in file_dict.items():
        print(f"Downloading {filename} from {url}...")
        download_file(url, filename)

if __name__ == "__main__":
    ensure_dirs()

    # Dictionary of files to download
    files_to_download = {
        # Tumor Compendium (PolyA)
        "tumor_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv",
        "tumor_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_TumorCompendium_v11_PolyA_for_GEO_20240520.tsv",

        # Tumor Compendium (Ribo)
        "tumor_ribo_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/TreehousePEDv9_Ribodeplete_unique_hugo_log2_tpm_plus_1.2019-03-25.tsv",
        "tumor_ribo_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/TreehousePEDv9_Ribodeplete_clinical_metadata_for_GEO_20240520.tsv",

        # Cell Line Compendium (PolyA)
        "cell_line_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/CellLinePolyA_21.06_hugo_log2tpm_58581genes_2021-06-15.tsv",
        "cell_line_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_CellLinePolyA_21.06_for_GEO_20240520.tsv",

        # PDX Compendium (PolyA)
        "PDX_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/Treehouse-PDX-Compendium-22.03-PolyA_hugo_log2tpm_58581genes_2022-03-09.tsv",
        "PDX_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-PolyA_for_GEO_20240520.tsv",

        # PDX Compendium (Ribo)
        "PDX_ribo_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/Treehouse-PDX-Compendium-22.03-Ribodeplete_hugo_log2tpm_58581genes_2022-03-10.tsv",
        "PDX_ribo_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-Ribodeplete_for_GEO_20240520.tsv",
    }
    print(f"Files will be saved in: {RAW_DATA_DIR}\n")
    download_files(files_to_download)
    # TODO: Use requests library to download data here.
