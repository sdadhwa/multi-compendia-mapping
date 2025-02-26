import pandas as pd
import numpy as np

def process_expression_compendium(expression_dict, variance_threshold=None, minimum_expression=None):
    """
    Build a single data frame out of multiple gene expression data frames. If specified, remove genes with low variance
    and/or low expression. When trying to do both, minimum_expression is applied first and then variance_threshold. Some
    dataframes may have different genes, in which case the union of all genes is taken and missing values are filled
    with 0.

    Ex. If only one sample has expression data for gene A, all the other samples will have 0 expression values for gene
    A set, even if those samples did not collect data for gene A. This will reduce the variance and mean expression
    overall for gene A, which means it is more likely to be filtered out. This behavior is desirable because it ensures
    that genes that have expression data across more samples are prioritized in being kept when applying filters.

    Args:
        expression_dict (dict): Dictionary where keys are compendium names and values are numpy dataframes containing
            gene expression data. Each column is a gene and each row is a sample.
        variance_threshold (int): What percentile of low variance genes to remove. Default None, no filtering.
        minimum_expression (float): The threshold for minimum expression exclusive. Units: mean log2(TPM+1). Default None, no
            filtering.

    Returns:
        pd.DataFrame: A single dataframe containing all patient ids and corresponding gene expression data from all
            inputted compendia.
    """

    # Add a column to each dataframe with the compendium name
    compendium_labeled_dfs = []
    for compendium_name, df in expression_dict.items():
        compendium_labeled_dfs.append(df)

    # Concatenate all dataframes into a single dataframe
    exp_df = pd.concat(expression_dict.values())

    # Replace any NaN values with 0. This is necessary because some dataframes may have different genes.
    # Replacing with 0 will factor into calculating variance and mean expression for filtering.
    exp_df = exp_df.fillna(0)

    # Remove genes with very low expression
    if minimum_expression is not None:
        gene_means = exp_df.mean()
        genes_to_keep = gene_means > minimum_expression
        exp_df = exp_df.loc[:, genes_to_keep]

    # Remove genes with the lowest variance
    if variance_threshold is not None:
        gene_variances = exp_df.var()
        genes_to_keep = gene_variances > np.percentile(gene_variances, variance_threshold)
        exp_df = exp_df.loc[:, genes_to_keep]

    filtered_exp_df = exp_df
    return filtered_exp_df


def process_clinical_compendium(clinical_dict):
    """
    Process a dictionary of clinical dataframes and return a compendium dataframe.

    Args:
        clinical_dict (dict): Dictionary where keys are compendium names and values are dataframes containing clinical data.

    Returns:
        pd.DataFrame: Compendia dataframe with clinical data and added 'compendium' column label that marks the
        compendium of origin.
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

