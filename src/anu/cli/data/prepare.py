"""cli data prepar modules."""

import os

import click

from anu.data.data_operations import extract_proteins_id_from_dataframe
from anu.data.dataframe_operation import (
    convert_csv_to_dataframe,
    save_dataframe_to_file,
)
from anu.data.pipelines.prepare_input import build_input_from_json


@click.command()
def dataframes() -> None:
    """Prepare the dataframes from raw data.

    This function first prepare the dataframe using pickle dataset
    then using negatome database.

    Steps:
        1. First prepare raw vaex dataframe for pickle dataset
        2. Filter column of raw vaex dataframe and keep on the
        column containing protein id
        3. Do above two process for negatome dataset.
    """
    PICKLE_PROTEIN_A_COLUMN = "InteractorA"
    PICKLE_PROTEIN_B_COLUMN = "InteractorB"
    PICKLE_PATH = os.path.join("pickle", "interacting-protein.txt")

    NEGATOME_PROTEIN_A_COLUMN = "UniprotID_A"
    NEGATOME_PROTEIN_B_COLUMN = "UniprotID_B"
    NEGATOME_PATH = os.path.join("negatome", "non-interacting-protein.tsv")

    try:
        # Pickle operations.
        click.secho("Preparing pickle dataframes", fg="cyan")
        pickle_df = convert_csv_to_dataframe(PICKLE_PATH)

        click.secho("Extracting protein column from pickle dataframes", fg="blue")
        pickle_df = extract_proteins_id_from_dataframe(
            pickle_df, PICKLE_PROTEIN_A_COLUMN, PICKLE_PROTEIN_B_COLUMN
        )

        # Negatome operations.
        click.secho("Preparing negatome dataframes", fg="cyan")
        negatome_df = convert_csv_to_dataframe(NEGATOME_PATH)

        click.secho("Extracting protein column from negatome dataframes", fg="blue")
        negatome_df = extract_proteins_id_from_dataframe(
            negatome_df, NEGATOME_PROTEIN_A_COLUMN, NEGATOME_PROTEIN_B_COLUMN
        )
    except OSError:
        click.secho("Dataset(s) not found.", fg="red")
        click.secho("Probably you haven't run: anu data fetch-databases", fg="yellow")
        exit()

    click.secho("Saving dataframes to file. Saving in arrow format.")
    PICKLE_SAVE_PATH = os.path.join("pickle", "interacting-protein")
    NEGATOME_SAVE_PATH = os.path.join("negatome", "non-interacting-protein")

    status = save_dataframe_to_file(pickle_df, PICKLE_SAVE_PATH)
    if status is False:
        click.secho("Unable to save dataframes", fg="red")
        exit()

    status = save_dataframe_to_file(negatome_df, NEGATOME_SAVE_PATH)
    if status is False:
        click.secho("Unable to save dataframes", fg="red")
        exit()

    click.secho("Completed successfully.", fg="green")


@click.command()
@click.option(
    "--interacting",
    "-i",
    is_flag=True,
    help="Prepare interacting input dataframe for training",
)
@click.option(
    "--non-interacting",
    "-n",
    is_flag=True,
    help="Prepare non-interacting input dataframe for training",
)
def inputs(interacting: bool, non_interacting: bool) -> None:
    """Prepare input dataframe for training."""
    NEGATOME_PATH = os.path.join(
        "negatome", "non-interacting-protein", "pair_selected.json"
    )
    PICKLE_PATH = os.path.join("pickle", "interacting-protein", "pair_selected.json")

    if interacting:
        click.secho("Building interacting protein input dataframe", fg="blue")
        build_input_from_json(PICKLE_PATH, "pickle", "pickle_input_df", True)
        click.secho("Process completed successfully", fg="green")

    elif non_interacting:
        click.secho("Building non-interacting protein input dataframe", fg="blue")
        build_input_from_json(NEGATOME_PATH, "negatome", "negatome_input_df", False)
        click.secho("Process completed successfully", fg="green")

    else:
        click.secho("First, building interacting protein input dataframe", fg="blue")
        build_input_from_json(PICKLE_PATH, "pickle", "pickle_input_df", True)
        click.secho("Now, building non-interacting protein input dataframe", fg="blue")
        build_input_from_json(NEGATOME_PATH, "negatome", "negatome_input_df", False)
        click.secho("Process completed successfully", fg="green")


@click.group()
def prepare() -> None:
    """Currently only prepare dataframes or input."""
    pass


prepare.add_command(dataframes)
prepare.add_command(inputs)
