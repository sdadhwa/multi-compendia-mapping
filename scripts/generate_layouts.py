import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.layout_algorithms import MCMUmap

# TODO Import csv data for ALL compendiums

'''
Label data points based on compendium of origin for
adding labels to data points for each compendium in the map
'''

# Expression data compendias by name
expression_files = {
    "Tumor_polyA": "data/Tumor_polyA_TPM.tsv",
    "Tumor_rRNA": "data/Tumor_rRNA_TPM.tsv",
    "CellLine_polyA": "data/CellLine_polyA_TPM.tsv",
    "PDX_polyA": "data/PDX_polyA_TPM.tsv",
    "PDX_rRNA": "data/PDX_rRNA_TPM.tsv",
}

# Clinical data compendias by name
clinical_files = {
    "Tumor_polyA": "data/Tumor_polyA_Clinical.tsv",
    "Tumor_rRNA": "data/Tumor_rRNA_Clinical.tsv",
    "CellLine_polyA": "data/CellLine_polyA_Clinical.tsv",
    "PDX_polyA": "data/PDX_polyA_Clinical.tsv",
    "PDX_rRNA": "data/PDX_rRNA_Clinical.tsv",
}

# Load in combined/merged and trimmed clinical and expression data
expression_file = "filtered_gene_expression.tsv"
df_expr = pd.read_csv(expression_file, sep="\t", index_col=0)

clinical_file = "filtered_clinical_data.tsv"
df_clinical = pd.read_csv(clinical_file, sep="\t", index_col=0)

compressed_df = MCMUmap().fit_transform(df_expr, df_clinical)