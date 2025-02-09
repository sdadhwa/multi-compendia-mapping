#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
UMAP setup

This is the skeleton for UMAP integration.
'''
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from matplotlib.pyplot import plt
import seaborn as sns
import pandas as pd
import umap
get_ipython().run_line_magic('matplotlib', 'inline')

# Map seaborn for plotting
sns(style="white", context = 'poster', rc={'figure.figsize':(14,10)})

# TODO Import csv data for ALL compendiums

# Use umap library and initiate class
reducer = umap.UMAP()

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

# Ensure correct data merging
merged_data = pd.merge(df_expr, df_clinical, left_index=True, right_index=True)

# Define metada columns
# TODO: adjust colums (add? remove?)
metadata_columns = [
    "Compendium",
    "SampleType",
    "TumorType"
]

# Extract numerical gene expression values
expression_data = df_expr.drop(columns=metadata_cols)  # Gene expression only
metadata = df_expr[metadata_cols] # Store metadata separately

# Drop missing values if needed
expression_data = expression_data.dropna()

# Standardize expression data
scaler = StandardScaler()
expression_scaled = scaler.fit_transform(expression_data)

# Perform UMAP dimensionality reduction
reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric="correlation", random_state=42)
embedding = reducer.fit_transform(expression_scaled)

# Create a DataFrame for the UMAP results
df_umap = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"], index=expression_data.index)
df_umap["Compendium"] = metadata["Compendium"] # Add compendium labels
df_umap["SampleType"] = metadata["SampleType"] # Add sample type labels
df_umap["TumorType"] = metadata["TumorType"] # Add tumor type labels

# Plot UMAP results
plt.figure(figsize=(10, 6))
sns.scatterplot(x="UMAP1", y="UMAP2", hue="Compendium", data=df_umap, palette="tab10")
plt.title("UMAP Projection of Filtered RNA-seq Data")
plt.legend(bbox_to_anchor=(1, 1))
plt.show()

# TODO: modify n_neighbors and min_dist to see how it affects the map
# and how it affects the clustering of samples

# Possible test:
# reducer = umap.UMAP(n_components=2, n_neighbors=30, min_dist=0.2, metric="correlation", random_state=42)
# embedding = reducer.fit_transform(expression_scaled)

