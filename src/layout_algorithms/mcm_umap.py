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
            pd.DataFrame: This dataframe should have dimension 2. The index should be the sample ids.
        """
        
        # Map seaborn for plotting
        sns.set_theme(style="white", context='poster', rc={'figure.figsize': (14, 10)})

        # Standardize expression data
        scaler = StandardScaler()
        expression_scaled = scaler.fit_transform(expression_df)

        # Perform UMAP dimensionality reduction
        reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric="correlation", random_state=42)
        embedding = reducer.fit_transform(expression_scaled)

        # Convert the embedding to a DataFrame
        embedding_df = pd.DataFrame(embedding, index=expression_df.index, columns=['UMAP1', 'UMAP2'])

        return embedding_df

