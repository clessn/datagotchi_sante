from constants import Constants as C

class Config:

    # Number of folds for cross-validation
    KFOLD = 5

    # List of models
    MODEL_LIST = [
        ("mean_regressor", {}),
        ("random_regressor", {}),
    ]

    # Target
    TARGET_NAME = C.TARGET_SCORE_TOT

    # List of metrics
    METRIC_LIST = [
        ("mse", {})
    ]

    # Number of non missing targets for metrics
    N_NON_MISSING_THRESHOLD = 30

    # Random state
    RANDOM_STATE = 42
