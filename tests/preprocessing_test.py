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

    # The processed compendium should have one column "SampleID" and 3 gene columns. There should be 6 rows in total.
    assert processed_compendium.shape == (6, 4)
    assert "SampleID" in processed_compendium.columns
    assert "gene_1" in processed_compendium.columns
    assert "gene_2" in processed_compendium.columns
    assert "gene_3" in processed_compendium.columns
    assert list(processed_compendium["SampleID"]) == patients1 + patients2