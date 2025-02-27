# Multi-Compendia Mapping.py

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
   python scripts/download_data.py --config full
   python scripts/process_data.py --config full
   python scripts/generate_layouts.py --config full
   ```

### 2. Single compendium mapping (PDX_polyA)

This script uses the PDX_polyA compendium from UCSC Treehouse Public Data cluster mapping.

Run this block:
   ```sh
   python scripts/download_data.py --config pdx_polya
   python scripts/process_data.py --config pdx_polya
   python scripts/generate_layouts.py --config pdx_polya
   ```
