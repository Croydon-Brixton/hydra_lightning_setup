"""Main module to load and train the model. This should be the program entry point."""

import hydra
from omegaconf import DictConfig
from pytorch_lightning import Trainer, seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

from src import constants
from src.configs import config
from src.models.sample_model import SampleModel  # TODO
from src.utils.logutils import get_logger

logger = get_logger(__name__)


def train_model(cfg):
    """Train model with PyTorch Lightning and log with Wandb."""
    # Set random seeds
    seed_everything(cfg.seed)

    # If continuing a previous run:
    if cfg.load_from_checkpoint is not None:
        logger.info("Loading model from checkpoint %s", cfg.load_from_checkpoint)
        model = SampleModel.load_from_checkpoint(cfg.load_from_checkpoint)
        model.config = cfg
    else:
        logger.info("Initialising new model")
        model = SampleModel(cfg)  # TODO

    # Setup logging and checkpointing
    run_dir = constants.IO_PATH / "models" / str(cfg.run_name)
    run_dir.mkdir(parents=True, exist_ok=True)
    # Force all runs to log to the specified project and allow anonymous
    # logging without a wandb account.
    wandb_logger = WandbLogger(
        name=cfg.run_name,
        save_dir=run_dir,
        entity="enter_entity_name",
        project="enter_project_name",
        save_code=False,
    )
    ckpt_dir = run_dir / "checkpoints"
    ckpt_dir.mkdir(exist_ok=True)
    # Saves the top k checkpoints according to the test metric throughout
    # training.
    ckpt = ModelCheckpoint(
        dirpath=ckpt_dir,
        filename="{epoch}",
        period=cfg.checkpoint_freq,
        monitor=f"Validation: {cfg.eval_metrics}",
        save_top_k=cfg.save_top_k,
        mode="min",
    )

    # Instantiate Trainer
    trainer = Trainer(
        accelerator=cfg.parallel_engine,
        auto_select_gpus=cfg.cuda,
        gpus=cfg.gpus,
        benchmark=True,
        deterministic=True,
        checkpoint_callback=ckpt,
        prepare_data_per_node=False,
        max_epochs=cfg.epochs,
        logger=wandb_logger,
        log_every_n_steps=cfg.log_steps,
        val_check_interval=cfg.val_interval,
    )

    # Train model
    trainer.fit(model)

    # Test the model at the best checkoint:
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
