from abc import ABC

from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap
from .base_layout import BaseLayout
from IPython import get_ipython
from preprocessing import process_expression_compendium, process_clinical_compendium

class MCMUmap(BaseLayout):

    def fit_transform(self, expression_df):
        '''
        UMAP setup

        This is the skeleton for UMAP integration.
        '''
        
        # Map seaborn for plotting
        sns.set_theme(style="white", context='poster', rc={'figure.figsize': (14, 10)})

        # Use umap library and initiate class
        reducer = umap.UMAP()

        # Ensure correct data merging
        merged_data = pd.merge(expression_df, left_index=True, right_index=True)

        # Drop missing values if needed
        merged_data = merged_data.dropna()

        # Standardize expression data
        scaler = StandardScaler()
        expression_scaled = scaler.fit_transform(merged_data)

        # Perform UMAP dimensionality reduction
        reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric="correlation", random_state=42)
        embedding = reducer.fit_transform(expression_scaled)

        # TODO: modify n_neighbors and min_dist to see how it affects the map
        # and how it affects the clustering of samples

        # Possible test:
        # reducer = umap.UMAP(n_components=2, n_neighbors=30, min_dist=0.2, metric="correlation", random_state=42)
        # embedding = reducer.fit_transform(expression_scaled)

