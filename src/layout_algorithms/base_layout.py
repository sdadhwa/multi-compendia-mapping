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

        # Dictionary to store scatter plot objects
        scatter_objects = {}

        unique_compendia = data['compendium'].unique()
        for compendium in unique_compendia:
            subset = data[data['compendium'] == compendium]
            scatter = ax.scatter(subset['x'], subset['y'], s=100, alpha=1.0, edgecolors='none', label=compendium)
            scatter_objects[compendium] = scatter

        # Set the title
        ax.set_title(title)

        # Set the grid
        ax.grid(True, linestyle='--', alpha=0.5)

        # Customize the legend
        legend = ax.legend(title='Compendium', loc='center left', bbox_to_anchor=(1, 0.5), title_fontsize=14, fontsize=12)

        # Map legend text to scatter objects
        legend_items = {text.get_text(): scatter_objects[text.get_text()] for text in legend.get_texts()}

        def on_legend_click(event):
            """
            Toggle visibility of the scatter plot corresponding to the clicked legend text.
            """
            artist = event.artist   # The Matplotlib artist that was clicked (e.g., a line, scatter plot, etc.)
            # Check if the artist is a Text object
            if isinstance(artist, plt.Text):
                artist_text = artist.get_text()  # Get the text of the artist
                # Check if the text is a compendium name corresponding to a scatter.
                if artist_text in legend_items:
                    scatter_obj = legend_items[artist_text]
                    scatter_obj.set_alpha(0 if scatter_obj.get_alpha() == 1 else 1)  # Toggle between 0 and 1
                    artist.set_alpha(1 if scatter_obj.get_alpha() == 1 else 0.3)  # Dim legend text if hidden
                    fig.canvas.draw_idle()  # Refresh the plot

        # Connect event listener
        fig.canvas.mpl_connect("pick_event", lambda event: on_legend_click(event))

        # Set picker property for legend text. This ensures that the legend fires a pick_event when clicked.
        for text in legend.get_texts():
            text.set_picker(True)

        # Save and show the figure
        plt.tight_layout()
        return fig
