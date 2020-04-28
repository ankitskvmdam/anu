"""Command-line entrypoint."""
import textwrap

import click

from .. import __version__


@click.group()
@click.version_option(version=__version__)
def main(language: str) -> None:
    """The hypermodern Python project."""

    click.secho("Hello, World!", fg="green")
