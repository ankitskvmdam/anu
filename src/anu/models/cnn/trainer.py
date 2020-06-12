"""CNN model trainer."""

import os
import pathlib
from time import asctime, time
from typing import Optional

from logzero import logger
import torch
from torch.autograd import Variable
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from anu.models.cnn.config import CNNTrainerConfig, get_default_cnn_trainer_config
from anu.models.cnn.model import ConvNet


class CNNTrainer:
    """CNN model trainer."""

    def __init__(
        self: "CNNTrainer",
        train_dataloader: DataLoader,
        test_dataloader: DataLoader,
        valid_dataloader: Optional[DataLoader] = None,
        config: Optional[CNNTrainerConfig] = None,
        model: ConvNet = ConvNet,
    ) -> None:
        """Initialize CNN trainer."""
        # initialize tensorboard writer for logging metrics
        if config is None:
            self.config = get_default_cnn_trainer_config()
        else:
            self.config = config
        self.writer = SummaryWriter(os.path.join(self.config["logdir"], "cnn"))
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.valid_dataloader = valid_dataloader
        self.model = model

    def train(self: "CNNTrainer") -> None:
        """Trains the model."""
        logger.info("Starting ConvNet Training.")

        # spawn the model on selected device
        cnn_net = self.model().to(self.config["device"])
        logger.info("Initialized model.")

        # write model to tensorboard
        # self.writer.add_graph(cnn_net)
        # logger.info("Graph added to tensor board")

        # spawn an optimizer
        optimizer = Adam(cnn_net.parameters(), lr=0.0001)  # .to(self.config["device"])
        logger.info("Initialized optimizer [ADAM]")

        # loss criterion
        criterion_loss = CrossEntropyLoss()
        logger.info("Initialized loss criterion")

        current_status = tqdm(total=0, position=3, bar_format="{desc}")
        save_status = tqdm(total=0, position=4, bar_format="{desc}")
        for _epoch in tqdm(range(self.config["epochs"]), unit=" epoch", position=1):
            for idx, (input_labels, input_batch) in enumerate(
                tqdm(self.train_dataloader, position=2, unit=" row")
            ):
                # forward pass
                current_status.set_description("Forward pass.")
                output = cnn_net(input_batch.float().to(self.config["device"]))

                # calculate loss
                current_status.set_description("Calculate loss.")
                loss = criterion_loss(
                    output,
                    Variable((input_labels.max(dim=0)[1]).to(self.config["device"])),
                )

                # backward pass
                current_status.set_description("Loss backward.")
                loss.backward()

                # update parameters
                optimizer.step()

                # TODO: Add callbacks for writing metrics and visualizations
                if idx % 100 == 0:
                    save_status.set_description("Saving model")
                    path = os.path.join(
                        self.config["model_savedir"], "cnn", str(int(time()))
                    )
                    pathlib.Path(path).mkdir(exist_ok=True, parents=True)
                    torch.save(cnn_net, f"{path}/{int(time())}.pt")
                    save_status.set_description(f"Last model saved at: {asctime()}")

            torch.save(
                cnn_net,
                os.path.join(self.config["model_savedir"], "cnn", "{_epoch}.pt"),
            )
            logger.info("Saving model.")
