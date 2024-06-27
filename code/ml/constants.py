import os
from pathlib import Path

from config import Config
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


class Constants:
    # Folders
    RAW_FOLDER_NAME = "raw"
    ML_FOLDER_NAME = "ml"
    SANDBOX_FOLDER_NAME = "sandbox"
    REAL_FOLDER_NAME = "real"
    CODEBOOK_FOLDER_NAME = "codebooks"
    FEATURE_LIBRARIES_FOLDER_NAME = "feature_libraries"
    FEATURE_LIBRARY_VERSION_FOLDER_NAME = Config.FEATURE_LIBRARY_VERSION
    FEATURE_SELECTION_FOLDER_NAME = "feature_selection"
    EXPERIMENTS_FOLDER_NAME = "experiments"
    EXPERIMENTS_FOLDER_VERSION_NAME = Config.EXPERIMENT_NAME
    EXPERIMENTS_ARTIFACTS_FOLDER_NAME = "artifacts"

    # Paths
    LOGGING_PATH = Path(os.getcwd()) / "code" / "ml"
    DATA_PATH = Path(os.getenv("DATA_PATH"))
    RAW_PATH = DATA_PATH / RAW_FOLDER_NAME
    ML_ROOT_PATH = DATA_PATH / ML_FOLDER_NAME
    CODEBOOK_PATH = ML_ROOT_PATH / CODEBOOK_FOLDER_NAME
    ML_PATH = ML_ROOT_PATH / eval(Config.RUN_TYPE)
    FEATURE_LIBRARIES_PATH = ML_PATH / FEATURE_LIBRARIES_FOLDER_NAME
    FEATURE_LIBRARY_VERSION_PATH = (
        FEATURE_LIBRARIES_PATH / FEATURE_LIBRARY_VERSION_FOLDER_NAME
    )
    FEATURE_SELECTION_PATH = (
        ML_PATH / FEATURE_SELECTION_FOLDER_NAME / FEATURE_LIBRARY_VERSION_FOLDER_NAME
    )
    EXPERIMENTS_PATH = ML_PATH / EXPERIMENTS_FOLDER_NAME
    EXPERIMENTS_VERSION_PATH = EXPERIMENTS_PATH / EXPERIMENTS_FOLDER_VERSION_NAME
    EXPERIMENTS_VERSION_ARTIFACTS_PATH = (
        EXPERIMENTS_VERSION_PATH / EXPERIMENTS_ARTIFACTS_FOLDER_NAME
    )

    # Create missing directories if any
    Path(ML_ROOT_PATH).mkdir(parents=True, exist_ok=True)
    Path(FEATURE_LIBRARIES_PATH).mkdir(parents=True, exist_ok=True)
    Path(FEATURE_LIBRARY_VERSION_PATH).mkdir(parents=True, exist_ok=True)
    Path(FEATURE_SELECTION_PATH).mkdir(parents=True, exist_ok=True)
    Path(EXPERIMENTS_PATH).mkdir(parents=True, exist_ok=True)
    Path(EXPERIMENTS_VERSION_PATH).mkdir(parents=True, exist_ok=True)
    Path(EXPERIMENTS_VERSION_ARTIFACTS_PATH).mkdir(parents=True, exist_ok=True)

    # Filenames
    RAW_FILENAME = "data_raw.sav"
    CODEBOOK_FILENAME = Config.CODEBOOK_VERSION
    ATTRIBUTES_FILENAME = "attributes.csv"
    FEATURE_LIBRARY_FILENAME = "feature_library.csv"
    FEATURE_SELECTION_FILENAME = "feature_selection_{}.csv"
    TARGETS_FILENAME = "targets.csv"
    PREDICTIONS_FILENAME = "predictions.csv"
    METRICS_FILENAME = "metrics.csv"
    LOGGING_CONFIG_FILENAME = "logging.conf"
    DASHBOARD_FILENAME = "dashboard.csv"
    ARTIFACTS_CONFIG_FILENAME = "config.json"
    ARTIFACTS_PREDICTIONS_FILENAME = "predictions.csv"

    # Codebook fields
    CODEBOOK_NAME_COL = "raw_variable_name"
    CODEBOOK_TYPE_COL = "raw_variable_type"
    CODEBOOK_OBSERVABILITY_COL = "observability"
    CODEBOOK_COLS = [CODEBOOK_NAME_COL, CODEBOOK_TYPE_COL, CODEBOOK_OBSERVABILITY_COL]

    CODEBOOK_TYPE_INTEGER_LABEL = "integer"
    CODEBOOK_TYPE_FLOAT_LABEL = "float"
    CODEBOOK_TYPE_ORDINAL_LABEL = "ordinal"
    CODEBOOK_TYPE_NOMINAL_SINGLE_LABEL = "nominal_single"
    CODEBOOK_TYPE_NOMINAL_MULTIPLE_LABEL = "nominal_multiple"

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

    # Metrics fields
    METRICS_RUN_ID_FIELD = "run_id"
    METRICS_TIMESTAMP_FIELD = "timestamp"
