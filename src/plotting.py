import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns

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

def add_scatter_plots(ax, data: pd.DataFrame, label_column: str):
    """
    Add scatter plots to the axes for each unique label in the specified column.

    Parameters:
        ax (matplotlib.axes.Axes): The axes to add the scatter plots to.
        data (pd.DataFrame): The data containing the plotting coordinates and labels.
        label_column (str): The column name containing the labels.

    Returns:
        dict: A dictionary mapping each label to its corresponding scatter plot object.
    """
    scatter_objects = {}
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

def generate_compendium_plot(data: pd.DataFrame, title: str):
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
