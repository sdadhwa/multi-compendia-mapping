import pandas as pd
import numpy as np

def process_expression_compendium(expression_dict, variance_threshold=None, minimum_expression=None):
    """
    Build a single data frame out of multiple gene expression data frames. If specified, remove genes with low variance
    and/or low expression. When trying to do both, minimum_expression is applied first and then variance_threshold.

    Args:
        expression_dict (dict): Dictionary where keys are compendium names and values are numpy dataframes containing
            gene expression data. Each column is a gene and each row is a sample.
        variance_threshold (int): What percentile of low variance genes to remove. Default None, no filtering.
        minimum_expression (float): The threshold for minimum expression. Units: mean log2(TPM+1). Default None, no
            filtering.
    """

    # Add a column to each dataframe with the compendium name
    compendium_labeled_dfs = []
    for compendium_name, df in expression_dict.items():
        df["compendium"] = compendium_name
        compendium_labeled_dfs.append(df)

    # Concatenate all dataframes into a single dataframe
    exp_df = pd.concat(expression_dict.values())

    # Separate non-numeric columns
    non_numeric_columns = exp_df.select_dtypes(exclude=[np.number]).columns
    non_numeric_data = exp_df[non_numeric_columns]

    # Process numeric columns (genes) only
    numeric_columns = exp_df.select_dtypes(include=[np.number])

    # Remove genes with very low expression
    if minimum_expression is not None:
        gene_means = numeric_columns.mean()
        genes_to_keep = gene_means > minimum_expression
        numeric_columns = numeric_columns.loc[:, genes_to_keep]

    # Remove genes with the lowest variance
    if variance_threshold is not None:
        gene_variances = numeric_columns.var()
        genes_to_keep = gene_variances > np.percentile(gene_variances, variance_threshold)
        numeric_columns = numeric_columns.loc[:, genes_to_keep]

    filtered_exp_df = pd.concat([non_numeric_data, numeric_columns], axis=1)
    return filtered_exp_df


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

