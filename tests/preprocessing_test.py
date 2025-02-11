import pandas as pd
from src.preprocessing import process_expression_compendium

def test_process_expression_compendium():
    # Create a DataFrame with patient identifying strings as IDs
    expression_dict = {
        "compendium1": pd.DataFrame({
            "SampleID": ["Patient_A", "Patient_B", "Patient_C"],
            "gene_1": [5.2, 4.8, 5.0],
            "gene_2": [3.1, 2.9, 3.0],
            "gene_3": [7.4, 6.8, 7.0],
            # Add more genes as needed
        }),
        "compendium2": pd.DataFrame({
            "SampleID": ["Patient_D", "Patient_E", "Patient_F"],
            "gene_1": [5.1, 4.9, 5.0],
            "gene_2": [3.2, 2.8, 3.1],
            "gene_3": [7.2, 6.9, 7.1],
            # Add more genes as needed
        })
    }

    # Process the expression compendium
    # TODO fix process_expression_compendium function to handle non numeric columns safely for SampleIDs
    result = process_expression_compendium(expression_dict)

    # Check that the result is a DataFrame
    assert isinstance(result, pd.DataFrame)