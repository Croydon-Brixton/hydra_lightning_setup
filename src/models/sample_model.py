"""Pytorch Lightning Sample model skeleton."""
from typing import List

import pytorch_lightning as pl
import torch
from omegaconf import DictConfig
from torch.utils.data import DataLoader, Dataset

from src.utils.logutils import get_logger
from src.models.utils import get_model

logger = get_logger(__file__)

class SampleModel(pl.LightningModule):
    """A dummy model to illustrate how to work with lightning"""

    def __init__(self, config: DictConfig) -> None:
        super().__init__()
        self.save_hyperparameters(config)
        self.config = config
        
        # Define the model
        self.model: torch.nn.Module = get_model(config)
        
        # Define the loss
        self.loss = self.configure_loss(config.loss)

    def forward(self, x):
        return self.model(x)

    def shared_step(batch: torch.Tensor):
        x, y = batch[0], batch[1]
        y_hat = self(x)  # Calls self.forward(x)
        return y, y_hat

    def training_step(self, batch: torch.Tensor, _):
        y, y_hat = self.shared_step(batch)
        loss = self.loss(y, y_hat)
        self.log("train_loss", loss)  # Logs to wandb
        return loss

    def validation_step(self, batch: torch.Tensor, _):
        y, y_hat = self.shared_step(batch)
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
