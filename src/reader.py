import pandas as pd


def read_statement(file_path):

    """
    This function reads credit card Excel statement

    Input:
        Excel file path

    Output:
        DataFrame (table format)
    """

    data = pd.read_excel(file_path)

    return data