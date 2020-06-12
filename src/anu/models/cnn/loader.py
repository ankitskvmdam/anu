"""Dataloader for the model."""

import numpy as np
import torch
from torch.utils.data import Dataset
import vaex


class InteractionClassificationDataset(Dataset):
    """Interaction classification dataset."""

    def __init__(
        self: "InteractionClassificationDataset", df: vaex.dataframe.DataFrame
    ) -> None:
        """Initialize dataset."""
        try:
            self.df = df
        except BaseException:
            raise "Error Initializing dataset"

    def __len__(self: "InteractionClassificationDataset") -> int:
        """Return len of dataframe."""
        return len(self.df)

    def __getitem__(
        self: "InteractionClassificationDataset", idx: int
    ) -> (torch.Tensor, torch.Tensor):
        """Return interaction_input and interaction_labels."""
        # Extract seq from df and concatenate
        sequence = np.hstack([self.df[idx][0], self.df[idx][1]])

        # Extract x pos from df and concatenate
        pos_x = np.hstack([self.df[idx][2], self.df[idx][3]])

        # Extract y pos from df and concatenate
        pos_y = np.hstack([self.df[idx][4], self.df[idx][5]])

        # Extract z pos from df and concatenate
        pos_z = np.hstack([self.df[idx][6], self.df[idx][7]])

        # Extract hydropathy from df and concatenate
        hydropathy = np.hstack([self.df[idx][8], self.df[idx][9]])

        # Extract hydropathy_index from df and concatenate
        hydropathy_index = np.hstack([self.df[idx][10], self.df[idx][11]])

        # Extract ph from df and concatenate
        ph = np.hstack([self.df[idx][12], self.df[idx][13]])

        # Extract mass from df and concatenate
        mass = np.hstack([self.df[idx][14], self.df[idx][15]])

        # Extract hydropathy from df and concatenate
        isoelectric_point = np.hstack([self.df[idx][16], self.df[idx][17]])

        # Extract hydropathy from df and concatenate
        charge = np.hstack([self.df[idx][18], self.df[idx][19]])

        # Build final matrix with vertical stacking all features
        features_matrix = np.vstack(
            [
                sequence,
                pos_x,
                pos_y,
                pos_z,
                hydropathy,
                hydropathy_index,
                ph,
                mass,
                isoelectric_point,
                charge,
            ]
        )
        interaction_type = np.array(self.df[idx][20])

        features_matrix.setflags(write=True)
        interaction_type.setflags(write=True)

        interaction_input = torch.from_numpy(features_matrix).view((1, 10, 8000))
        interaction_label = torch.from_numpy(interaction_type)

        return interaction_label, interaction_input
