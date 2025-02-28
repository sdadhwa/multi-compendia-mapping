# Development Log

Project Name: Multi-Compendia Mapping
Authors: Ally Hoogs, Sunny Dadhwal, Hansa Atreya, Piet Rottinghuis 
Start Date: 2025-01-27

### Overview
#### Progress Summary:
- Implemented core functionality for multi-compendia mapping.
- Integrated UMAP for dimensionality reduction.
- Added Scanpy preprocessing to filter least variable 20% of data.
- Refactored pipeline to support modular configurations.

#### Next Steps:
- Improve visualization options (color-coding clusters by metadata).
- Optimize UMAP parameters for better separation of clusters.

#### Key Features Implemented:
1. Multi-Compendia Gene Mapping
Supports five biological source types from UCSC Treehouse Public Data.
Allows full multi-compendia mapping or single-compendium analysis (e.g., PDX_polyA).
3. Data Processing & Dimensionality Reduction
Uses Scanpy to preprocess and remove the least variable 20% of the dataset.
Implements UMAP for high-dimensional gene expression visualization.
4. Configurable Pipeline
Configurations set via --config flags (production, pdx_polya, etc.).
Modular scripts for easy extension and dataset-specific processing.
5. Automated Workflow
Download step: Retrieves required genomic datasets.
Processing step: Cleans, normalizes, and structures expression data.
Layout generation step: Applies UMAP and outputs cluster mappings.
6. Output & Visualization
Outputs TSV and UMAP files with structured gene mappings.
Uses Matplotlib & Seaborn to generate UMAP plots.
7. Environment & Reproducibility
Conda environment (mcomp-mapping-env) ensures dependency consistency.
Setup simplified using environment.yml.
8. Open-Source & Contribution
Licensed under MIT License (open for modification and reuse).
GitHub repo includes structured README, installation guide, and contribution guidelines.

### Setup + Environment
See README for setup and running instructions.

### Timeline

#### Completed Milestones:
-Initial setup & repo structure (YYYY-MM-DD)
-Basic processing pipeline for gene expression data (YYYY-MM-DD)
-Integration of Scanpy for preprocessing (YYYY-MM-DD)
-UMAP-based dimensionality reduction implemented (YYYY-MM-DD)

#### Upcoming Features & Enhancements:
-Improve visualization with metadata color mapping (ETA: YYYY-MM-DD)
-Optimize UMAP hyperparameters for better clustering (ETA: YYYY-MM-DD)
-Implement alternative clustering methods (Leiden, HDBSCAN) (ETA: YYYY-MM-DD)
-Benchmark performance on larger datasets (ETA: YYYY-MM-DD)


### Challenges & Solutions:
Handling large datasets efficiently: Optimized data loading using Pandas. [config options]
Ensuring reproducibility: Environment setup via Conda to standardize dependencies.

### Future Usage
Scalability:
Designed to process datasets of varying sizes, ensuring adaptability to new genomic data.
Configurable scripts allow switching between full and single-compendium mapping.

Reproducibility:
Standardized dependencies via Conda and environment.yml.
Clear documentation ensures easy setup for new users.

Extensibility:
Modular script structure allows easy integration of new clustering techniques.
Open to future contributions for enhanced visualization and analysis.

Potential Applications:
Comparative genomic studies across tumor, PDX, and cell line samples.
Identifying gene expression patterns using UMAP-based visualizations.
