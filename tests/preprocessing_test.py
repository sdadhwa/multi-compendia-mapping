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
        "gene_3": [7.5, 6.7, 7.0],
        "gene_4": [1.0, 1.2, 1.3],
        "gene_5": [2.2, 1.9, 2.4],
        "gene_6": [3.0, 3.1, 3.4],
        "gene_7": [4.0, 4.2, 4.5],
        "gene_8": [5.0, 5.1, 5.3],
        "gene_9": [6.0, 6.3, 6.6],
        "gene_10": [7.0, 7.4, 7.8]
    }

    data2 = {
        "gene_1": [5.1, 4.9, 5.0],
        "gene_2": [3.2, 2.8, 3.1],
        "gene_3": [7.2, 6.9, 7.1],
        "gene_4": [1.1, 1.0, 1.3],
        "gene_5": [2.1, 2.0, 2.5],
        "gene_6": [3.1, 3.0, 3.5],
        "gene_7": [4.1, 4.0, 4.4],
        "gene_8": [5.1, 5.0, 5.2],
        "gene_9": [6.1, 6.0, 6.4],
        "gene_10": [7.1, 7.0, 7.5]
    }

    df1 = pd.DataFrame(data1, index=patients1)
    df2 = pd.DataFrame(data2, index=patients2)

    expression_dict = {
        "compendium1": df1,
        "compendium2": df2
    }

    return expression_dict

def verify_processed_compendium(processed_compendium):
    """
    Verify that the processed compendium has the expected format for patient IDs and compendium column. These should
    never be removed or altered by functionality the processing function. This function should be called after
    doing processing on the expression_dict fixture.
    """
    patients = ["Patient_A", "Patient_B", "Patient_C", "Patient_D", "Patient_E", "Patient_F"]
    assert all(patient in processed_compendium.index for patient in patients)
    assert "compendium" in processed_compendium.columns

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
    verify_processed_compendium(processed_compendium)
    for i in range(1, 11):
        assert f"gene_{i}" in processed_compendium.columns

def test_min_exp_process_expression_compendium(expression_dict):
    # Calculate the mean expressions for each gene
    mean_expressions = pd.concat(expression_dict.values()).mean()

    # Determine the two genes with the lowest mean expressions
    lowest_mean_genes = mean_expressions.nsmallest(2).index

    # Call the function to test with the minimum expression set to the highest mean of the two lowest mean genes
    minimum_expression = mean_expressions[lowest_mean_genes].max()
    processed_compendium = process_expression_compendium(expression_dict, minimum_expression=minimum_expression)

    # Processed compendium should not contain the two genes with the lowest mean expressions
    for gene in lowest_mean_genes:
        assert gene not in processed_compendium.columns

    # Processed compendium should still contain all other genes
    for gene in mean_expressions.index:
        if gene not in lowest_mean_genes:
            assert gene in processed_compendium.columns

    # Make sure structure is still correct
    verify_processed_compendium(processed_compendium)

def test_min_var_process_expression_compendium():
    """
    Test the variance_threshold argument of the process_expression_compendium function to ensure it filters out genes
    with variance below the threshold.
    """