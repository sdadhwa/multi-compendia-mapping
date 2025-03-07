from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import umap

class BaseLayout(ABC):
    """
    API for layout algorithms. To make a new layout algorithm, inherit from this class and implement the fit_transform
    method.
    """

    @abstractmethod
    def fit_transform(self, expression_df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform a layout algorithm on the given dataframe. Examples TSNE, PCA, UMAP. The input should be high
        dimensional gene expression data and the output should be a 2D representation of the data.

        Parameters:
        expression_df (pd.DataFrame): The gene expression data. All columns should be genes and all rows should be
            samples. The index should be the sample ids. There should be no missing values (NaNs). All samples
            should have the same genes.

        Returns:
        pd.DataFrame: This dataframe should have dimension 2. The index should be the sample ids.
        """
        pass
