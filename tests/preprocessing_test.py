import pandas as pd
from src.preprocessing import process_expression_compendium
import pytest

@pytest.fixture
def expression_dict():
    patients1 = ["Patient_A", "Patient_B", "Patient_C"]
    patients2 = ["Patient_D", "Patient_E", "Patient_F"]

    data1 = {
        "gene_1": [5.2, 4.8, 5.0],
        "gene_2": [3.1, 2.9, 3.0],
        "gene_3": [7.4, 6.8, 7.0],
        "gene_4": [1.0, 1.1, 1.2],
        "gene_5": [2.0, 2.1, 2.2],
        "gene_6": [3.0, 3.1, 3.2],
        "gene_7": [4.0, 4.1, 4.2],
        "gene_8": [5.0, 5.1, 5.2],
        "gene_9": [6.0, 6.1, 6.2],
        "gene_10": [7.0, 7.1, 7.2]
    }

    data2 = {
        "gene_1": [5.1, 4.9, 5.0],
        "gene_2": [3.2, 2.8, 3.1],
        "gene_3": [7.2, 6.9, 7.1],
        "gene_4": [1.1, 1.0, 1.2],
        "gene_5": [2.1, 2.0, 2.2],
        "gene_6": [3.1, 3.0, 3.2],
        "gene_7": [4.1, 4.0, 4.2],
        "gene_8": [5.1, 5.0, 5.2],
        "gene_9": [6.1, 6.0, 6.2],
        "gene_10": [7.1, 7.0, 7.2]
    }

    df1 = pd.DataFrame(data1, index=patients1)
    df2 = pd.DataFrame(data2, index=patients2)

    expression_dict = {
        "compendium1": df1,
        "compendium2": df2
    }

    return expression_dict

def test_format_process_expression_compendium(expression_dict):
    """
    Test the process_expression_compendium function to ensure it concatenates two compendia into one returns a
    DataFrame with the expected format.
    """

    # Call the function to test
    processed_compendium = process_expression_compendium(expression_dict)

    # The processed compendium should have one column "compendium" and 10 gene columns. Index column doesn't get counted.
    # 6 samples so should have 6 rows
    assert processed_compendium.shape == (6, 11)

    # Check that the indexes are the same as the patient IDs
    patients = ["Patient_A", "Patient_B", "Patient_C", "Patient_D", "Patient_E", "Patient_F"]
    assert all(patient in processed_compendium.index for patient in patients)
    assert "compendium" in processed_compendium.columns
    for i in range(1, 11):
        assert f"gene_{i}" in processed_compendium.columns

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

def test_min_var_process_expression_compendium():
    """
    Test the variance_threshold argument of the process_expression_compendium function to ensure it filters out genes
    with variance below the threshold.
    """