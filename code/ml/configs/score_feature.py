class ScoreFeatureConfig:
    # Versioning
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    FEATURE_LIBRARY_VERSION = "feature_library_v2"

    # Feature Selection Grid
    # FEATURE_SELECTION_METHOD_NAMES = [
    #     {
    #         "all": {},
    #         "kbest": {"k": [20]},
    #         "variance": {"threshold": [0.1]},
    #     }
    # ]
    FEATURE_SELECTION_METHOD = ("kbest", {"k": 20})

    # Target choice
    TARGET_NAME = "C.TARGET_SCORE_TOT"
