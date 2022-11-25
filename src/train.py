"""Main module to load and train the model. This should be the program entry point."""

import hydra
from omegaconf import DictConfig
from pytorch_lightning import Trainer, seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

from src import constants
from src.configs import config
from src.models.sample_model import SampleModel# TODO
from src.models.utils import get_lightning_model
from src.utils.logutils import get_logger, get_lightning_logger
from src.utils.callbacks import get_callbacks
from src.data.datamodule import get_datamodule

logger = get_logger(__name__)


def train_model(cfg):
    """Train model with PyTorch Lightning and log with Wandb."""
    # Set random seeds
    seed_everything(cfg.seed)

    # Get the model and datasets 
    model = get_lightning_model(cfg)
    datamodule = get_datamodule(cfg)

    # Setup logging and checkpointing
    pl_logger = get_lightning_logger(cfg)
    callbacks = get_callbacks(cfg)

    # Instantiate Trainer
    trainer = Trainer(
        accelerator=cfg.parallel_engine,
        auto_select_gpus=cfg.cuda,
        gpus=cfg.gpus,
        benchmark=True,
        deterministic=True,
        callbacks=callbacks,
        prepare_data_per_node=False,
        max_epochs=cfg.epochs,
        logger=pl_logger,
        log_every_n_steps=cfg.log_steps,
        val_check_interval=cfg.val_interval,
    )

    # Train model
    trainer.fit(model)

    # Test the model at the best checkoint:
    if cfg.test:
        logger.info("Testing the model at checkpoint %s", ckpt.best_model_path)
        model = SampleModel.load_from_checkpoint(ckpt.best_model_path)
        trainer.test(model)
        logger.info("Train loop completed. Exiting.")


# Load hydra config from yaml filses and command line arguments.
@hydra.main(
    config_path=constants.CONFIG_PATH,
    config_name="default",
    version_base=constants.HYDRA_VERSION_BASE,
)
def main(cfg: DictConfig) -> None:
    """Load and validate the hydra config."""
    cfg = config.validate_config(cfg)
    train_model(cfg)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
