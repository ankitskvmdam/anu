"""CNN model configs."""

from typing import TypedDict


class CNNTrainerConfig(TypedDict):
    """CNN model trainer config."""

    device: str
    epochs: int
    logdir: str


def get_default_cnn_trainer_config() -> CNNTrainerConfig:
    """Return default cnn trainer config."""
    logdir_path = ""
    config: CNNTrainerConfig = {"device": "cpu", "epochs": 10, "logdir": logdir_path}
    return config
