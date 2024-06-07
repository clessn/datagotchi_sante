import os
from pathlib import Path

from config import Config
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


class Constants:
    # Paths
    DATA_PATH = Path(os.getenv("DATA_PATH"))
    RAW_FOLDER_NAME = "raw"
    ML_FOLDER_NAME = "ml"
    SANDBOX_FOLDER_NAME = "sandbox"
    REAL_FOLDER_NAME = "real"
    RAW_PATH = DATA_PATH / RAW_FOLDER_NAME
    ML_PATH = DATA_PATH / ML_FOLDER_NAME / eval(Config.RUN_TYPE)
    LOGGING_PATH = Path(os.getcwd()) / "code" / "ml"

    # Filenames
    RAW_FILENAME = "data_raw.sav"
    CODEBOOK_FILENAME = "frozen_codebook_may_5.csv"
    ATTRIBUTES_FILENAME = "attributes.csv"
    FEATURES_FILENAME = "features.csv"
    TARGETS_FILENAME = "targets.csv"
    PREDICTIONS_FILENAME = "predictions.csv"
    METRICS_FILENAME = "metrics.csv"
    LOGGING_CONFIG_FILENAME = "logging.conf"

    # Codebook fields
    CODEBOOK_NAME_COL = "raw_variable_name"
    CODEBOOK_TYPE_COL = "raw_variable_type"
    CODEBOOK_OBSERVABILITY_COL = "observability"
    CODEBOOK_COLS = [CODEBOOK_NAME_COL, CODEBOOK_TYPE_COL, CODEBOOK_OBSERVABILITY_COL]

    CODEBOOK_TYPE_INTEGER_LABEL = "integer"
    CODEBOOK_TYPE_FLOAT_LABEL = "float"
    CODEBOOK_TYPE_ORDINAL_LABEL = "ordinal"

    CODEBOOK_OBSERVABILITY_OBSERVABLE_LABEL = "observable"
    CODEBOOK_OBSERVABILITY_PSEUDO_OBSERVABLE_LABEL = "pseudo-observable"
    CODEBOOK_OBSERVABILITY_PERCEPTIF_LABEL = "perceptif"
    OBSERVABILITY_LEVEL = [
        CODEBOOK_OBSERVABILITY_OBSERVABLE_LABEL,
        CODEBOOK_OBSERVABILITY_PSEUDO_OBSERVABLE_LABEL,
    ]

    # Attribute fields
    ATTRIBUTE_ID_COL = "ResponseId"

    TARGET_EMOTIONAL_HEALTH = "emotional_health"
    TARGET_POSITIVE_FUNCTIONING = "positive_functioning"
    TARGET_SCORE_TOT = "score_tot"
    TARGET_HEALTH_INDICATOR = "health_indicator"
    TARGET_COLS = [
        TARGET_EMOTIONAL_HEALTH,
        TARGET_POSITIVE_FUNCTIONING,
        TARGET_SCORE_TOT,
        TARGET_HEALTH_INDICATOR,
    ]
