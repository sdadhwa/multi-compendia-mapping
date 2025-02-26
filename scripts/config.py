import os

class ScriptConfig:
    """
    Base configuration class. Do not use attributes to access file or directory paths directly. Instead, use methods
    provided. The attributes are meant to be overridden by subclasses for changes in file names or directory structure.
    The included methods build the full paths to files and directories based on the attributes which are safe to use
    in scripts.

    Attributes:
        project_root (str): The name of the project root directory.
        data_dir (str): The name of the data directory.
        raw_data_dir (str): The name of the raw data directory.
        processed_dir (str): The name of the processed data directory.
        expression_file (str): The name of the expression data file.
        clinical_file (str): The name of the clinical data file.
        expression_targets (dict): A dictionary for file targets of expression data. Keys should be the file name with
            proper extension and values should be the URL to download the file.
            Example: {"file_expression.tsv": "https://example.com/file_expression.tsv"}
        clinical_targets (dict): A dictionary for file targets of expression data. Keys should be the file name with
            proper extension and values should be the URL to download the file.
            Example: {"file_clinical.tsv": "https://example.com/file_clinical.tsv"}
    """

    project_root = '.'
    data_dir = 'data'
    raw_data_dir = 'raw'
    processed_dir = 'processed'
    expression_file = 'processed_compendium.tsv'
    clinical_file = 'processed_clinical_data.tsv'
    expression_targets = {}
    clinical_targets = {}

    @classmethod
    def data_dir_path(cls):
        """
        Get the full path to the data directory.
        """
        return os.path.join(cls.project_root, cls.data_dir)

    @classmethod
    def raw_data_dir_path(cls):
        """
        Get the path to the raw data directory relative to the project root directory.
        """
        return os.path.join(cls.data_dir_path(), cls.raw_data_dir)

    @classmethod
    def processed_dir_path(cls):
        """
        Get the path to the processed data directory relative to the project root directory.
        """
        return os.path.join(cls.data_dir_path(), cls.processed_dir)

    @classmethod
    def expression_file_path(cls):
        """
        Get the path to the expression data file relative to the project root directory.
        """
        return os.path.join(cls.processed_dir_path(), cls.expression_file)

    @classmethod
    def clinical_file_path(cls):
        """
        Get the path to the expression data file relative to the project root directory.
        """
        return os.path.join(cls.processed_dir_path(), cls.clinical_file)

    @classmethod
    def get_path_expression_url_targets(cls):
        """
        Get a dictionary of file paths to URLs for downloading expression files.

        Returns:
            dict: A dictionary where keys are expression file paths and values are URLs.
        """
        return {os.path.join(cls.raw_data_dir, file): url for file, url in cls.expression_targets.items()}

    @classmethod
    def get_path_clinical_url_targets(cls):
        """
        Get a dictionary of file paths to URLs for downloading clinical files.

        Returns:
            dict: A dictionary where keys are clinical file paths and values are URLs.
        """
        return {os.path.join(cls.raw_data_dir, file): url for file, url in cls.clinical_targets.items()}

    @classmethod
    def get_expression_file_paths(cls):
        """
        Get a list of expression file paths.

        Returns:
            list: A list of expression file paths.
        """
        return [os.path.join(cls.raw_data_dir, file) for file in cls.expression_targets]

    @classmethod
    def get_clinical_file_paths(cls):
        """
        Get a list of clinical file paths.

        Returns:
            list: A list of clinical file paths.
        """
        return [os.path.join(cls.raw_data_dir, file) for file in cls.clinical_targets]

class ProductionConfig(ScriptConfig):

    expression_targets = {
        "tumor_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv",
        "tumor_ribo_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/TreehousePEDv9_Ribodeplete_unique_hugo_log2_tpm_plus_1.2019-03-25.tsv",
        "cell_line_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/CellLinePolyA_21.06_hugo_log2tpm_58581genes_2021-06-15.tsv",
        "PDX_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-PolyA_for_GEO_20240520.tsv",
        "PDX_ribo_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-Ribodeplete_for_GEO_20240520.tsv"
    }

    clinical_targets = {
        "tumor_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_TumorCompendium_v11_PolyA_for_GEO_20240520.tsv",
        "tumor_ribo_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/Treehouse-PDX-Compendium-22.03-PolyA_hugo_log2tpm_58581genes_2022-03-09.tsv",
        "cell_line_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_CellLinePolyA_21.06_for_GEO_20240520.tsv",
        "PDX_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-PolyA_for_GEO_20240520.tsv",
        "PDX_ribo_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-Ribodeplete_for_GEO_20240520.tsv"
    }

class PDX_PolyA(ScriptConfig):
    """
    Configuration for only PDX\_polyA data. This is useful for testing and development for a single compendium and
    no compendium merging.
    """

    data_dir = 'data/pdx_polya'
    expression_targets = {
        "PDX_polyA_expression.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-PolyA_for_GEO_20240520.tsv",
    }

    clinical_targets = {
        "PDX_polyA_clinical.tsv": "https://xena.treehouse.gi.ucsc.edu/download/clinical_Treehouse-PDX-Compendium-22.03-PolyA_for_GEO_20240520.tsv",
    }

VALID_CONFIGS = ["production", "pdx_polya"]

def get_config(config_name):
    """
    Returns the appropriate configuration class based on the provided command line argument.

    Args:
        config_name (str): The name of the configuration to use. Available options are:
            - "production": Use the ProductionConfig class.
            - "pdx_polya": Use the PDX_PolyA class.

    Returns:
        ScriptConfig: The configuration class corresponding to the provided name, or None if an invalid configuration name is provided.

    Prints:
        str: An error message if an invalid configuration name is provided.
    """
    if config_name == "production":
        return ProductionConfig
    elif config_name == "pdx_polya":
        return PDX_PolyA
    else:
        print(f"Invalid configuration name: {config_name}. Valid configurations are: {', '.join(VALID_CONFIGS)}")
        return None