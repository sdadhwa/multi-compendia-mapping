# Multi-Compendia Mapping.py
This project facilitates the mapping of gene clusters across multiple biological compendia using data from the UCSC Treehouse Public Data. It includes scripts for processing datasets and generating gene cluster layouts using UMAP for dimensionality reduction. Scanpy is employed to filter out the 20% least variable genes before processing.

The project supports:
- Full multi-compendia mapping
- Single compendium mapping (for development & testing)
- Flexible configuration via config.py
  
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

Each script combines specific data sets to generate visualization/s for. Below is a description of
each script and a block of commands to run them.

### 1. Full Multi-Compendia Mapping (WIP)

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
Look in `multi-compendia-mapping/data/vis/plot.png` for the visualization.


### 2. Single compendium mapping (Development)

This script uses the PDX_polyA compendium from UCSC Treehouse Public Data cluster mapping. It is the smallest dataset
in the UCSC Treehouse Public Data and is used for development purposes. Primarily useful in testing file downloading
and visualization cosmetics.

Run this block:
   ```sh
   python scripts/download_data.py --config pdx_polya
   python scripts/process_data.py --config pdx_polya
   python scripts/generate_layouts.py --config pdx_polya
   ```
Look in `multi-compendia-mapping/data/pdx_polya/vis/plot.png` for the visualization.

### 3. Two compendium mapping (Development)

This script uses the PDX_polyA and PDX_RiboDeplete compendia from UCSC Treehouse Public Data cluster mapping. This builds
a compendium out of the two smallest datasets in the UCSC Treehouse Public Data. Data is trimmed to exclude the 20% least
variable genes and then a UMAP algorithm is used to generate a layout plot. This is the fastest and most concise
way to test the full workflow using Treehouse datasets.

Run this block:
   ```sh
   python scripts/download_data.py --config pdx_cellline_polya
   python scripts/process_data.py --config pdx_cellline_polya
   python scripts/generate_layouts.py --config pdx_cellline_polya
   ```
Look in `multi-compendia-mapping/data/pdx_cellline_polya/vis/plot.png` for the visualization.

### Configuration Details

The following configuration options are available for running the scripts. Each configuration specifies different 
datasets to include during the mapping workflow and paths that scripts can use to access the data.

- `production`: Uses all five compendia for full mapping.
- `pdx_polya`: Uses only the PDX_polyA dataset. This is useful for testing and development for a single compendium and no compendium merging.
- `tumor_polya`: Uses only the Tumor_polyA dataset. This is useful for testing and development for a single compendium that is around 5.5 Gb. No compendium merging expected.
- `pdx_cellline_polya`: Merges PDX_polyA and Cell Line_polyA data. This is useful for testing and development for merging two relatively small compendia.

These configurations can be specified using the --config flag when running the scripts. For example:
```shell
python scripts/download_data.py --config production
```

It is suggested that the workflow is completed start to finish ie download->process->layout using the same configuration.
This will guarantee that expected data exits and can be accessed at each step.

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
