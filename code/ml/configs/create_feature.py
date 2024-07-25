class CreateFeatureConfig:
    # Versioning
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    CODEBOOK_VERSION = "frozen_codebook_july_25.csv"

    # Target encoding
    TARGET_ENCODING_SINGLE_NOMINAL = False  # set fo False, True not supported anymore
    TARGET_ENCODING_MULTIPLE_NOMINAL = False # set fo False, True not supported anymore
    TARGET_NAME = "C.TARGET_SCORE_TOT"

