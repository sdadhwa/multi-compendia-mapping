import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import umap
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
    
    # Load clinical data and merge with expression dataframe
    clinical_df = pd.read_csv(config.clinical_file_path(), sep="\t", index_col=0)
    umap_df = layout_df.merge(clinical_df, left_index=True, right_index=True, how='inner')

    # Map seaborn for plotting
    sns(style="white", context='poster', rc={'figure.figsize': (14, 10)})

    def draw_umap(data, n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean', title=''):
        u = umap_df
        fig = plt.figure()
        if n_components == 1:
            ax = fig.add_subplot(111)
            ax.scatter(u[:,0], range(len(u)), c=data)
        if n_components == 2:
            ax = fig.add_subplot(111)
            ax.scatter(u[:,0], u[:,1], c=data)
        if n_components == 3:
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(u[:,0], u[:,1], u[:,2], c=data, s=100)
        plt.title(title, fontsize=18)
        plt.show()