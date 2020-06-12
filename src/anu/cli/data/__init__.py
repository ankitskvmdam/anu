"""Cli modules related to data."""

import click

from .fetch import fetch_databases, fetch_pdb_files
from .prepare import prepare_dataframes, prepare_input


@click.group()
def data() -> None:
    """Data group."""
    pass


# Fetch commands
data.add_command(fetch_databases)
data.add_command(fetch_pdb_files)

# Prepare command
data.add_command(prepare_dataframes)
data.add_command(prepare_input)
