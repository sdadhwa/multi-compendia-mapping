import scanpy as sc
import pandas as pd
import numpy as np
import os

# Define local file paths for downloaded expression and clinical data
EXPRESSION_FILES = {
    "Tumor_polyA": "data/Tumor_polyA_TPM.tsv",
    "Tumor_rRNA": "data/Tumor_rRNA_TPM.tsv",
    "CellLine_polyA": "data/CellLine_polyA_TPM.tsv",
    "PDX_polyA": "data/PDX_polyA_TPM.tsv",
    "PDX_rRNA": "data/PDX_rRNA_TPM.tsv",
}

CLINICAL_FILES = {
    "Tumor_polyA": "data/Tumor_polyA_Clinical.tsv",
    "Tumor_rRNA": "data/Tumor_rRNA_Clinical.tsv",
    "CellLine_polyA": "data/CellLine_polyA_Clinical.tsv",
    "PDX_polyA": "data/PDX_polyA_Clinical.tsv",
    "PDX_rRNA": "data/PDX_rRNA_Clinical.tsv",
}

# Create lists to store processed data
filtered_datasets = []
clinical_datasets = []

# Process each dataset
for compendium, expression_path in EXPRESSION_FILES.items():
    print(f"Processing {compendium} dataset...")

    # Load gene expression data
    expression_df = pd.read_csv(expression_path, sep="\t", index_col=0)

    # Convert to Scanpy AnnData format
    adata = sc.AnnData(expression_df.T)  # Transpose: Genes → Variables, Samples → Observations

    # Remove genes with very low expression (mean log2(TPM+1) < 1)
    min_expression = 1  # Threshold for minimum expression
    gene_means = adata.X.mean(axis=0)  # Mean expression per gene
    genes_to_keep = gene_means > min_expression
    adata = adata[:, genes_to_keep]  # Keep only genes that pass the threshold

    # Remove the least variable 20% of genes
    sc.pp.highly_variable_genes(adata, flavor="seurat_v3", n_top_genes=int(0.8 * adata.shape[1]))  
    adata = adata[:, adata.var.highly_variable]  # Keep only highly variable genes

    # Convert back to Pandas DataFrame
    filtered_expression_df = pd.DataFrame(adata.X.T, index=adata.var_names, columns=adata.obs_names)
    filtered_expression_df["compendium"] = compendium  # Add a compendium column

    # Store filtered dataset
    filtered_datasets.append(filtered_expression_df)

    # Process clinical data
    clinical_path = CLINICAL_FILES[compendium]
    clinical_df = pd.read_csv(clinical_path, sep="\t", index_col=0)

    # Add compendium label to clinical data
    clinical_df["compendium"] = compendium

    # Store clinical dataset
    clinical_datasets.append(clinical_df)

# Merge all processed datasets into a single DataFrame
final_expression_df = pd.concat(filtered_datasets, axis=1)  # Merge all gene expression data
final_clinical_df = pd.concat(clinical_datasets)  # Merge all clinical data

# Save the processed data
final_expression_df.to_csv("filtered_gene_expression.tsv", sep="\t")
final_clinical_df.to_csv("filtered_clinical_data.tsv", sep="\t")

