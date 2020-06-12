"""modules to realted to data frame operations."""

import os
from typing import Union, Optional

import vaex


def get_base_data_path() -> str:
    """Compute the base data path.

    Returns:
        Return the base data path.
    """
    return os.path.realpath(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
        )
    )


def convert_csv_to_dataframe(
    filename: str, sep: str = "\t"
) -> Union[vaex.dataframe.DataFrame, None]:
    """Convert the csv file to pandas dataframe.

    File path must be relative to data/raw

    Args:
        filename: name of the file with extention.

    Returns:
        vaex dataframe.
    """
    path = os.path.join(get_base_data_path(), "raw", filename)
    if os.path.exists(path):
        return vaex.read_csv(filepath_or_buffer=path, sep="\t", lineterminator="\n")

    raise OSError


def save_dataframe_to_file(df: vaex.dataframe.DataFrame, filename: str) -> bool:
    """Only save dataframe relative to data/processed in arrow format.

    Args:
        df: vaex dataframe.
        filename: name of the file.

    Returns:
        True if successfully save the file.
    """
    import pathlib

    path_to_processed_data = os.path.join(get_base_data_path(), "processed")

    if os.path.exists(path_to_processed_data):
        path = os.path.realpath(os.path.join(path_to_processed_data, filename))
        dir = os.path.dirname(path)
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

        if os.path.exists(f"{path}.arrow"):
            os.remove(f"{path}.arrow")

        df.export(f"{path}.arrow")
        return True

    return False


def read_dataframe_from_file(path: str) -> Optional[vaex.dataframe.DataFrame]:
    """Only read dataframe present in data/processed.

    Args:
        path: path relative to data/processed.

    Returns:
        vaex dataframe.
    """
    path_to_processed_data = os.path.join(get_base_data_path(), "processed", path)
    file_path = f"{path_to_processed_data}.arrow"

    if not os.path.exists(file_path):
        raise OSError

    else:
        return vaex.open(file_path)


def read_dataframes_from_file(path_list: str) -> Optional[vaex.dataframe.DataFrame]:
    """Only read dataframe present in data/processed.

    Args:
        path_list: list of path relative to data/processed.

    Returns:
        vaex dataframe.
    """

    base_path = os.path.join(get_base_data_path(), "processed")

    file_path_list: List[str] = []

    for path in path_list:
        file_path = os.path.join(base_path, f"{path}.arrow")
        if not os.path.exists(file_path):
            raise OSError
        file_path_list.append(file_path)

    return vaex.open_many(file_path_list)


def shuffle_dataframe(
    df: vaex.dataframe.DataFrame,
    frac: float = 1.0,
    replace: bool = False,
    random_state: int = 32,
) -> vaex.dataframe.DataFrame:
    """Shuffle the given dataframe.

    Args:
        df: vaex dataframe which has to be shuffled.
        frac: fractional number of takes to take
        replace: If true, a row may be drawn multiple times
        random_state: seed or RandomState for reproducibility
    """
    return df.sample(frac=frac, replace=replace, random_state=random_state)
