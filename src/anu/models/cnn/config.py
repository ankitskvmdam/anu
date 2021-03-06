"""CNN model configs."""

import os
from typing import TypedDict


class CNNTrainerConfig(TypedDict):
    """CNN model trainer config."""

    device: str
    epochs: int
    logdir: str
    model_savedir: str


def get_default_cnn_trainer_config() -> CNNTrainerConfig:
    """Return default cnn trainer config."""
    root = os.path.realpath(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    )
    logdir_path = os.path.join(root, "logs")
    model_savedir_path = os.path.join(root, "pre_trained_models")

    if os.environ.get("TRAIN_DEVICE") == "GPU":
        config: CNNTrainerConfig = {
            "device": "cuda:0",
            "epochs": 10,
            "logdir": logdir_path,
            "model_savedir": model_savedir_path,
        }
    else:
        config: CNNTrainerConfig = {
            "device": "cpu",
            "epochs": 10,
            "logdir": logdir_path,
            "model_savedir": model_savedir_path,
        }
    return config
