"""module to prepare data."""

import vaex


def extract_proteins_id_from_dataframe(
    df: vaex.dataframe.DataFrame, first_col_name: str, second_col_name: str
) -> vaex.dataframe.DataFrame:
    """Extract protein id in pairs.

    As in a row there is only two protein given. So we only have to extract
    their id.

    Args:
        df: vaex dataframe
        first_col_name: name of the first col where we get the protein id.
        second_col_name: name of the second col where we get the protein id.

    Returns:
        Return a new dataframe having only two columns of interest.
    """
    all_columns = df.column_names
    columns_to_keep = [first_col_name, second_col_name]
    columns_to_remove = list(
        filter(lambda col: col not in columns_to_keep, all_columns)
    )

    protein_df = df.drop(columns_to_remove)

    return protein_df


def fetch_pdb_using_uniprot_id(id: str) -> str:
    """Fetch pdb file using uniprot id.

    Currently fetch pdb file using swiss-model using uniprot id.

    Args:
        id: uniprot id.

    Returns:
        Return the pdb file.
    """
    import requests

    base_url = "https://swissmodel.expasy.org/repository/uniprot/"
    format = ".pdb"

    complete_url = f"{base_url}{id}{format}"

    file = requests.get(complete_url)

    return file.text
