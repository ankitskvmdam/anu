"""Command-line entrypoint."""

import click

from .. import __version__

from anu.cli.data.fetch import data


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Predict the interaction parameters."""
    pass


main.add_command(data)
