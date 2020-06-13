"""module to prepare data."""

import os
from time import time

import click
import requests
import vaex

from anu.cli.utils.download_bar import print_progress


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


def fetch_pdb_using_uniprot_id(id: str) -> (str, int):
    """Fetch pdb file using uniprot id.

    Currently fetch pdb file using swiss-model using uniprot id.

    Args:
        id: uniprot id.

    Returns:
        Return a tuple of pdb file in text if found and status code.
    """
    # Strip the id.
    id = str.strip(id)

    base_url = "https://swissmodel.expasy.org/repository/uniprot/"
    format = ".pdb"

    complete_url = f"{base_url}{id}{format}"

    file = requests.get(complete_url)
    return (file.text, file.status_code)


def fetch_from_zenodo(id: str, path: str, filename: str) -> None:
    """Download data from zenodo.

    Args:
        id: zenodo record id.
        path: directory path where to save file.
        filename: name of the downloaded file.
    """
    zendo_base_get_url = "https://zenodo.org/api/records/"

    click.secho("Retrieving download information")
    r = requests.get(f"{zendo_base_get_url}{id}")
    r = r.json()

    click.secho(f"Downloading file: {filename}")
    file_link = r["files"][0]["links"]["self"]
    file_path = os.path.join(path, filename)

    r = requests.get(file_link, stream=True)
    file_size = int(r.headers.get("content-length"))
    with open(file_path, "w") as f:
        start = int(time())
        size = 0
        speed = 0
        total_size = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                size = size + f.write(chunk.decode("utf-8"))
                f.flush()

                total_size = total_size + len(chunk)
                end = int(time())
                diff = end - start
                if diff > 1:
                    start = int(time())
                    speed = size
                    size = 0
                print_progress(file_size, total_size, speed)
        print("\n")


def fetch_pdb_from_pdb_id(id: str) -> (str, int):
    """Fetch pdb.

    Args:
        id: pdb id.

    Returns:
        Return a tuple of pdb file in text if found and status code.
    """
    # Strip the id.
    id = str.strip(id)

    base_url = "https://files.rcsb.org/download/"
    format = ".pdb"

    complete_url = f"{base_url}{id}{format}"

    file = requests.get(complete_url)
    return (file.text, file.status_code)
