import os

"""
File paths for the scripts.
"""

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define file paths relative to the project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
EXPRESSION_FILE = os.path.join(PROCESSED_DIR, "processed_compendium.tsv")
CLINICAL_FILE = os.path.join(PROCESSED_DIR, "processed_clinical_data.tsv")