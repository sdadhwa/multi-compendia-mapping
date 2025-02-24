from abc import ABC

from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap
from .base_layout import BaseLayout
from IPython import get_ipython


class MCMUmap(BaseLayout):

    def fit_transform(self, expression_df, clinical_df):
        '''
        UMAP setup

        This is the skeleton for UMAP integration.
        '''

        get_ipython().run_line_magic('matplotlib', 'inline')

        # Map seaborn for plotting
        sns(style="white", context='poster', rc={'figure.figsize': (14, 10)})

        # Use umap library and initiate class
        reducer = umap.UMAP()

        # Ensure correct data merging
        merged_data = pd.merge(expression_df, clinical_df, left_index=True, right_index=True)

        # Define metada columns
        # TODO: adjust colums (add? remove?)
        metadata_columns = [
            "Compendium",
            "SampleType",
            "TumorType"
        ]

        # Extract numerical gene expression values
        expression_data = expression_df.drop(columns=metadata_columns)  # Gene expression only
        metadata = clinical_df[metadata_columns]  # Store metadata separately

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
        df_umap["Compendium"] = metadata["Compendium"]  # Add compendium labels
        df_umap["SampleType"] = metadata["SampleType"]  # Add sample type labels
        df_umap["TumorType"] = metadata["TumorType"]  # Add tumor type labels

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

