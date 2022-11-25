from pytorch_lightning.callbacks import Callback, ModelCheckpoint


## Define own callbacks here




def get_callbacks(cfg):
    
    callacks = []

    if 'checkpointing' in cfg.callbacks:
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
        callacks.append(ckpt)

    # TODO add your own callbacks here
    
    return callacks