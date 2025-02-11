import scanpy as sc
import pandas as pd
import numpy as np

LOWEST_VARIANCE_PERCENTILE = 20

def process_expression_compendium(expression_dict):
    """
    Process a dictionary of gene expression dataframes and return a compendium dataframe.

    Args:
        expression_dict (dict): Dictionary where keys are compendium names and values are dataframes containing gene expression data.

    Returns:
        pd.DataFrame: Compendia dataframe with filtered gene expression data and compendium labels.
    """
    filtered_datasets = []

    for compendium, expression_df in expression_dict.items():
        # Convert to Scanpy AnnData format
        adata = sc.AnnData(expression_df.T)  # Transpose: Genes → Variables, Samples → Observations

        # Remove genes with very low expression (mean log2(TPM+1) < 1)
        min_expression = 1  # Threshold for minimum expression
        gene_means = adata.X.mean(axis=0)  # Mean expression per gene
        genes_to_keep = gene_means > min_expression
        adata = adata[:, genes_to_keep]  # Keep only genes that pass the threshold

        # Calculate variance for each gene
        gene_variances = adata.X.var(axis=0)

        # Determine the threshold for the top 80% most variable genes
        threshold = np.percentile(gene_variances, LOWEST_VARIANCE_PERCENTILE)

        # Select genes with variance above the threshold
        genes_to_keep = gene_variances > threshold
        adata = adata[:, genes_to_keep]  # Keep only the most variable genes

        # Convert back to Pandas DataFrame
        filtered_expression_df = pd.DataFrame(adata.X.T, index=adata.var_names, columns=adata.obs_names)
        filtered_expression_df["compendium"] = compendium  # Add a compendium column

        # Store filtered dataset
        filtered_datasets.append(filtered_expression_df)

    # Merge all processed datasets into a single DataFrame
    compendia_df = pd.concat(filtered_datasets, axis=0)  # Merge all gene expression data

    return compendia_df


def process_clinical_compendium(clinical_dict):
    """
    Process a dictionary of clinical dataframes and return a compendium dataframe.

    Args:
        clinical_dict (dict): Dictionary where keys are compendium names and values are dataframes containing clinical data.

    Returns:
        pd.DataFrame: Compendia dataframe with clinical data and compendium labels.
    """
    clinical_datasets = []

    for compendium, clinical_df in clinical_dict.items():
        # Add compendium label to clinical data
        clinical_df["compendium"] = compendium

        # Store clinical dataset
        clinical_datasets.append(clinical_df)

    # Merge all clinical datasets into a single DataFrame
    compendia_df = pd.concat(clinical_datasets)

    return compendia_df

