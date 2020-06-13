"""pipeline module for cnn model."""

import os
from typing import List

import click
from logzero import logger
import torch
from torch.utils.data import DataLoader
import vaex

from anu.data.dataframe_operation import read_dataframes_from_file
from anu.models.cnn.config import get_default_cnn_trainer_config
from anu.models.cnn.loader import InteractionClassificationDataset
from anu.models.cnn.trainer import CNNTrainer


def load_dataset(df: vaex.dataframe.DataFrame) -> InteractionClassificationDataset:
    """Load dataset to InteractionClassificationDataset.

    Args:
        df: vaex dataframe.

    Returns:
        InteractionClassificationDataset class object
    """
    return InteractionClassificationDataset(df)


def data_loader(
    dataset: InteractionClassificationDataset, batch_size: int, num_workers: int,
) -> DataLoader:
    """Data loader.

    Args:
        dataset: InteractionClassificationDataset.
        batch_size: size of each batch.
        num_workers: for multiprocessing.

    Returns:
        Dataloader
    """
    return DataLoader(dataset, batch_size=batch_size, num_workers=num_workers)


def train_cnn(paths: List[str], batch_size: int = 2, num_workers: int = 2) -> None:
    """Train using cnn model.

    Args:
        paths: list of dataframes path with respect to /data/processed.
        batch_size: size of each batch.
        num_workers: for multiprocessing.
    """
    logger.info("Loading dataframe")
    df = read_dataframes_from_file(paths)

    logger.info("Spliting dataframe")
    train_df, test_df, validate_df = df.split_random(frac=[0.7, 0.2, 0.1])

    # Load dataset
    logger.info("Loading dataset")
    train_dataset = load_dataset(train_df)
    test_dataset = load_dataset(test_df)
    validate_dataset = load_dataset(validate_df)

    # Dataloader
    logger.info("Preparing dataloader")
    train_dataloader = data_loader(train_dataset, batch_size, num_workers)
    test_dataloader = data_loader(test_dataset, batch_size, num_workers)
    validate_dataloader = data_loader(validate_dataset, batch_size, num_workers)

    logger.info("Initiating cnn trainer")
    cnn_trainer = CNNTrainer(train_dataloader, test_dataloader, validate_dataloader)
    cnn_trainer.train("protein_cnn_model.pt")


def predict_cnn(df: vaex.dataframe.DataFrame) -> None:
    """Predict using cnn model.

    Args:
        df: vaex dataframe.
    """
    MODEL_PATH = os.path.realpath(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "..",
                "pre_trained_models",
                "cnn",
                "protein_cnn_model.pt",
            )
        )
    )

    if os.path.exists(MODEL_PATH) is False:
        click.secho("Pretrained model is not available", fg="red")
        exit()

    click.secho("Loading model...", fg="blue")
    model = torch.load(MODEL_PATH)
    model.eval()

    click.secho("Preparing data for model...", fg="blue")
    dataset = load_dataset(df)

    _, model_input = dataset.__getitem__(0)
    config = get_default_cnn_trainer_config()

    model_input_unsqueeze = model_input.unsqueeze_(0)
    click.secho("Calculating interaction statistics", fg="cyan")
    output = model(model_input_unsqueeze.float().to(config["device"]))
    softmax = torch.nn.Softmax(dim=-1)(output)
    argmax = torch.argmax(softmax)
    # print(output)
    # print(softmax)
    # print(argmax.item())
    click.secho("*" * 52, fg="magenta")
    result = "*" + (" " * 22) + "Result" + (" " * 22) + "*"
    click.secho(result, fg="magenta")
    click.secho("*" * 52, fg="magenta")
    stars = "*" + " " * 50 + "*"
    click.secho(stars, fg="magenta")

    if argmax.item() == 1:
        click.secho(f"*{' '*13}Non-interacting proteins{' '*12} *", fg="magenta")
    else:
        click.secho(f"*{' '*15}Interacting proteins{' '*14} *", fg="magenta")

    click.secho(stars, fg="magenta")
    click.secho("*" * 52, fg="magenta")
