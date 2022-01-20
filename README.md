# Getting started

Clone the repo in your working machine.

```bash
make env
source env/bin/activate
make init
```

# Experiment logging with wandb

To log to wandb, you will first need to log in. To do so, simply install wandb via pip
with `pip install wandb` and call `wandb login` from the commandline.

If you are already logged in and need to relogin for some reason, use `wandb login --relogin`.

# Training a model with pytorch lightning and logging on wandb

To run a model simply use

```
python src/train.py run_name=<YOUR_RUN_NAME>
```

To use parameters that are different from the default parameters in `src/configs/config.yaml`
you can simply provide them in the command line call. For example:

```
python src/train.py run_name=<YOUR_RUN_NAME> epochs=100
```
