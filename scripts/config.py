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

    def __init__(self):
        self.project_root = '..'
        self.data_dir = 'data'
        self.raw_data_dir = 'raw'
        self.processed_dir = 'processed'
        self.expression_file = 'processed_compendium.tsv'
        self.clinical_file = 'processed_clinical_data.tsv'
        self.expression_targets = {}
        self.clinical_targets = {}

    def data_dir_path(self):
        """
        Get the full path to the data directory.
        """
        return os.path.join(self.project_root, self.data_dir)

    def raw_data_dir_path(self):
        """
        Get the path to the raw data directory relative to the project root directory.
        """
        return os.path.join(self.data_dir_path(), self.raw_data_dir)

    def processed_dir_path(self):
        """
        Get the path to the processed data directory relative to the project root directory.
        """
        return os.path.join(self.data_dir_path(), self.processed_dir)

    def expression_file_path(self):
        """
        Get the path to the expression data file relative to the project root directory.
        """
        return os.path.join(self.processed_dir_path(), self.expression_file)

    def clinical_file_path(self):
        """
        Get the path to the expression data file relative to the project root directory.
        """
        return os.path.join(self.processed_dir_path(), self.clinical_file)

    def get_path_expression_url_targets(self):
        """
        Get a dictionary of file paths to URLs for downloading expression files.

        Returns:
            dict: A dictionary where keys are expression file paths and values are URLs.
        """
        return {os.path.join(self.raw_data_dir, file): url for file, url in self.expression_targets.items()}

    def get_path_clinical_url_targets(self):
        """
        Get a dictionary of file paths to URLs for downloading clinical files.

        Returns:
            dict: A dictionary where keys are clinical file paths and values are URLs.
        """
        return {os.path.join(self.raw_data_dir, file): url for file, url in self.clinical_targets.items()}

    def get_expression_file_paths(self):
        """
        Get a list of expression file paths.

        Returns:
            list: A list of expression file paths.
        """
        return [os.path.join(self.raw_data_dir, file) for file in self.expression_targets]

    def get_clinical_file_paths(self):
        """
        Get a list of clinical file paths.

        Returns:
            list: A list of clinical file paths.
        """
        return [os.path.join(self.raw_data_dir, file) for file in self.clinical_targets]