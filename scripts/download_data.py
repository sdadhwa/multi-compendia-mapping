import os

"""
Script to download data for the project.
"""

RAW_PATH = "data/raw"

def ensure_dirs():
    """Ensure required directories exist before writing files."""
    os.makedirs(RAW_PATH, exist_ok=True)  # Creates if not exists

def preprocess():
    """Preprocess downloaded data."""


if __name__ == "__main__":
    ensure_dirs()
    # TODO: Use requests library to download data here.