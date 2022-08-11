## Environment
### 1. Conda environment
Create a conda environment for the project via
```bash
make venv # will create a cpu environment
# NOTE: This will simply call
#  conda env create --prefix=./venv -f requirements/env.yml

# For a gpu environment call
#  make name=venv_gpu sys=gpu venv
#  conda activate ./venv_gpu

# For a Mac m1 environment call
#  make name=venv sys=m1 venv
#  conda activate ./venv

# To activate the environment, use:
conda activate ./venv
```

### 2. Environment variables

Set environemnt variables for you system in a `.env` file at the project directory
(same as this readme.)


## Experiment logging with wandb

To log to wandb, you will first need to log in. To do so, simply install wandb via pip
with `pip install wandb` and call `wandb login` from the commandline.

If you are already logged in and need to relogin for some reason, use `wandb login --relogin`.

## Training a model with pytorch lightning and logging on wandb

To run a model simply use

```
python src/train.py run_name=<YOUR_RUN_NAME>
```

To use parameters that are different from the default parameters in `src/configs/config.yaml`
you can simply provide them in the command line call. For example:

```
python src/train.py run_name=<YOUR_RUN_NAME> epochs=100
```
To configure extra things such as logging, use
```
# LOGGING
# For running at DEBUG logging level:
#  (c.f. https://hydra.cc/docs/tutorials/basic/running_your_app/logging/ )
## Activating debug log level only for loggers named `__main__` and `hydra`
python src/train.py 'hydra.verbose=[__main__, hydra]'
## Activating debug log level for all loggers
python src/train.py hydra.verbose=true

# PRINTING CONFIG ONLY
## Print only the job config, then return without running
python src/train.py --cfg job

# GET HELP
python src/train.py --help
```
