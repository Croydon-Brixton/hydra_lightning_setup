import logging
from pathlib import Path

# ---------------- PATH CONSTANTS -------------------
#  Source folder path
constants_path = Path(__file__)
SRC_PATH = constants_path.parent
PROJECT_PATH = SRC_PATH.parent

# Data path
#  set your data paths ehre
DATA_PATH = Path("data")
RAW_PATH = DATA_PATH / "raw"
INTERIM_PATH = DATA_PATH / "interim"

# Config path
HYDRA_CONFIG_PATH = SRC_PATH / "configs"
HYDRA_CONFIG_NAME = "config"

# ---------------- LOGGING CONSTANTS ----------------
DEFAULT_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s [in %(funcName)s at %(pathname)s:%(lineno)d]"
)
DEFAULT_LOG_FILE = PROJECT_PATH / "logs" / "default_log.log"
DEFAULT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
DEFAULT_LOG_LEVEL = logging.DEBUG  # verbose logging per default
