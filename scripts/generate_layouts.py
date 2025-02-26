import sys
import os
from matplotlib import pyplot as plt
import pandas as pd
import umap
from layout_algorithms.mcm_umap import MCMUmap
from preprocessing import process_expression_compendium, process_clinical_compendium
from process_data import clinical_dict, expression_dict

# TODO Import csv data for ALL compendiums

'''
Label data points based on compendium of origin for
adding labels to data points for each compendium in the map
'''

# All tsv files for expression and clinical data
expression_file = expression_dict["expression_tsv"]
clinical_file = clinical_dict["clinical_tsv"]

# Load expression data into DataFrame
df_expr = pd.read_csv(expression_file, sep="\t", index_col=0)
print(f"Expression data shape: {df_expr.shape}")

# Load clinical data into DataFrame
df_clinical = pd.read_csv(clinical_file, sep="\t", index_col=0)
print(f"Clinical data shape: {df_clinical.shape}")

compressed_df = MCMUmap().fit_transform(df_expr, df_clinical)

# UMAP Utility Function for testing
# TODO: Write more tests with different neighbors and distance values
def draw_umap(data, n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean', title=''):
    fit = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        metric=metric
    )
    u = fit.fit_transform(data)
    fig = plt.figure()
    if n_components == 1:
        ax = fig.add_subplot(111)
        ax.scatter(u[:,0], range(len(u)), c=data)
    if n_components == 2:
        ax = fig.add_subplot(111)
        ax.scatter(u[:,0], u[:,1], c=data)
    if n_components == 3:
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(u[:,0], u[:,1], u[:,2], c=data, s=100)
    plt.title(title, fontsize=18)
    plt.show()

# UMAP visualization tests - replace numbers above with these numbers
# n_neighbors values: 5, 15, 30
# min_dist values: 0.1, 0.25, 0.5  
# n_components values: 1, 2, 3
# metric values: 'euclidean', 'correlation' --> most likely will use euclidean
# but it would be cool to see what correlation looks like, maybe it fits our data better or not?