# Development Log

Project Name: Multi-Compendia Mapping
Authors: Ally Hoogs, Sunny Dadhwal, Hansa Atreya, Piet Rottinghuis 
Start Date: 2025-01-27

### Overview
#### Progress Summary:
- Implemented core functionality for multi-compendia mapping.
- Integrated UMAP for dimensionality reduction.
- Added numpy/pandas preprocessing to filter least variable 20% of data.
- Refactored pipeline to support modular configurations.
- Improved visualization options (color-coding clusters by metadata).
- Optimized UMAP parameters for better separation of clusters.

#### Next Steps:
- Implement patient-specific sequence analysis by plotting data by patient ID.
- Explore alternative visualization methods beyond UMAP to improve analysis of smaller datasets.
- Expand dataset comparisons using different clinical variables.

#### Key Features Implemented:
1. Multi-Compendia Gene Mapping
Supports five biological source types from UCSC Treehouse Public Data.
Allows full multi-compendia mapping or single-compendium analysis (e.g., PDX_polyA).
3. Data Processing & Dimensionality Reduction
Uses numpy and pandas to preprocess and remove the least variable 20% of the dataset.
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
Uses Matplotlib & Seaborn to generate UMAP plots with legend, option to toggle dataset visibility.
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
-Initial setup & repo structure (2025-01-30)
- Dataset retrieval pipeline implemented (2025-02-06)
- Preprocessing pipeline integrated (gene filtering & normalization) (2025-02-28)
- UMAP-based dimensionality reduction applied to compendia (2025-02-28)
- First UMAP visualizations generated & reviewed (2025-02-28)
- Scanpy integrated for preprocessing & filtering (YYYY-MM-DD)
- Refactored pipeline to support modular configurations (2025-02-25)
- Evaluation of dataset mixing across five compendium types (2025-03-06)
- Validation of clustering consistency across different UMAP parameters (2025-03-06)
- GitHub repository documentation & initial release (2025-02-27)
  
#### Upcoming Features & Enhancements:
-Implement alternative clustering methods (Leiden, HDBSCAN)
-Benchmark performance on larger datasets 


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
