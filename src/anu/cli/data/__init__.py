"""Cli modules related to data."""

import click

from .fetch import fetch
from .prepare import prepare


@click.group()
def data() -> None:
    """Data group."""
    pass


data.add_command(fetch)
data.add_command(prepare)
