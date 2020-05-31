"""modules to realted to data frame operations."""

import os
from typing import Optional

import vaex


def convert_csv_to_dataframe(filename: str, sep: str = "\t") -> Optional[vaex.dataframe.DataFrame]:
    """Convert the csv file to pandas dataframe.

    File path must be relative to data/raw

    Args:
        filename: name of the file with extention.

    Returns:
        vaex dataframe.
    """
    path = os.path.realpath(os.path.join("..", "..", "..", "data", "raw", filename))

    if os.path.exists(path):
        return vaex.read_csv(filepath_or_buffer=path, sep="\t", lineterminator="\n")


def save_dataframe_to_file(df: vaex.dataframe.DataFrame, filename: str) -> bool:
    """Only save dataframe relative to data/processed in arrow format.

    Args:
        df: vaex dataframe.
        filename: name of the file.

    Returns:
        True if successfully save the file.
    """
    import pathlib

    path_to_processed_data = os.path.realpath(
        os.path.join("..", "..", "..", "data", "processed")
    )

    if os.path.exists(path_to_processed_data):
        path = os.path.realpath(os.path.join(path_to_processed_data, filename))
        dir = os.path.dirname(path)
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

        if os.path.exists(f"{path}.arrow"):
            os.remove(f"{path}.arrow")

        df.export(f"{path}.arrow")
        return True

    return False


def read_dataframe_from_file(path: str) -> vaex.dataframe.DataFrame:
    """Only read dataframe present in data/processed.

    Args:
        path: path relative to data/processed.

    Returns:
        vaex dataframe.
    """
    path_to_processed_data = os.path.realpath(
        os.path.join("..", "..", "..", "data", "processed", path)
    )

    return vaex.open(f"{path_to_processed_data}.arrow")
