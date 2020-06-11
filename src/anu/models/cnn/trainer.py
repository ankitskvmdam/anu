"""CNN model trainer."""

import os
from typing import Optional

from logzero import logger
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
        self.writer.add_graph(cnn_net)
        logger.info("Graph added to tensor board")

        # spawn an optimizer
        optimizer = Adam(cnn_net.parameters(), lr=0.0001).to(self.config["device"])
        logger.info("Initialized optimizer [ADAM]")

        # loss criterion
        criterion_loss = CrossEntropyLoss()
        logger.info("Initialized loss criterion")

        for _epoch in tqdm(self.config["epochs"]):
            for input_labels, input_batch in tqdm(self.train_dataloader):
                # forward pass
                logger.info("Forward pass.")
                output = cnn_net(input_batch.float().to(self.config["device"]))

                # calculate loss
                logger.info("Calculate loss.")
                loss = criterion_loss(
                    output,
                    Variable((input_labels.max(dim=0)[1]).to(self.config["device"])),
                )

                # backward pass
                logger.info("Loss backward.")
                loss.backward()

                # update parameters
                optimizer.step()

                # TODO: Add callbacks for writing metrics and visualizations

            logger.info("Saving model.")
            cnn_net.save(os.path.join(self.config["model_savedir"], "cnn"))
