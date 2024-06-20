import inspect


class Config:

    # 0. Versioning
    # RUN_TYPE = "SANDBOX_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    CODEBOOK_VERSION = "frozen_codebook_june_9.csv"
    FEATURE_LIBRARY_VERSION = "feature_library_v1"
    EXPERIMENT_NAME = "1_initial_exploration"

    # 1. Predictions Pipeline
    # 1.1. Evaluation
    KFOLD = 5
    METRIC_LIST = [
        "mse",
        "mae",
    ]
    MIN_TRAIN_SIZE = 30
    MIN_TEST_SIZE = 30
    RANDOM_STATE_SPLITTING = 42

    # 1.3. Modelling
    MODEL_LIST = {
        "mean_regressor": {},
        "random_regressor": {},
        "linear_regressor": {"scaler": "minmax", "imputer": "imputer_mean"},
        "extra_tree_regressor": {
            "scaler": "std",
            "imputer": "imputer_mean",
            "hyperparameters": {"random_state": 42},
        },
    }
    TARGET_NAME = "C.TARGET_SCORE_TOT"

    # 2. Sandbox creation
    SANDBOX_N_ATTRIBUTES = 20
    SANDBOX_N_SAMPLE = 200
    SANDBOX_RANDOM_STATE = 42

    # 3. Feature selection pipeline
    FEATURE_SELECTION_METHOD_NAME = "all"

    @classmethod
    def to_dict(cls):
        return {
            name: attr
            for name, attr in cls.__dict__.items()
            if not inspect.isroutine(attr) and not name.startswith("__")
        }
