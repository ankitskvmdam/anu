"""Cli data modules related to fetching of data."""

import os
import pathlib
import requests
import time

import click

from anu.data.data_operations import fetch_from_zenodo
from anu.data.pipelines.process_raw_data import fetch_pdb_from_df
from anu.data.dataframe_operation import read_dataframe_from_file


@click.command()
def databases() -> None:
    """Fetch data from all database.

    Currently only fetch data from pickle 2.5 (interacting protein database) and
    negatome (non interacting protein database). We have uploaded the databases to
    zenodo. We use the record id to retrieve the databases.
    """
    # Zenodo record id.
    NEGATOME_ID = "3889713"
    PICKLE_ID = "3889702"

    # Path where to save data
    BASE_PATH = os.path.realpath(
        os.path.abspath(
            os.path.join(__file__, "..", "..", "..", "..", "..", "data", "raw")
        )
    )
    NEGATOME_PATH = os.path.join(BASE_PATH, "negatome")
    PICKLE_PATH = os.path.join(BASE_PATH, "pickle")

    # Create the path
    click.secho("Creating directory to save data.", fg="green")
    pathlib.Path(NEGATOME_PATH).mkdir(exist_ok=True, parents=True)
    pathlib.Path(PICKLE_PATH).mkdir(exist_ok=True, parents=True)

    try:
        # Downloading files
        click.secho("Downloading Negatome database.")
        fetch_from_zenodo(NEGATOME_ID, NEGATOME_PATH, "non-interacting-protein.tsv")

        click.secho("Downloading Pickle database.")
        fetch_from_zenodo(PICKLE_ID, PICKLE_PATH, "interacting-protein.txt")

        click.secho("Database fetching is completed successfully", fg="green")

    except requests.ConnectionError:
        click.secho("Unable to connect to the internet", fg="yellow")
        click.secho("Database fetching failed", fg="red")


def pdb_cli(path: str, db_name: str) -> None:
    """Fetch PDB files.

    Args:
        path: path of the dataframe.
        db_name: database name.
    """
    try:
        click.secho(
            f"Downloading pdb files for {db_name} dataframe. You can press ctrl+c any time and move to download pdb from next database",
            fg="cyan",
        )
        click.secho(
            "Also you don't have to download the complete pdb files. 300 to 400 from each dataset works.",
            fg="cyan",
        )
        fetch_pdb_from_df(path, db_name)
    except OSError:
        click.secho("Unable to load Dataframe", fg="red")
        click.secho(
            "This is probably if you didn't run: anu data prepare dataframes",
            fg="yellow",
        )
        exit()


@click.command()
@click.option(
    "--pickle",
    "-p",
    is_flag=True,
    help="Download pdb files for present in pickle dataset",
)
@click.option(
    "--negatome",
    "-n",
    is_flag=True,
    help="Download pdb files for present in negatome dataset",
)
def pdb(pickle: bool, negatome: bool) -> None:
    """Fetch required pdb files."""
    PICKLE_PATH = os.path.join("pickle", "interacting-protein")
    NEGATOME_PATH = os.path.join("negatome", "non-interacting-protein")

    if pickle:
        pdb_cli(PICKLE_PATH, "pickle")

    elif negatome:
        pdb_cli(NEGATOME_PATH, "negatome")

    else:
        pdb_cli(PICKLE_PATH, "pickle")
        pdb_cli(NEGATOME_PATH, "negatome")


@click.group()
def fetch() -> None:
    """Currently fetch databases or pdb files."""
    pass


fetch.add_command(pdb)
fetch.add_command(databases)
