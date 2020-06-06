"""CNN model trainer."""

from typing import Optional

from torch.autograd import Variable
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

# from anu.models.cnn.loader import InteractionClassificationDataloader
from anu.models.cnn.config import CNNTrainerConfig, get_default_cnn_trainer_config
from anu.models.cnn.model import ConvNet


class CNNTrainer:
    """CNN model trainer."""

    def __init__(
        self: "CNNTrainer",
        train_dataloader: DataLoader,
        test_dataloader: DataLoader,
        valid_dataloader: Optional[DataLoader],
        model: ConvNet,
        config: Optional[CNNTrainerConfig],
    ) -> None:
        """Initialize CNN trainer."""
        # initialize tensorboard writer for logging metrics
        if config is None:
            self.config = get_default_cnn_trainer_config()
        else:
            self.config = config
        self.writer = SummaryWriter(self.config.logdir)
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.valid_dataloader = valid_dataloader
        self.model = model

    def train(self: "CNNTrainer") -> None:
        """Trains the model."""
        # spawn the model on selected device
        cnn_net = self.model().to(self.config.device)

        # write model to tensorboard
        self.writer.add_graph(cnn_net)

        # spawn an optimizer
        optimizer = Adam(cnn_net.parameters(), lr=0.0001).to(self.config.device)

        # loss criterion
        criterion_loss = CrossEntropyLoss()

        for _epoch in tqdm(self.config.epochs):
            for input_labels, input_batch in tqdm(self.train_dataloader):

                # forward pass
                output = cnn_net(input_batch.float().to(self.config.device))

                # calculate loss
                loss = criterion_loss(
                    output,
                    Variable((input_labels.max(dim=0)[1]).to(self.config.device)),
                )

                # backward pass
                loss.backward()

                # update parameters
                optimizer.step()

                # TODO: Add callbacks for writing metrics and visualizations
