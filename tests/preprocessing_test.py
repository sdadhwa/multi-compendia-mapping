import pandas as pd
from src.preprocessing import process_expression_compendium

def test_format_process_expression_compendium():
    """
    Test the process_expression_compendium function to ensure it concatenates two compendia into one returns a
    DataFrame with the expected format.
    """

    patients1 = ["Patient_A", "Patient_B", "Patient_C"]
    patients2 = ["Patient_D", "Patient_E", "Patient_F"]
    # Create a DataFrame with patient identifying strings as IDs
    expression_dict = {
        "compendium1": pd.DataFrame({
            "SampleID": patients1,
            "gene_1": [5.2, 4.8, 5.0],
            "gene_2": [3.1, 2.9, 3.0],
            "gene_3": [7.4, 6.8, 7.0],
            # Add more genes as needed
        }),
        "compendium2": pd.DataFrame({
            "SampleID": patients2,
            "gene_1": [5.1, 4.9, 5.0],
            "gene_2": [3.2, 2.8, 3.1],
            "gene_3": [7.2, 6.9, 7.1],
            # Add more genes as needed
        })
    }

    # Call the function to test
    processed_compendium = process_expression_compendium(expression_dict)

    # The processed compendium should have one column "SampleID", one column "compendium" and 3 gene columns.
    # There should be 6 rows in total.
    assert processed_compendium.shape == (6, 5)
    assert "SampleID" in processed_compendium.columns
    assert "gene_1" in processed_compendium.columns
    assert "gene_2" in processed_compendium.columns
    assert "gene_3" in processed_compendium.columns
    assert list(processed_compendium["SampleID"]) == patients1 + patients2

def test_min_exp_process_expression_compendium():
    """
    Test the min_expression argument of the process_expression_compendium function to ensure it filters out genes with
    mean expressions below the threshold.
    """
    expression_dict = {
        "compendium1": pd.DataFrame({
            "SampleID": ["Patient_A", "Patient_B", "Patient_C"],
            "gene_1": [1, 1, 1],
            "gene_2": [3, 3, 3],
            "gene_3": [2, 2, 2],
            "gene_4": [0, 0, 0],
        }),
        "compendium2": pd.DataFrame({
            "SampleID": ["Patient_D", "Patient_E", "Patient_F"],
            "gene_1": [1, 1, 1],
            "gene_2": [3, 3, 3],
            "gene_3": [2, 2, 2],
            "gene_4": [0, 0, 0],
        })
    }

    # Call the function to test
    mean_gene1 = expression_dict["compendium1"]["gene_1"].mean()
    mean_gene2 = expression_dict["compendium1"]["gene_2"].mean()
    mean_gene3 = expression_dict["compendium1"]["gene_3"].mean()
    mean_gene4 = expression_dict["compendium1"]["gene_4"].mean()

    # Make sure that gene 1 and gene 4 are filtered out if the minimum expression is set to the mean of gene 1
    assert mean_gene1 > mean_gene4
    assert mean_gene1 < mean_gene2 and mean_gene1 < mean_gene3

    processed_compendium = process_expression_compendium(expression_dict, minimum_expression=mean_gene1)

    # Processed compendium should not contain gene_4 or gene_1 columns
    assert "gene_1" not in processed_compendium.columns
    assert "gene_4" not in processed_compendium.columns