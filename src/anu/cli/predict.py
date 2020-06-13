"""Anu predict cli command."""

import json
import os
from typing import Any, List, Tuple, Union

import click

from anu.data.data_operations import fetch_pdb_from_pdb_id, fetch_pdb_using_uniprot_id
from anu.data.pipelines.prepare_input import build_df_from_dic, build_matrix
from anu.models.cnn.pipeline import predict_cnn


@click.group()
def predict() -> None:
    """To predict interactions."""
    pass


def download_file(ids: Tuple[str, str], database: str) -> Union[List[str], None]:
    """Download pdb files.

    Args:
        ids: list of pdb id or uniprot id but not both.
        database: pdb or uniport str

    Returns:
        downloaded path of pdb files or None.
    """
    proteins_pdb_path = []

    download_path = os.path.realpath(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "user")
        )
    )
    downloaded_file_list_path = os.path.join(download_path, "downloaded.json")

    if os.path.exists(download_path) is False:
        os.mkdir(download_path)

    downloaded_list = {}

    if os.path.exists(downloaded_file_list_path) is True:
        with open(downloaded_file_list_path) as fp:
            downloaded_list = json.load(fp)

    click.secho("Downloading pdb files...", fg="cyan")
    for id in ids:
        if id in downloaded_list:
            click.secho(f"{id} is already downloaded. Skipping this...", fg="green")
            proteins_pdb_path.append(os.path.join(download_path, f"{id}.pdb"))
        else:
            if database == "pdb":
                pdb, status = fetch_pdb_from_pdb_id(id)
            else:
                pdb, status = fetch_pdb_using_uniprot_id(id)

            if status == 200:
                with open(os.path.join(download_path, f"{id}.pdb"), "w") as fp:
                    fp.write(pdb)

                with open(downloaded_file_list_path, "w") as fp:
                    downloaded_list[id] = id
                    json.dump(downloaded_list, fp)

                proteins_pdb_path.append(os.path.join(download_path, f"{id}.pdb"))
                click.secho(f"Downloaded {id}")

            else:
                click.secho(f"Unable to download pdb with id: {id}", fg="yellow")
                click.secho(
                    "Given id may be wrong or there might be a network issue",
                    fg="yellow",
                )
                click.secho("Quitting...", fg="yellow")
                exit()

    return proteins_pdb_path


@click.command(help="Give pdb file path",)
@click.argument("paths", required=False, nargs=2)
@click.option("--pdb", "-p", is_flag=True, help="Give pdb id instead of path")
@click.option("--uniprot", "-u", is_flag=True, help="Give uniport id instread of path")
def protein(paths: Any, pdb: Union[bool, None], uniprot: Union[bool, None]) -> None:
    """Predict interaction possibility between given proteins.

    Args:
        paths: List of pdb path or uniport id or pdb id.
        pdb: bool value, if true then download pdb.
        uniprot: bool value, if true download pdb using uniport it.
    """
    protein_a = ""
    protein_b = ""

    if pdb is True:
        protein_a, protein_b = download_file(paths, "pdb")

    elif uniprot is True:
        protein_a, protein_b = download_file(paths, "uniprot")

    else:
        protein_a, protein_b = paths
        if os.path.exists(protein_a) is False:
            click.secho(f"Path: {protein_a} doesn't exists...", fg="red")
            exit()
        if os.path.exists(protein_b) is False:
            click.secho(f"Path: {protein_b} doesn't exists...", fg="red")
            exit()

    click.secho("PDB file loaded successfully", fg="green")
    click.secho("Preparing input", fg="cyan")
    protein_a = build_matrix(protein_a, "Protein A")
    protein_b = build_matrix(protein_b, "Protein B")

    df = build_df_from_dic(protein_a, protein_b)

    predict_cnn(df)


predict.add_command(protein)
