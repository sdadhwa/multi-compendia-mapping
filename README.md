# Multi-Compendia Mapping.py
This project facilitates the mapping of gene clusters across multiple biological compendia types using data from the UCSC Treehouse Public Data. It provides scripts for processing different sets of data and generating gene cluster layouts using UMAP for dimensionality reduction. Additionally, Scanpy is used to trim the 20% least variable data before processing. The project supports  full multi-compendia mapping, as well as single compendia mapping for development purposes. The configuration file can be updated to add more dtatasets/adjust existing sets in config.py.

## Setting Up the Conda Environment

1. **Create the Conda Environment:**

   Run the following command in your terminal to create the environment from the `environment.yml` file:

   ```sh
   conda env create -f environment.yml
   
2. **Activate the Conda Environment:**

   After the environment is created, activate it using:

   ```sh
   conda activate mcomp-mapping-env
   ```

## Running Scripts

This project includes multiple scripts that process different sets of data and present various types of results. Each 
script is designed to handle specific data configurations and generate outputs accordingly. Below is a description of
each script and a block of commands to run them.

### 1. Full Multi-Compendia Mapping

This script uses the 5 compendia types from the UCSC Treehouse Public Data to generate gene cluster mapping.

| Biological Source Type | Library Preparation Method       |
|------------------------|----------------------------------|
| Tumor                  | polyA selection                  |
| Tumor                  | ribosomal RNA depletion          |
| Cell line              | polyA selection                  |
| PDX                    | polyA selection                  |
| PDX                    | ribosomal RNA depletion          |

Run this block:
   ```sh
   python scripts/download_data.py --config production
   python scripts/process_data.py --config production
   python scripts/generate_layouts.py --config production
   ```

### 2. Single compendium mapping (PDX_polyA)

This script uses the PDX_polyA compendium from UCSC Treehouse Public Data cluster mapping.

Run this block:
   ```sh
   python scripts/download_data.py --config pdx_polya
   python scripts/process_data.py --config pdx_polya
   python scripts/generate_layouts.py --config pdx_polya
   ```

### Configuration Details

The --config flag determines which dataset is used. Available options:

production: Uses all five compendia for full mapping.

pdx_polya: Uses only the PDX_polyA dataset.

### Expected Output

Each script generates processed gene cluster mapping layouts using UMAP. Before mapping, Scanpy is used to trim the 20% least variable data. The output format may include:

TSV files containing processed data.

UMAP files with structured mapping information.

Visual representations (if applicable) stored in an output/ directory.

### Troubleshooting & Common Issues

Environment Creation Fails: Ensure Conda is installed and the environment.yml file is correctly formatted.

Module Import Errors: Activate the environment using conda activate mcomp-mapping-env before running scripts.

Permission Errors: Run commands with the appropriate user privileges.

### Contribution Guidelines

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -m "Added new feature").

Push to the branch (git push origin feature-branch).

Submit a pull request.

### License [needs updates]

This project is licensed under an MIT license. See LICENSE file for details.
