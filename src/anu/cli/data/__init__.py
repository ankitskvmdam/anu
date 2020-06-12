"""Cli modules related to data."""

import click

from .fetch import fetch_databases, fetch_pdb_files
from .prepare import prepare_dataframes


@click.group()
def data() -> None:
    """Data group."""
    pass


data.add_command(fetch_databases)
data.add_command(fetch_pdb_files)
data.add_command(prepare_dataframes)
