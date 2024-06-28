import inspect


class CrossvalConfig:

    # 0. Versioning
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    CODEBOOK_VERSION = "frozen_codebook_june_21.csv"
    FEATURE_LIBRARY_VERSION = "feature_library_v2"
    EXPERIMENT_NAME = "2_feature_selection"

    # 1. Modeling
    # 1.1. Feature Selection
    FEATURE_SELECTION_METHOD = ("kbest", {"k": 20})

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

    # 1.2. Modelling
    MODEL_LIST = {
        "mean_regressor": {},
        "random_regressor": {},
        "linear_regressor": {"scaler": "robust", "imputer": "imputer_mean"},
        "extra_tree_regressor": {
            "scaler": "robust",
            "imputer": "imputer_mean",
            "hyperparameters": {"random_state": 42},
        },
        "xgboost": {
            "scaler": "robust",
            "imputer": "imputer_mean",
            "hyperparameters": {},
        },
    }
    TARGET_NAME = "C.TARGET_SCORE_TOT"

    # Display config as a dictionary
    @classmethod
    def to_dict(cls):
        return {
            name: attr
            for name, attr in cls.__dict__.items()
            if not inspect.isroutine(attr) and not name.startswith("__")
        }


class CreateSandboxConfig:
    SANDBOX_N_ATTRIBUTES = 20
    SANDBOX_N_SAMPLE = 200
    SANDBOX_RANDOM_STATE = 42
