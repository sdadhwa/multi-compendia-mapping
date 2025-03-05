from matplotlib.figure import Figure
from sklearn.preprocessing import StandardScaler
import pandas as pd
import umap
from .base_layout import BaseLayout
import seaborn as sns

class MCMUmap(BaseLayout):

    def fit_transform(self, expression_df):
        """
        Perform UMAP layout algorithm on the given dataframe. This implementation uses the UMAP algorithm from the
        umap-learn library.

        Args:
            expression_df (pd.DataFrame): The gene expression data. All columns should be genes and all rows should be
                samples. The index should be the sample ids. There should be no missing values ie no NaNs. All samples
                should have the same genes.

        Returns:
            pd.DataFrame: This dataframe should have dimension 2. Sample Ids are the index and the columns are 'UMAP1'
                and 'UMAP2' representing the x and y coordinates of the UMAP embedding.

        """

        # Standardize expression data
        scaler = StandardScaler()
        expression_scaled = scaler.fit_transform(expression_df)

        # Perform UMAP dimensionality reduction
        reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric="correlation", random_state=42)
        embedding = reducer.fit_transform(expression_scaled)

        # Convert the embedding to a DataFrame
        embedding_df = pd.DataFrame(embedding, index=expression_df.index, columns=['x', 'y'])

        return embedding_df

    @classmethod
    def generate_plot(cls, data: pd.DataFrame, title: str) -> Figure:
        fig = super().generate_plot(data, title)
        ax = fig.get_axes()[0]

        # Adjust the axis labels specific to MCMUmap
        ax.set_xlabel("UMAP_1", fontsize=14)
        ax.set_ylabel("UMAP_2", fontsize=14)

        return fig