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
        
        sns.set_theme(style="white", context='poster', rc={'figure.figsize': (14, 10)})
        fig, ax = plt.subplots()

        # Create the scatter plot with the custom color palette
        scatter = sns.scatterplot(
            data=data, x='x', y='y', hue='compendium', ax=ax, s=100, alpha=0.3, edgecolors='none'
        )

        # Set the title
        ax.set_title(title)

        # Customize the legend
        ax.legend(title='Compendium', loc='center left', bbox_to_anchor=(1, 0.5), title_fontsize=14, fontsize=12)

        # Add a descriptive label for each color in the legend
        for line in scatter.legend_.get_lines():
            line.set_alpha(1)  # Set legend markers to full opacity

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.5)

        # Save and show the figure
        plt.tight_layout()
        return fig