from constants import Constants as C


class Config:

    # Number of folds for cross-validation
    KFOLD = 5

    # List of models
    MODEL_LIST = [
        "mean_regressor",
        "random_regressor",
        "linear_regressor",
        "extra_tree_regressor",
    ]

    # Target
    TARGET_NAME = C.TARGET_SCORE_TOT

    # List of metrics
    METRIC_LIST = [
        "mse",
    ]

    # Number of non missing targets
    MIN_TRAIN_SIZE = 30
    MIN_TEST_SIZE = 30

    # Random states
    RANDOM_STATE_SPLITTING = 42
