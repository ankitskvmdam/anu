"""pipeline module for cnn model."""

from typing import List

from logzero import logger
from torch.utils.data import DataLoader
import vaex

from anu.data.dataframe_operation import read_dataframes_from_file
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
    cnn_trainer.train()
