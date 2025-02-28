from abc import ABC, abstractmethod
import pandas as pd
from matplotlib.pyplot import Figure
import seaborn as sns

class BaseLayout(ABC):
    """
    API for threshold algorithms. To make a new layout algorithm, inherit from this class and implement the fit_transform
    method.
    """

    @abstractmethod
    def fit_transform(self, expression_df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform a layout algorithm on the given dataframe. Examples TSNE, PCA, UMAP. The input should be high
        dimensional gene expression data and the output should be a 2D representation of the data.

        Parameters:
        expression_df (pd.DataFrame): The gene expression data. All columns should be genes and all rows should be
            samples. The index should be the sample ids. There should be no missing values ie no NaNs. All samples
            should have the same genes.

        Returns:
        pd.DataFrame: This dataframe should have dimension 2. The index should be the sample ids.
        """
        pass

    @classmethod
    def generate_plot(cls, data: pd.DataFrame, title: str) -> Figure:
        """
        Generate a plot of the data from the fit_transform method.

        Parameters:
        data (pd.DataFrame): The layout data. The index should be the sample ids. The columns holding plotting
            coordinates should be 'x' and 'y'. There needs to be a column 'compendium' that holds the compendium of
            origin for each sample.
        title (str): The title of the plot.

        Returns:
            Figure: The plot figure.
        """
        pass