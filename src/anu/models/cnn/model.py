"""CNN model."""

from torch import nn
from torch import Tensor


class ConvNet(nn.Module):
    """CNN model."""

    def __init__(self: "ConvNet") -> None:
        """Initialize CNN model."""
        super(ConvNet, self).__init__()

        self.conv = nn.Sequential(
            # 2D convolution layer
            nn.Conv2d(1, 10, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(10),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # 2D convolution layer
            nn.Conv2d(10, 30, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(30),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # 2D convolution layer
            nn.Conv2d(30, 30, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(30),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.fcn = nn.Sequential(
            nn.Linear(30 * 1 * 500 * 2, 1500),
            nn.ReLU(inplace=True),
            nn.Linear(1500, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 12),
            nn.ReLU(inplace=True),
            nn.Linear(12, 2),
        )

    # Defining the forward pass
    def forward(self: "ConvNet", x: Tensor) -> Tensor:
        """Forward pass function."""
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fcn(x)
        return x
