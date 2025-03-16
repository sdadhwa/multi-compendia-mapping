import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns

"""
This module provides functions for generating and customizing scatter plots using Matplotlib and Seaborn. The plots can
be color-coded based on different categories such as compendium of origin or type of disease. The module includes
functions to set up plots, add scatter plots, customize legends, and handle interactive legend clicks for toggling
scatter plot visibility.

Functions:
    setup_plot(title: str) -> tuple:
        Set up the plot with the given title and return the figure and axes objects.

    add_scatter_plots(ax, data: pd.DataFrame, label_column: str, unique_labels: list = None) -> dict:
        Add scatter plots to the axes for each unique label in the specified column and return a dictionary mapping each
        label value to its corresponding scatter plot object.

    customize_legend(ax, scatter_objects: dict) -> tuple:
        Customize the legend for the scatter plots and return the legend and a dictionary mapping legend text to scatter
        objects.

    on_legend_click(event, legend_items: dict, fig: Figure):
        Callback for pick_event to toggle visibility of the scatter plot corresponding to the clicked legend text.

    generate_compendium_plot(data: pd.DataFrame, title: str) -> Figure:
        Generate a scatter plot color-coded by compendium of origin and return the plot figure.

    generate_disease_plot(data: pd.DataFrame, title: str) -> Figure:
        Generate a scatter plot color-coded by type of disease and return the plot figure.
"""

def setup_plot(title: str):
    """
    Set up the plot with the given title.

    Parameters:
        title (str): The title of the plot.

    Returns:
        tuple: A tuple containing the figure and axes objects.
    """
    sns.set_theme(style="white", context='poster', rc={'figure.figsize': (14, 10)})
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig, ax

def add_scatter_plots(ax, data: pd.DataFrame, label_column: str, unique_labels: list = None):
    """
    Add scatter plots to the axes for each unique label in the specified column.

    Parameters:
        ax (matplotlib.axes.Axes): The axes to add the scatter plots to.
        data (pd.DataFrame): The data containing the plotting coordinates and labels.
        label_column (str): The column name containing the labels.
        unique_labels (list): A list of unique labels to plot. If None, all unique labels in the data will be plotted.

    Returns:
        dict: A dictionary mapping each label to its corresponding scatter plot object.
    """
    scatter_objects = {}
    if unique_labels is None:
        unique_labels = data[label_column].unique()
    for label in unique_labels:
        subset = data[data[label_column] == label]
        scatter = ax.scatter(subset['x'], subset['y'], s=100, alpha=1.0, edgecolors='none', label=label)
        scatter_objects[label] = scatter
    return scatter_objects

def customize_legend(ax, scatter_objects):
    """
    Customize the legend for the scatter plots.

    Parameters:
        ax (matplotlib.axes.Axes): The axes containing the scatter plots.
        scatter_objects (dict): A dictionary mapping each label to its corresponding scatter plot object.

    Returns:
        tuple: A tuple containing the legend and a dictionary mapping legend text to scatter objects.
    """
    legend = ax.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.5), title_fontsize=14, fontsize=12)
    # Map legend text to scatter objects
    legend_items = {text.get_text(): scatter_objects[text.get_text()] for text in legend.get_texts()}
    return legend, legend_items

def on_legend_click(event, legend_items, fig):
    """
    Callback for pick_event to toggle visibility of the scatter plot corresponding to the clicked legend text.

    Parameters:
        event (matplotlib.backend_bases.PickEvent): The pick event.
        legend_items (dict): A dictionary mapping legend text to scatter objects.
        fig (matplotlib.figure.Figure): The figure containing the plot.
    """

    # The Matplotlib artist that was clicked (e.g., a line, scatter plot, etc.)
    # Check if the artist is a Text object
    artist = event.artist
    if isinstance(artist, plt.Text):
        # Get the text of the artist. Check if the text is a label name corresponding to a scatter.
        artist_text = artist.get_text()
        if artist_text in legend_items:
            scatter_obj = legend_items[artist_text]
            scatter_obj.set_alpha(0 if scatter_obj.get_alpha() == 1 else 1)
            artist.set_alpha(1 if scatter_obj.get_alpha() == 1 else 0.3)
            fig.canvas.draw_idle()

def generate_compendium_plot(data: pd.DataFrame, title: str) -> Figure:
    """
    Generate a plot which color codes by compendium of origin. This method creates a scatter plot for each unique
    compendium in the data. It maps each compendium name to its corresponding scatter plot object, allowing for
    interactive toggling of scatter plot visibility via legend clicks.

    Parameters:
        data (pd.DataFrame): The layout data. The index should be the sample ids. The columns holding plotting
            coordinates should be 'x' and 'y'. There needs to be a column 'compendium' that holds the compendium of
            origin for each sample.
        title (str): The title of the plot.

    Returns:
        Figure: The plot figure.
    """

    fig, ax = setup_plot(title)
    scatter_objects = add_scatter_plots(ax, data, 'compendium')
    legend, legend_items = customize_legend(ax, scatter_objects)

    fig.canvas.mpl_connect("pick_event", lambda event: on_legend_click(event, legend_items, fig))
    for text in legend.get_texts():
        text.set_picker(True)

    plt.tight_layout()
    return fig

def generate_disease_plot(data: pd.DataFrame, title: str) -> Figure:
    """
    Generate a plot where color codes for type of disease.

    Args:
        data (pd.DataFrame): The layout data. The index should be the sample ids. The columns holding plotting
            coordinates should be 'x' and 'y'. There needs to be a column 'disease' that holds the type of disease for
            each sample.
        title (str): The title of the plot.

    Returns:
        Figure: The plot figure.
    """
    label_column = 'disease'

    # Convert the disease labels to lowercase
    data[label_column] = data[label_column].str.lower()

    # Count the occurrences of each disease
    disease_counts = data[label_column].value_counts()

    # Get the top 10 most common diseases
    top_10_diseases = disease_counts.nlargest(9).index.tolist()
    top_10_diseases.append('unknown')

    fig, ax = setup_plot(title)
    scatter_objects = add_scatter_plots(ax, data, 'disease', top_10_diseases)
    legend, legend_items = customize_legend(ax, scatter_objects)

    fig.canvas.mpl_connect("pick_event", lambda event: on_legend_click(event, legend_items, fig))
    for text in legend.get_texts():
        text.set_picker(True)

    plt.tight_layout()
    return fig
