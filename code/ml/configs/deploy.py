class DeployConfig:
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    CODEBOOK_VERSION = "frozen_codebook_july_25.csv"

    # Feature selection
    FEATURE_LIBRARY_VERSION = "feature_library_v6"
    FEATURE_SELECTION_METHOD = ("xgboost", {"k": 20})

    # Example
    N_USERS = 3

