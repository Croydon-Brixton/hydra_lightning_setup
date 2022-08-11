"""Pytorch Lightning Sample model skeleton."""
from typing import List

import pytorch_lightning as pl
import torch
from omegaconf import DictConfig
from torch.utils.data import DataLoader, Dataset

from src.utils.logutils import get_logger

logger = get_logger(__file__)


def get_sample_model(config: DictConfig):
    """Define and return the Unet model from the config."""

    # The pytorch model
    # Pass parameters via "config.parameter_name"
    # Example:
    run_name = config.run_name  # pylint: disable=unused-variable
    model: torch.nn.Module = SampleNet()

    return model


class SampleDataset(Dataset):
    """A dummy dataset to illustrate how to work with lightning"""

    def __init__(self) -> None:
        pass

    def __len__(self) -> int:
        return 10

    def __getitem__(self, idx: int) -> torch.Tensor:
        return torch.rand((10)), torch.rand((10))


class SampleNet(torch.nn.Module):
    """A dummy network to illustrate how to work with lightning"""

    def __init__(self):
        super().__init__()
        self.a = torch.nn.Parameter(torch.randn(()))

    def forward(self, x: torch.Tensor):
        return self.a * x


class SampleModel(pl.LightningModule):
    """A dummy model to illustrate how to work with lightning"""

    def __init__(self, config: DictConfig) -> None:
        super().__init__()
        self.save_hyperparameters(config)
        self.config = config
        self.model: torch.nn.Module = get_sample_model(config)
        self.loss = self.configure_loss(config.loss)

    # --- Configuring the model
    def configure_optimizers(self):
        logger.info("Configuring optimizer with learning rate %s", self.config.learning_rate)
        opt = torch.optim.Adam(params=self.parameters(), lr=self.config.learning_rate)
        return opt

    def configure_loss(self, name: str):
        """Return the loss function based on the config."""
        logger.info("Selecting loss function: %s", name)
        dummy_loss = lambda y, y_hat: torch.sum((y - y_hat) ** 2)
        return dummy_loss

    # --- Forward pass
    def forward(self, x):
        return self.model(x)

    # --- Training
    def train_dataloader(self):
        """Load train dataset."""
        logger.info("Train-loader: Loading training data")
        dataloader = DataLoader(SampleDataset())
        return dataloader

    def training_step(self, batch: torch.Tensor, _):
        x, y = batch[0], batch[1]
        y_hat = self(x)  # Calls self.forward(x)
        loss = self.loss(y, y_hat)
        self.log("train_loss", loss)  # Logs to wandb
        return loss

    # --- Validation
    def val_dataloader(self):
        """Load validation dataset."""
        logger.info("Valid-loader: Loading validation data")
        dataloader = DataLoader(SampleDataset())
        return dataloader

    def validation_step(self, batch: torch.Tensor, _):
        x, y = batch[0], batch[1]
        y_hat = self(x)
        return y, y_hat

    def on_validation_epoch_start(self) -> None:
        logger.info("Validation epoch started")
        # You can modify steps to be done at valid epoch starte here.
        # For example if your dataset has a switch, etc.

    def validation_epoch_end(self, outputs: List) -> None:
        y_list, y_pred_list = [], []
        for y, y_pred in outputs:
            y_list.append(y)
            y_pred_list.append(y_pred)
        self.log("Validation: wohoo", 1)  # Logs to wandb

    # --- Testing
    def test_dataloader(self):
        """Load test dataset."""
        logger.info("Test-loader: Loading test data")
        dataloader = DataLoader(SampleDataset())
        return dataloader

    def test_step(self, batch: torch.Tensor, batch_idx: int):
        return self.validation_step(batch, batch_idx)

    def on_test_epoch_start(self):
        logger.info("Test epoch started")
        # You can modify steps to be done at test epoch starte here.
        # For example if your dataset has a switch, etc.

    def test_epoch_end(self, outputs: List) -> None:
        y_list, y_pred_list = [], []
        for y, y_pred in outputs:
            y_list.append(y)
            y_pred_list.append(y_pred)
        # TODO: Calculate metrics here
