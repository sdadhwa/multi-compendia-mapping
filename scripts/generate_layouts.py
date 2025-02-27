import pandas as pd
import argparse
import matplotlib.pyplot as plt
from layout_algorithms.mcm_umap import MCMUmap
from config import ScriptConfig, get_config, VALID_CONFIGS

if __name__ == '__main__':
    # Command line argument parsser to get configuration
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

    # Load expression data
    expression_df = pd.read_csv(config.expression_file_path(), sep="\t", index_col=0)

    layout_algorithm = MCMUmap()

    # Perform layout algorithm
    layout_df = layout_algorithm.fit_transform(expression_df)

    # Assuming layout_df has columns 'UMAP1' and 'UMAP2'
    plt.figure(figsize=(10, 6))
    plt.scatter(layout_df['UMAP1'], layout_df['UMAP2'], s=10, alpha=0.7)
    plt.title('UMAP Layout')
    plt.xlabel('UMAP1')
    plt.ylabel('UMAP2')
    plt.grid(True)
    plt.show()

    pass
