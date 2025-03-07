import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os
import logging
from layout_algorithms.mcm_umap import MCMUmap
from config import get_config, VALID_CONFIGS
from plotting import generate_compendium_plot, generate_disease_plot

# Set the interactive backend for Matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == '__main__':
    logging.info("Starting UMAP layout generation process...")

    # Command line argument parser to get configuration
    parser = argparse.ArgumentParser(description="Process genomic data files.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help=f"Configuration name (e.g., {', '.join(VALID_CONFIGS)})"
    )
    args = parser.parse_args()

    # Get configuration
    config = get_config(args.config)
    logging.info(f"Using configuration: {args.config}")

    # Load expression data
    logging.info("Loading expression data...")
    expression_df = pd.read_csv(config.expression_file_path(), sep="\t", index_col=0)

    # File format is (gene, sample). Layout algorithms expect (sample, gene)
    expression_df = expression_df.T
    logging.info(f"Expression data loaded: {expression_df.shape[0]} samples, {expression_df.shape[1]} genes.")

    # Initialize layout algorithm
    layout_algorithm = MCMUmap()

    # Perform layout algorithm
    logging.info("Performing UMAP dimensionality reduction...")
    layout_df = layout_algorithm.fit_transform(expression_df)
    logging.info("UMAP transformation complete.")

    # Load clinical data and merge with expression dataframe
    logging.info("Loading clinical data...")
    clinical_df = pd.read_csv(config.clinical_file_path(), sep="\t", index_col=0)
    umap_df = layout_df.merge(clinical_df, left_index=True, right_index=True, how='inner')
    logging.info(f"Clinical data merged: {umap_df.shape[0]} total samples.")

    # Generate UMAP figure using the method defined above
    logging.info("Generating UMAP plot...")

    disease_fig = generate_disease_plot(umap_df, "UMAP Disease Plot")
    compendium_fig = generate_compendium_plot(umap_df, "UMAP Compendium Plot")

    # Show the figure
    plt.show()

    # Save the figure
    os.makedirs(config.get_vis_dir_path(), exist_ok=True)
    disease_fig_path = config.gen_figure_file_path("umap-disease.png")
    disease_fig.savefig(disease_fig_path, dpi=300, bbox_inches='tight')

    compendium_fig_path = config.gen_figure_file_path("umap-compendium.png")
    compendium_fig.savefig(compendium_fig_path, dpi=300, bbox_inches='tight')

    logging.info(f"UMAP figure saved at: {disease_fig_path}")
