from abc import ABC, abstractmethod
import pandas as pd

class BaseLayout(ABC):
    """
    API for threshold algorithms.
    """

    @abstractmethod
    def fit_transform(self, expression_df: pd.DataFrame, clinical_df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform the layout algorithm on the given data.

        Parameters:
        expression_df (pd.DataFrame): The gene expression data.
        clinical_df (pd.DataFrame): The clinical data.

        Returns:
        pd.DataFrame: The transformed data with layout coordinates.
        """
        pass