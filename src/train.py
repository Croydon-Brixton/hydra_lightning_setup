"""Main module to load and train the model. This should be the program entry point."""
import hydra
from omegaconf import DictConfig
from pytorch_lightning import Trainer, seed_everything

from src import constants
from src.models.sample_model import SampleModel
from src.models.utils import get_lightning_model
from src.utils.logutils import get_logger, get_lightning_logger
from src.utils.callbacks import get_callbacks
from src.data.datamodule import get_datamodule

logger = get_logger(__name__)

# Load hydra config from yaml filses and command line arguments.
@hydra.main(config_path=constants.CONFIG_PATH,
            config_name="default",
            version_base=constants.HYDRA_VERSION_BASE)
def train(config: DictConfig):
    """Train model with PyTorch Lightning and log with Wandb."""
    
    # Set random seeds
    seed_everything(config.seed)
    config = config.validate_config(config)


    # Get the model and datasets 
    model = get_lightning_model(config)
    datamodule = get_datamodule(config)

    # Setup logging and checkpointing
    pl_logger = get_lightning_logger(config)
    callbacks = get_callbacks(config)

    # Instantiate Trainer
    trainer = Trainer(
        accelerator=config.parallel_engine,
        auto_select_gpus=config.cuda,
        gpus=config.gpus,
        benchmark=True,
        deterministic=True,
        callbacks=callbacks,
        prepare_data_per_node=False,
        max_epochs=config.epochs,
        logger=pl_logger,
        log_every_n_steps=config.log_steps,
        val_check_interval=config.val_interval,
    )

    # Train model
    trainer.fit(model, datamodule)

    # Test the model at the best checkoint:
    # TODO Implement
    if config.test:
        logger.info("Testing the model at checkpoint %s", ckpt.best_model_path)
        model = SampleModel.load_from_checkpoint(ckpt.best_model_path)
        trainer.test(model)
        logger.info("Train loop completed. Exiting.")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    train()
