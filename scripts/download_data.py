import os

"""
Script to download data for the project.
"""

# Define RAW_PATH to target the project-level data/raw directory
RAW_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/raw")

def ensure_dirs():
    """Ensure required directories exist before writing files."""
    os.makedirs(RAW_PATH, exist_ok=True)  # Creates if not exists

if __name__ == "__main__":
    ensure_dirs()
    # TODO: Use requests library to download data here.