"""Command-line entrypoint."""

import click

from anu.cli.data import data
from anu.cli.predict import predict
from anu.cli.train import train
from .. import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Predict the interaction parameters."""
    pass


main.add_command(data)
main.add_command(predict)
main.add_command(train)
