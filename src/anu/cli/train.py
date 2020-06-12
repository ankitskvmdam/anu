"""Cli train module."""

import os

import click


@click.command()
def cnn() -> None:
    """Train using cnn model."""
    from anu.models.cnn.pipeline import train_cnn

    # Path with respect to data/processed and without file extension
    PICKLE_PATH = os.path.join("input", "pickle", "pickle_input_df")
    NEGATOME_PATH = os.path.join("input", "negatome", "negatome_input_df")

    try:
        click.secho("Starting cnn training", fg="blue")
        train_cnn([PICKLE_PATH, NEGATOME_PATH])
    except OSError:
        click.secho("Unable to load input", fg="red")
        click.secho("You probable forgot to run: anu data prepare-input", fg="yellow")
        click.secho("Both interacting and non-interacting input must be prepared.")
        exit()


@click.group()
def train() -> None:
    """Train command group."""
    pass


train.add_command(cnn)
